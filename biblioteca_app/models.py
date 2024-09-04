from django.db import models
from django.core.validators import MinValueValidator

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
    senha = models.CharField(max_length=128, null=False, default='')

    def __str__(self):
        return f"{self.nome}"

class Livro(models.Model):
    
    FICCAO_CIENTIFICA = 'Ficção Científica'
    NAO_FICCAO = 'Não Ficção'
    BIOGRAFIA = 'Biografia'
    FANTASIA = 'Fantasia'
    # HORROR = 'Horror'
    # INFANTIL = 'Infantil'
    # ACADEMICO = 'Acadêmico'
    # AUTOAJUDA = 'Autoajuda'
    # HQ_MANGA = 'HQs e Mangás'
    # FILOSOFIA = 'Filosofia'
    # ROMANCE = 'Romance'
    # ARTE = 'Arte'
    # TECNOLOGIA = 'Tecnologia'
    # MISTERIO = 'Mistério'
    

    GENERO_CHOICES = [
        (FICCAO_CIENTIFICA, 'Ficção Científica'),
        (NAO_FICCAO, 'Não Ficção'),
        (BIOGRAFIA, 'Biografia'),
        (FANTASIA, 'Fantasia'),
        # (HORROR, 'Horror'),
        # (INFANTIL, 'Infantil'),
        # (ACADEMICO, 'Acadêmico'),
        # (AUTOAJUDA, 'Autoajuda'),
        # (HQ_MANGA, 'HQs e Mangás'),
        # (FILOSOFIA, 'Filosofia'),
        # (ROMANCE, 'Romance'),
        # (ARTE, 'Arte'),
        # (TECNOLOGIA, 'Tecnologia'),
        # (MISTERIO, 'Mistério'),
    ]
    
    id_livro = models.AutoField(primary_key=True)
    autor = models.CharField(max_length=120, null=False)
    titulo = models.CharField(max_length=100, null=False)
    genero = models.CharField(
        max_length=40,
        choices=GENERO_CHOICES,
        default=FICCAO_CIENTIFICA,
    )
    cad_por = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    estoque = models.IntegerField(validators=[MinValueValidator(0)])
    capa_url = models.ImageField(upload_to='livros/capas/', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo}"

class Livro_emprestado(models.Model):
    id_emprestimo = models.AutoField(primary_key=True)
    id_livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Empréstimo {self.id_emprestimo}"

class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('cliente', 'livro')

    def __str__(self):
        return f"{self.cliente.nome} - {self.livro.titulo}"

