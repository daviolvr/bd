from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .models import Cliente, Livro, Livro_emprestado, Carrinho
from django.http import JsonResponse

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
    auth_logout(request)
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
    cliente_id = request.session.get('cliente_id') 
    return render(request, 'biblioteca_app/livro_details.html', {'livro': livro, 'cliente_id': cliente_id})

def buscar_livros(request):
    query = request.GET.get('q')
    livros = Livro.objects.all()

    if query:
        livros = livros.filter(titulo__icontains=query)

    cliente_id = request.session.get('cliente_id')

    return render(request, 'biblioteca_app/home.html', {'livros': livros, 'cliente_id': cliente_id})

def adicionar_ao_carrinho(request, pk):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    livro = get_object_or_404(Livro, pk=pk)
    
    # Verificar se o livro está emprestado pelo cliente
    if Livro_emprestado.objects.filter(id_cliente=cliente, id_livro=livro).exists():
        return JsonResponse({'error': f'Você já alugou \'{livro.titulo}\'.'})
    
    if livro.estoque <= 0:
        return JsonResponse({'error': 'Infelizmente, o estoque acabou.'})
    
    if Carrinho.objects.filter(cliente=cliente, livro=livro).exists():
        return JsonResponse({'error': f'\'{livro.titulo}\' já está no carrinho.'})
    
    Carrinho.objects.create(cliente=cliente, livro=livro)
    return JsonResponse({'success': 'Livro adicionado ao carrinho com sucesso.'})

def carrinho(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    livros_carrinho = Carrinho.objects.filter(cliente=cliente)
    
    context = {
        'cliente_id': cliente_id,
        'livros_carrinho': livros_carrinho,
    }
    return render(request, 'biblioteca_app/carrinho.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrinho, Livro

def remover_do_carrinho(request, pk):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    livro = get_object_or_404(Livro, pk=pk)
    
    carrinho_item = Carrinho.objects.filter(cliente=cliente, livro=livro)
    if carrinho_item.exists():
        carrinho_item.delete()
        messages.success(request, 'Livro removido do carrinho com sucesso.')
    else:
        messages.error(request, 'Livro não encontrado no carrinho.')
    
    return redirect('carrinho')

def alugar_livros(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    carrinho = Carrinho.objects.filter(cliente=cliente)
    
    if not carrinho.exists():
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')
    
    for item in carrinho:
        livro = item.livro
        if livro.estoque > 0:
            livro.estoque -= 1
            livro.save()
            Livro_emprestado.objects.create(id_livro=livro, id_cliente=cliente)
        else:
            messages.error(request, f'O livro "{livro.titulo}" está fora de estoque.')
    
    carrinho.delete()
    messages.success(request, 'Livros alugados com sucesso.')
    return redirect('meus-emprestimos', pk=cliente_id)

def devolver_livro(request, pk):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    emprestimo = get_object_or_404(Livro_emprestado, id_emprestimo=pk, id_cliente=cliente)
    livro = emprestimo.id_livro
    
    # aumentar o estoque do livro
    livro.estoque += 1
    livro.save()
    
    # remover o registro do livro emprestado
    emprestimo.delete()
    
    # adicionar mensagem de sucesso
    messages.success(request, 'Devolução efetuada.')
    
    return redirect('meus-emprestimos', pk=cliente_id)




