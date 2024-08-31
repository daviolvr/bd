from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .models import Cliente, Livro, Livro_emprestado

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'biblioteca_app/cadastro.html')
    else:
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        
        try:
            Cliente.objects.get(cpf=cpf)
            messages.error(request, 'CPF já cadastrado.')
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
        
        try:
            cliente = Cliente.objects.get(cpf=cpf, senha=senha)
            request.session['cliente_id'] = cliente.id_cliente
            return redirect('home')
        except Cliente.DoesNotExist:
            messages.error(request, 'CPF ou senha inválidos.')
            return redirect('login')

def logout(request):
    auth_logout(request)  # limpa todas as sessões ativas do usuário
    return redirect('login')

def home(request):
    cliente_id = request.session.get('cliente_id')
    if cliente_id:
        livros = Livro.objects.all()
        context = {'livros': livros, 'cliente_id': cliente_id}
        return render(request, 'biblioteca_app/home.html', context)
    else:
        return redirect('login')

def meus_emprestimos(request, pk):
    cliente_id = request.session.get('cliente_id')
    if cliente_id == pk:
        livros_emprestados = Livro_emprestado.objects.filter(id_cliente=cliente_id)
        context = {'livros_emprestados': livros_emprestados}
        return render(request, 'biblioteca_app/meus_emprestimos.html', context)
    else:
        return redirect('home')

def livro_details(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'biblioteca_app/livro_details.html', {'livro': livro})

def buscar_livros(request):
    query = request.GET.get('q')
    livros = Livro.objects.all()

    if query:
        livros = livros.filter(titulo__icontains=query)

    cliente_id = request.session.get('cliente_id')

    return render(request, 'biblioteca_app/home.html', {'livros': livros, 'cliente_id': cliente_id})

