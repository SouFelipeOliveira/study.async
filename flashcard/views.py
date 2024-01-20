from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Categoria, Flashcard
from django.contrib import messages
from django.contrib.messages import constants

@login_required(login_url='login')
def novo_flashcard(request):
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    categorias = Categoria.objects.all()

    flashcards = Flashcard.objects.filter(user=request.user)

    categoria_filter = request.GET.get('categoria')
    dificuldade_filter = request.GET.get('dificuldade')

    if categoria_filter:
        flashcards = flashcards.filter(categoria_id=categoria_filter)

    if dificuldade_filter:
        flashcards = flashcards.filter(dificuldade=dificuldade_filter)

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
        'flashcards': flashcards
    }
    return render(request, 'novo_flashcard.html', context)

def deleteFlashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)
    flashcard.delete()
    messages.add_message(
            request,
            messages.SUCCESS,
            'Flashcard deletado com sucesso'
        )
    return redirect('novo_flashcard')
