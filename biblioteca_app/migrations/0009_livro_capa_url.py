# Generated by Django 5.1 on 2024-08-30 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca_app', '0008_livro_estoque'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='capa_url',
            field=models.ImageField(blank=True, null=True, upload_to='livros/capas/'),
        ),
    ]
