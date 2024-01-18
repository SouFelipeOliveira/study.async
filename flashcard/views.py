from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Categoria, Flashcard
from django.contrib import messages
from django.contrib.messages import constants

@login_required(login_url='login')
def novo_flashcard(request):
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    categorias = Categoria.objects.all()

    flashcards = Flashcard.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                "Preencha os campos de pergunta e resposta"
            )
            return redirect('novo_flashcard')

        Flashcard.objects.create(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade
        )
        messages.add_message(
            request,
            messages.SUCCESS,
            'Flashcard criado com sucesso'
        )
        return redirect('novo_flashcard')
    
    context = {
        'dificuldades': dificuldades,
        'categorias': categorias,
        'flashcard': flashcards
    }
    return render(request, 'novo_flashcard.html', context)
