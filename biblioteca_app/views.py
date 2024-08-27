from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente, Admin

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'biblioteca_app/cadastro.html')
    else:
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        
        try:
            Cliente.objects.get(nome=nome, cpf=cpf, senha=senha)
            return HttpResponse('Cliente já cadastrado.')
        except Cliente.DoesNotExist:
            Cliente.objects.create(nome=nome, cpf=cpf, senha=senha)
            return HttpResponse('Cliente cadastrado com sucesso.')

def login(request):
    if request.method =='GET':
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
                return HttpResponse('CPF ou senha inválidos.')
        else:
            try:
                Cliente.objects.get(cpf=cpf, senha=senha)
                return redirect('home')
            except Cliente.DoesNotExist:
                return HttpResponse('CPF ou senha inválidos.')
        
def home(request):
    return render(request, 'biblioteca_app/home.html')