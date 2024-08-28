from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Cliente, Admin

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'biblioteca_app/cadastro.html')
    else:
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        
        try:
            Cliente.objects.get(cpf=cpf)
            messages.error(request, 'Cliente já cadastrado.')
        except Cliente.DoesNotExist:
            if len(cpf) == 11: 
                Cliente.objects.create(nome=nome, cpf=cpf, senha=senha)
                messages.success(request, 'Cliente cadastrado com sucesso.')
            else:
                messages.error(request, 'CPF deve ter 11 números.')

        return redirect('cadastro') 

def login(request):
    if request.method == 'GET':
        return render(request, 'biblioteca_app/login.html')
    else:
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        is_admin = request.POST.get('is_admin') == 'on'
        
        if is_admin:
            try:
                Admin.objects.get(cpf=cpf, senha=senha)
                return redirect('/admin/')
            except Admin.DoesNotExist:
                messages.error(request, 'CPF ou senha inválidos.')
                return redirect('login')
        else:
            try:
                Cliente.objects.get(cpf=cpf, senha=senha)
                return redirect('home')
            except Cliente.DoesNotExist:
                messages.error(request, 'CPF ou senha inválidos.')
                return redirect('login')
        
def home(request):
    return render(request, 'biblioteca_app/home.html')