from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'), 
    path('home/', views.home, name='home'),
    path('meus-emprestimos/<int:pk>', views.meus_emprestimos, name='meus-emprestimos'),
    path('livro/<int:pk>', views.livro_details, name='livro-details'),
    path('', views.buscar_livros, name='home'),
]
