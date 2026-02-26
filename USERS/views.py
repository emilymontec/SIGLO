from django.contrib import messages
from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.db import models
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings

from .forms import EmailUserCreationForm

import logging
from mailjet_rest import Client


class CustomLoginView(LoginView):
    def form_invalid(self, form):
        username = self.request.POST.get('username')
        User = get_user_model()
        # Buscamos al usuario por email o username (case-insensitive)
        user = User.objects.filter(models.Q(email__iexact=username) | models.Q(username__iexact=username)).first()
        
        if user and not user.is_active:
            # Agregamos un atributo al formulario para identificar el error de verificación
            form.is_unverified = True
            # Limpiamos errores previos para que no aparezca el aviso de credenciales inválidas
            form._errors = {} 
            return self.render_to_response(self.get_context_data(form=form))
            
        return super().form_invalid(form)


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
        
        # Contexto para la plantilla HTML
        context = {
            'user_name': user.get_full_name() or user.username,
            'activation_link': activation_link,
        }
        
        # Renderizar la versión HTML y de texto plano
        html_content = render_to_string('emails/activation_email.html', context)
        text_content = f"Hola {context['user_name']},\n\nGracias por registrarte en SIGLO.\n\nPara activar tu cuenta, haz clic en el siguiente enlace:\n{activation_link}\n\nNota: Si no encuentras el correo, revisa tu carpeta de SPAM."
        
        import os
        logger = logging.getLogger(__name__)
        
        try:
            esult = send_mailjet_email(
                subject=subject,
                html_content=html_content,
                to_email=user.email,
                to_name=user.get_full_name() or user.username
                )
            print("Mailjet response:", result.status_code, result.json())
            
        except Exception as e:
            print(f"ERROR CORREO: {type(e).__name__}: {e}")

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
        messages.add_message(request, messages.SUCCESS, 
                           "Tu cuenta ha sido activada correctamente. Ahora puedes iniciar sesión.", 
                           extra_tags='activated')
        return redirect("login")

    messages.error(request, "El enlace de activación no es válido o ha expirado.")
    return redirect("login")


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        email = request.POST.get("email") or ""
        first_name = request.POST.get("first_name") or ""
        last_name = request.POST.get("last_name") or ""
        current_password = request.POST.get("current_password") or ""
        new_password = request.POST.get("new_password") or ""
        confirm_password = request.POST.get("confirm_password") or ""

        if email and email != user.email:
            user.email = email
        
        user.first_name = first_name
        user.last_name = last_name

        if new_password or confirm_password:
            if not current_password or not user.check_password(current_password):
                messages.error(request, "La contraseña actual no es correcta.")
                return render(
                    request,
                    "users/profile.html",
                    {
                        "form": {
                            "email": email or user.email,
                            "first_name": first_name or user.first_name,
                            "last_name": last_name or user.last_name,
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
                            "first_name": first_name or user.first_name,
                            "last_name": last_name or user.last_name,
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
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }
    return render(request, "users/profile.html", context)

import os

def send_mailjet_email(subject, html_content, to_email, to_name=''):
    mailjet = Client(
        auth=(os.environ.get('MJ_APIKEY_PUBLIC'), os.environ.get('MJ_APIKEY_PRIVATE')),
        version='v3.1'
    )
    data = {
        'Messages': [
            {
                'From': {
                    'Email': 'siglo.sys.py@gmail.com',
                    'Name': 'SIGLO'
                },
                'To': [
                    {
                        'Email': to_email,
                        'Name': to_name
                    }
                ],
                'Subject': subject,
                'HTMLPart': html_content,
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result