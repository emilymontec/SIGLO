from django.urls import path
from .views import dashboard, admin_content

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/content/', admin_content, name='admin_content'),
]
