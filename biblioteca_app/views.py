from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente, Admin

def login_view(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        is_admin = request.POST.get('is_admin') == 'on'

        if is_admin:
            try:
                admin = Admin.objects.get(cpf=cpf, senha=senha)
                if admin:
                    return redirect('/admin/')
            except Admin.DoesNotExist:
                messages.error(request, 'Admin não encontrado ou senha incorreta.')
        else:
            try:
                cliente = Cliente.objects.get(cpf=cpf, senha=senha)
                if cliente:
                    return redirect('home')
            except Cliente.DoesNotExist:
                messages.error(request, 'Cliente não encontrado ou senha incorreta.')
    
    return render(request, 'biblioteca_app/login.html')

def home_view(request):
    return render(request, 'biblioteca_app/home.html')