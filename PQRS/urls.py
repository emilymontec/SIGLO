from django.urls import path
from .views import (
    PQRSCreateView,
    my_pqrs_list,
    admin_pqrs_list,
    admin_pqrs_edit,
)

urlpatterns = [
    path('create/', PQRSCreateView.as_view(), name='pqrs_create'),
    path('mis-solicitudes/', my_pqrs_list, name='mypqrs_list'),
    path('admin/list/', admin_pqrs_list, name='admin_pqrs_list'),
    path('admin/edit/<int:pqrs_id>/', admin_pqrs_edit, name='admin_pqrs_edit'),
]
