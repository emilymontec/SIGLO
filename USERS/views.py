from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from .forms import EmailUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
import requests


def register_view(request):
    form = EmailUserCreationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.role = "CLIENT"
                user.save()

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                activation_link = request.build_absolute_uri(
                    f"/cuenta/activar/{uid}/{token}/"
                )

                subject = "Activa tu cuenta en SIGLO"
                html_content = f"""
                <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
                    <h2 style="color: #333;">Bienvenido a SIGLO</h2>
                    <p>Gracias por registrarte. Para activar tu cuenta, haz clic en el botón de abajo:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{activation_link}" style="background-color: #000; color: #fff; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Activar mi cuenta</a>
                    </div>
                    <p style="color: #666; font-size: 14px;">Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
                    <p style="color: #007bff; font-size: 12px;">{activation_link}</p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="color: #999; font-size: 12px;">Si no solicitaste esta cuenta, puedes ignorar este correo.</p>
                </div>
                """

                # Intentar enviar con Resend API primero
                status_code = send_email_resend(user.email, subject, html_content)

                if status_code not in [200, 201]:
                    # Si falla Resend API, intentar con el backend de Django (SMTP)
                    body = f"Hola,\n\nPara activar tu cuenta haz clic en el siguiente enlace:\n\n{activation_link}"
                    email = EmailMessage(
                        subject,
                        body,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                    )
                    email.send(fail_silently=True)

                return render(
                    request,
                    "users/registration_pending.html",
                    {
                        "email": user.email,
                        "activation_link": activation_link if settings.DEBUG else None,
                        "debug": settings.DEBUG
                    },
                )
            except Exception as e:
                print("ERROR EN REGISTRO:", e)
                messages.error(request, "Hubo un error al procesar tu registro. Por favor intenta de nuevo.")
                if settings.DEBUG:
                    messages.error(request, f"Detalle técnico: {str(e)}")
        else:
            print("FORM ERRORS ❌", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return render(request, "users/register.html", {"form": form})

@login_required
def admin_user_list(request):
    role = getattr(request.user, "role", "CLIENT")
    if role != "ADMIN":
        return redirect("dashboard")

    User = get_user_model()
    users = User.objects.all().order_by("date_joined")
    return render(request, "users/admin_user_list.html", {"users": users})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Tu cuenta ha sido activada correctamente. Ahora puedes iniciar sesión.")
        return redirect("login")

    messages.error(request, "El enlace de activación no es válido o ha expirado.")
    return redirect("login")


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        email = request.POST.get("email") or ""
        current_password = request.POST.get("current_password") or ""
        new_password = request.POST.get("new_password") or ""
        confirm_password = request.POST.get("confirm_password") or ""

        if email and email != user.email:
            user.email = email

        if new_password or confirm_password:
            if not current_password or not user.check_password(current_password):
                messages.error(request, "La contraseña actual no es correcta.")
                return render(
                    request,
                    "users/profile.html",
                    {
                        "form": {
                            "email": email or user.email,
                        }
                    },
                )
            if new_password != confirm_password:
                messages.error(request, "Las contraseñas nuevas no coinciden.")
                return render(
                    request,
                    "users/profile.html",
                    {
                        "form": {
                            "email": email or user.email,
                        }
                    },
                )
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("profile")

    context = {
        "form": {
            "email": user.email,
        }
    }
    return render(request, "users/profile.html", context)

def send_email_resend(to_email, subject, html_content):
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "onboarding@resend.dev")
    
    # Si estamos en modo onboarding y no es el correo del dueño, Resend fallará.
    # Pero intentamos usar el remitente configurado.
    
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        },
    )
    print("RESEND STATUS:", response.status_code)
    print("RESEND RESPONSE:", response.text)
    return response.status_code
