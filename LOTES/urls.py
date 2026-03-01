from django.urls import path
from .views import (
    lot_list,
    map_view,
    lot_list_api,
    admin_lot_list,
    admin_lot_create,
    admin_lot_edit,
    admin_stage_list,
    admin_stage_create,
    admin_stage_edit,
)
from SALES.views import buy_lot

urlpatterns = [
    path('', lot_list, name='lot_list'),
    path('mapa/', map_view, name='lot_map'),
    path('api/list/', lot_list_api, name='lot_list_api'),
    path('buy/<int:lot_id>/', buy_lot, name='buy_lot'),
    
    # Admin Lotes
    path('admin/list/', admin_lot_list, name='admin_lot_list'),
    path('admin/create/', admin_lot_create, name='admin_lot_create'),
    path('admin/edit/<int:lot_id>/', admin_lot_edit, name='admin_lot_edit'),
    
    # Admin Etapas
    path('admin/stages/', admin_stage_list, name='admin_stage_list'),
    path('admin/stages/create/', admin_stage_create, name='admin_stage_create'),
    path('admin/stages/edit/<int:stage_id>/', admin_stage_edit, name='admin_stage_edit'),
]
