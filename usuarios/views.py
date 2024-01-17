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
                user = form.save()
                login(request, user)
                messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
                return redirect('novo_flashcard')
            
            except ValidationError as e:
                messages.add_message(request, constants.ERROR, str(e))
                return redirect('cadastro')

    context = {
        'form': form
    }
    return render(request, 'cadastro.html', context)


def pageLogin(request):
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('novo_flashcard')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('novo_flashcard')
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
    return redirect('login')