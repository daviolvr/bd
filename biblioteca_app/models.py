from django.db import models

# Create your models here.
class Biblioteca(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=120, default='')
    cnpj = models.ForeignKey(Biblioteca, on_delete=models.CASCADE)
    senha = models.CharField(max_length=20, null=False, default='') 

    def __str__(self):
        return f"{self.cnpj} - {self.id_admin}"

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, unique=True, null=False)
    nome = models.CharField(max_length=100, null=False)
    cnpj = models.ForeignKey(Biblioteca, on_delete=models.CASCADE)
    senha = models.CharField(max_length=20, null=False, default='') 

    def __str__(self):
        return f"{self.nome}"

class Livro(models.Model):
    id_livro = models.AutoField(primary_key=True)
    autor = models.CharField(max_length=120, null=False)
    titulo = models.CharField(max_length=100, null=False)
    cnpj = models.ForeignKey(Biblioteca, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo}"

class Livro_emprestado(models.Model):
    id_emprestimo = models.AutoField(primary_key=True)
    id_livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_emprestimo}"


