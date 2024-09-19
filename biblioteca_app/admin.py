from django.contrib import admin
from .models import Admin, Cliente, Livro, Livro_emprestado, Carrinho, Livro_Carrinho

admin.site.register(Admin)
admin.site.register(Cliente)
admin.site.register(Livro)
admin.site.register(Livro_emprestado)
admin.site.register(Carrinho)
admin.site.register(Livro_Carrinho)