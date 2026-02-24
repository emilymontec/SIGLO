from django.contrib import messages
from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import EmailUserCreationForm


def register_view(request):
    form = EmailUserCreationForm(request.POST or None)
    if form.is_valid():
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
        body_lines = [
            "Hola,",
            "",
            "Gracias por registrarte en SIGLO.",
            "Para activar tu cuenta y comenzar a invertir, haz clic en el siguiente enlace:",
            "",
            activation_link,
            "",
            "Si tú no solicitaste este registro, puedes ignorar este correo.",
        ]
        body = "\n".join(body_lines)

        email = EmailMessage(
            subject,
            body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            to=[user.email],
        )


        return render(
            request,
            "users/registration_pending.html",
            {
                "email": user.email,
                "activation_link": activation_link,
                "debug": settings.DEBUG,
            },
        )
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
