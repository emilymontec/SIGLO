from django.urls import path
from .views import map_view

urlpatterns = [
    path('mapa/', map_view, name='map_view'),
]