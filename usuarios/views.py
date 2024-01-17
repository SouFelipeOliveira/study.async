from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from .forms import CadastroForm, LoginForm
from django.contrib.auth.models import User


def cadastro(request):
    form = CadastroForm()

    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                if user.password1 != user.password2:
                    messages.add_message(request, constants.ERROR, 'As senhas não conferem')
                user.username = user.username
                user.save()
                login(request, user)
                messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')
                return redirect('/flashcard/novo_flashcard')
            
            except ValidationError as e:
                messages.add_message(request, constants.ERROR, str(e))
                return redirect(reverse('cadastro'))
            
            except Exception:
                messages.add_message(request, constants.ERROR, 'Erro interno do servidor')
                return redirect(reverse('cadastro'))

    context = {
        'form': form
    }
    return render(request, 'cadastro.html', context)


def pageLogin(request):
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect(reverse('flashcard'))
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.add_messsage(
                    request,
                    constants.ERROR,
                    'O usuário não existe'
                )
                return redirect(reverse('login'))

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('flashcard')
            else:
                messages.add_message(
                    request,
                    constants.ERROR,
                    'Usuário ou senha não existem'
                )
    
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    messages.add_message(request, constants.SUCCESS, 'Deslogado com sucesso')
    return render(request, 'login.html')