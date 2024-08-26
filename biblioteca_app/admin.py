from django.contrib import admin
from .models import Biblioteca, Admin, Cliente, Livro, Livro_emprestado

admin.site.register(Biblioteca)
admin.site.register(Admin)
admin.site.register(Cliente)
admin.site.register(Livro)
admin.site.register(Livro_emprestado)