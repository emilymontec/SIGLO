"""
URL configuration for SIGLO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from PROJECT_INFO import views as project_views
from LOTES.views import (
    admin_lot_create,
    admin_lot_edit,
    admin_lot_list,
    admin_stage_create,
    admin_stage_edit,
    admin_stage_list,
    lot_list,
    lot_list_api,
    map_view,
)
from USERS.views import register_view, admin_user_list, profile_view, activate_account
from PQRS.views import PQRSCreateView, admin_pqrs_edit, admin_pqrs_list, my_pqrs_list
from SALES.views import (
    admin_payment_create,
    admin_payment_edit,
    admin_payment_list,
    admin_purchase_create,
    admin_purchase_edit,
    admin_purchase_list,
    buy_lot,
    my_purchases_list,
    purchase_detail,
    register_payment,
    validate_payment,
)


def profile_redirect(request):
    return redirect('dashboard')


def logout_view(request):
    logout(request)
    return redirect('login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', project_views.dashboard, name='dashboard'),
    path('lotes/', lot_list, name='lot_list'),
    path('lotes/mapa/', map_view, name='lot_map'),
    path('lotes/<int:lot_id>/comprar/', buy_lot, name='buy_lot'),
    path('api/lotes/', lot_list_api, name='lot_list_api'),
    path('compras/', my_purchases_list, name='my_purchases_list'),
    path('compras/<int:purchase_id>/', purchase_detail, name='purchase_detail'),
    path('compras/<int:purchase_id>/pago/', register_payment, name='register_payment'),
    path('accounts/register/', register_view, name='register'),
    path('cuenta/activar/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('pqrs/nueva/', PQRSCreateView.as_view(), name='pqrs_create'),
    path('pqrs/mias/', my_pqrs_list, name='mypqrs_list'),
    path('panel/lotes/', admin_lot_list, name='admin_lot_list'),
    path('panel/lotes/nuevo/', admin_lot_create, name='admin_lot_create'),
    path('panel/lotes/<int:lot_id>/editar/', admin_lot_edit, name='admin_lot_edit'),
    path('panel/etapas/', admin_stage_list, name='admin_stage_list'),
    path('panel/etapas/nueva/', admin_stage_create, name='admin_stage_create'),
    path('panel/etapas/<int:stage_id>/editar/', admin_stage_edit, name='admin_stage_edit'),
    path('panel/compras/', admin_purchase_list, name='admin_purchase_list'),
    path('panel/compras/nueva/', admin_purchase_create, name='admin_purchase_create'),
    path('panel/compras/<int:purchase_id>/editar/', admin_purchase_edit, name='admin_purchase_edit'),
    path('panel/pagos/<int:payment_id>/validar/', validate_payment, name='admin_payment_validate'),
    path('panel/pagos/', admin_payment_list, name='admin_payment_list'),
    path('panel/pagos/nuevo/', admin_payment_create, name='admin_payment_create'),
    path('panel/pagos/<int:payment_id>/editar/', admin_payment_edit, name='admin_payment_edit'),
    path('panel/pqrs/', admin_pqrs_list, name='admin_pqrs_list'),
    path('panel/pqrs/<int:pqrs_id>/', admin_pqrs_edit, name='admin_pqrs_edit'),
    path('panel/contenido/', project_views.admin_content, name='admin_content'),
    path('panel/usuarios/', admin_user_list, name='admin_user_list'),
    path('perfil/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('accounts/logout/', logout_view),
    path('accounts/profile/', profile_redirect),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
