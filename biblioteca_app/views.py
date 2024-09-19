from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .models import Cliente, Livro, Livro_emprestado, Carrinho, Livro_Carrinho, Genero
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
    if not cliente_id:
        return redirect('login')

    genero_id = request.GET.get('genero')
    query = request.GET.get('q', '')

    livros = Livro.objects.all()
    if genero_id:
        livros = livros.filter(genero_id=genero_id)
    if query:
        livros = livros.filter(titulo__icontains=query)

    generos = Genero.objects.all()
    context = {'livros': livros, 'generos': generos, 'cliente_id': cliente_id}
    
    return render(request, 'biblioteca_app/home.html', context)

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


def adicionar_ao_carrinho(request, pk):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    livro = get_object_or_404(Livro, pk=pk)
    
    if Livro_emprestado.objects.filter(id_cliente=cliente, id_livro=livro).exists():
        return JsonResponse({'error': f'Você já alugou \'{livro.titulo}\'.'})
    
    carrinho, created = Carrinho.objects.get_or_create(cliente=cliente)
    
    if Livro_Carrinho.objects.filter(carrinho=carrinho, livro=livro).exists():
        return JsonResponse({'error': f'\'{livro.titulo}\' já está no carrinho.'})
    
    if livro.estoque <= 0:
        return JsonResponse({'error': 'Infelizmente, o estoque acabou.'})
    
    Livro_Carrinho.objects.create(carrinho=carrinho, livro=livro)
    return JsonResponse({'success': 'Livro adicionado ao carrinho com sucesso.'})


def carrinho(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    try:
        carrinho = Carrinho.objects.get(cliente=cliente)
    except Carrinho.DoesNotExist:
        carrinho = None

    if carrinho:
        livros_carrinho = Livro_Carrinho.objects.filter(carrinho=carrinho)
    else:
        livros_carrinho = []

    context = {
        'cliente_id': cliente_id,
        'livros_carrinho': livros_carrinho,
    }
    return render(request, 'biblioteca_app/carrinho.html', context)


def remover_do_carrinho(request, pk):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    livro = get_object_or_404(Livro, pk=pk)
    
    carrinho = get_object_or_404(Carrinho, cliente=cliente)
    
    livro_carrinho = Livro_Carrinho.objects.filter(carrinho=carrinho, livro=livro)
    if livro_carrinho.exists():
        livro_carrinho.delete()
        return redirect('carrinho')
    else:
        return JsonResponse({'error': 'Livro não encontrado no carrinho.'})


def alugar_livros(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    try:
        carrinho = Carrinho.objects.get(cliente=cliente)
    except Carrinho.DoesNotExist:
        carrinho = None
    
    if not carrinho:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')
    
    livros_carrinho = Livro_Carrinho.objects.filter(carrinho=carrinho)
    
    if not livros_carrinho.exists():
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')
    
    for item in livros_carrinho:
        livro = item.livro
        if livro.estoque > 0:
            livro.estoque -= 1
            livro.save()
            Livro_emprestado.objects.create(id_livro=livro, id_cliente=cliente)
        else:
            messages.error(request, f'O livro "{livro.titulo}" está fora de estoque.')
    
    livros_carrinho.delete()
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
