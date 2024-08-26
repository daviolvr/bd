from django.urls import path
from django.contrib import admin
from .views import login_view, home_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
]