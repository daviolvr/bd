from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta
import bcrypt
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, unique=True, null=False)
    nome = models.CharField(max_length=120, default='')
    senha = models.CharField(max_length=128, null=False, default='') 

    def __str__(self):
        return f"CPF: {self.cpf}"

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, unique=True, null=False)
    nome = models.CharField(max_length=100, null=False)
    senha_hash = models.CharField(max_length=128, null=False, default='')

    @property
    def senha(self):
        return None

    @senha.setter
    def senha(self, raw_password):
        if raw_password:
            self.senha_hash = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.senha_hash.encode('utf-8'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'carrinho'):
            Carrinho.objects.create(cliente=self)

    def __str__(self):
        return f"{self.id_cliente} - {self.nome}"
    
class Genero (models.Model):
    id_genero = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.nome}"

class Livro(models.Model):
    id_livro = models.AutoField(primary_key=True)
    autor = models.CharField(max_length=120, null=False)
    titulo = models.CharField(max_length=100, null=False)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    cad_por = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    estoque = models.IntegerField(validators=[MinValueValidator(0)])
    capa_url = models.ImageField(upload_to='livros/capas/', blank=True, null=True)

    def __str__(self):
        return f"{self.id_livro} - {self.titulo}"

class Livro_emprestado(models.Model):
    id_emprestimo = models.AutoField(primary_key=True)
    id_livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateField(default=timezone.now().date() + timedelta(days=30))

    def delete(self, *args, **kwargs):
        livro = self.id_livro
        livro.estoque += 1
        livro.save()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return f"{self.id_cliente.nome} - {self.id_livro.titulo}"

class Carrinho(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrinho de {self.cliente.cpf}"
    
class Livro_Carrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('carrinho', 'livro') 

    def __str__(self):
        return f"{self.carrinho.cliente.cpf} - {self.livro.titulo}"