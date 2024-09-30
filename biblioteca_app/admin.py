from django.contrib import admin
from .models import Admin, Cliente, Livro, Livro_emprestado, Carrinho, Livro_Carrinho, Genero

class ClienteAdmin(admin.ModelAdmin):
    search_fields = ['cpf', 'nome', 'id_cliente']

    list_display = ('id_cliente', 'nome', 'cpf')  
    list_filter = ('cpf',)
    
class GeneroAdmin(admin.ModelAdmin):
    search_fields = ['id_genero', 'nome']
    
    list_display = ('id_genero', 'nome')
    list_filter = ('nome',)
    
class LivroAdmin(admin.ModelAdmin):
    search_fields = ['id_livro', 'autor', 'titulo']
    
    list_display = ('id_livro', 'titulo', 'autor', 'genero')
    list_filter = ('genero', 'autor')
    
class CarrinhoAdmin(admin.ModelAdmin):
    search_fields = ['id']
    
    list_display = ('id', 'cliente', 'data_adicao')
    list_filter = ('data_adicao',)
    
class Livro_emprestadoAdmin(admin.ModelAdmin):
    search_fields = ['id_emprestimo']
    
    list_display = ('id_emprestimo', 'id_cliente', 'id_livro', 'data_emprestimo', 'data_devolucao')
    list_filter = ('data_emprestimo',)
    
class Livro_CarrinhoAdmin(admin.ModelAdmin):
    search_fields = ['id']
    
    list_display = ('id', 'carrinho', 'livro')
    list_filter = ('id',)

admin.site.register(Admin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Livro, LivroAdmin)
admin.site.register(Livro_emprestado, Livro_emprestadoAdmin)
admin.site.register(Carrinho, CarrinhoAdmin)
admin.site.register(Livro_Carrinho, Livro_CarrinhoAdmin)
admin.site.register(Genero, GeneroAdmin)