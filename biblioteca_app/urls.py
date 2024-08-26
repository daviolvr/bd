from django.urls import path
from .views import login_view, admin_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('admin/', admin_view, name='admin'),
]