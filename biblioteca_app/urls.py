from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('meus-emprestimos/<int:pk>', views.meus_emprestimos, name='meus-emprestimos'),
    path('livro/<int:pk>', views.livro_details, name='livro-details'),
    path('adicionar-ao-carrinho/<int:pk>/', views.adicionar_ao_carrinho, name='adicionar-ao-carrinho'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('remover-do-carrinho/<int:pk>/', views.remover_do_carrinho, name='remover_do_carrinho'),  # Nova rota
    path('alugar-livros/', views.alugar_livros, name='alugar_livros'),
    path('devolver-livro/<int:pk>/', views.devolver_livro, name='devolver-livro'),
    path('', views.buscar_livros, name='home'),
    # path('filtrar_livros/', views.filtrar_livros, name='filtrar_livros'),
]
