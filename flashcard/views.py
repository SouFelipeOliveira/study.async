from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import (
    Categoria,
    Flashcard,
    Desafio,
    FlashcardDesafio
    )
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages import constants
from operator import itemgetter
import json
from django.http import HttpResponse

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

@login_required(login_url='login')
def deleteFlashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)

    if flashcard.user != request.user:
        messages.add_message(
            request,
            constants.ERROR,
            'Você não tem permissão para deletar esse flashcard'
        )
    flashcard.delete()
    messages.add_message(
        request, constants.SUCCESS, 'Flashcard deletado com sucesso!'
    )
    return redirect('/flashcard/novo_flashcard')


@login_required(login_url='login')
def iniciar_desafio(request):
    
    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtde_perguntas = request.POST.get('qtd_perguntas')

        try:
            desafio = Desafio(
                user=request.user,
                titulo=titulo,
                dificuldade=dificuldade,
                quantidade_perguntas=qtde_perguntas
            )
            desafio.save()

            desafio.categoria.add(*categorias)

            messages.add_message(
                request,
                messages.SUCCESS,
                'Desafio criado com sucesso'
            )
        except Exception:
            messages.add_message(
                request,
                constants.ERROR,
                'Erro ao criar desafio'
            )
            return redirect('iniciar_desafio')


        flashcards = Flashcard.objects.filter(
            Q(user=request.user) &
            Q(dificuldade=dificuldade) &
            Q(categoria_id__in=categorias)
            ).order_by('?')
        
        if flashcards.count() < int(qtde_perguntas):
            messages.add_message(
                request,
                constants.ERROR,
                'Não há flashcards suficientes para criar o desafio'
            )
            return redirect('novo_flashcard')

        flashcards = flashcards[:int(qtde_perguntas)]

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                flashcard=f,
            )
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        return redirect(f'/flashcard/desafio/{desafio.id}')

    context = {
        'categorias': categorias,
        'dificuldades': dificuldades
    }
    return render(request, 'iniciar_desafio.html', context)


@login_required(login_url='login')
def listar_desafio(request):
    desafios = Desafio.objects.filter(user=request.user)

    categoria_filter = request.GET.get('categoria')
    dificuldade_filter = request.GET.get('dificuldade')

    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES

    if categoria_filter:
        desafios = desafios.filter(categoria__id=categoria_filter)

    if dificuldade_filter:
        desafios = desafios.filter(dificuldade=dificuldade_filter)



    context = {
        'desafios': desafios,
        'categorias': categorias,
        'dificuldades': dificuldades
        }
    return render(request, 'listar_desafios.html', context)


def deletar_desafio(request, id):
    desafio = Desafio.objects.get(id=id)

    if desafio.user != request.user:
        messages.add_message(
            request,
            constants.ERROR,
            'Você não tem permissão para deletar esse flashcard'
        )
    desafio.delete()
    messages.add_message(
        request,
        constants.SUCCESS,
        'Desafio deletado com sucesso!'
    )
    return redirect('listar_desafio')


@login_required(login_url='login')
def desafio(request, id):
    desafio = Desafio.objects.get(id=id)

    if desafio.user != request.user:
        raise Http404
    

    acertos = desafio.flashcards.filter(
        respondido=True, 
        acertou=True
        ).count()
    
    erros = desafio.flashcards.filter(
        respondido=True, 
        acertou=False
        ).count()
    
    faltantes = desafio.flashcards.filter(
       respondido=False
        ).count()

    context = {
        'desafio': desafio,
        'acertos': acertos,
        'erros': erros,
        'faltantes': faltantes
    }
    return render(request, 'desafio.html', context)


def responder_flashcard(request, id):
    flashcard_desafio = FlashcardDesafio.objects.get(id=id)
    acertou = request.GET.get('acertou')
    desafio_id = request.GET.get('desafio_id')

    if not flashcard_desafio.flashcard.user == request.user:
        raise Http404

    flashcard_desafio.respondido = True

    flashcard_desafio.acertou = True if acertou == '1' else False
    flashcard_desafio.save()
    
    return redirect(f'/flashcard/desafio/{desafio_id}')


def relatorio(request, id):
    desafio = Desafio.objects.get(id=id)

    acertos = desafio.flashcards.filter(acertou=True).count()
    erros = desafio.flashcards.filter(acertou=False).count()

    dados_grafico = [acertos, erros]

    categorias = desafio.categoria.all()

    nome_categoria = [i.nome for i in categorias]

    dados_grafico2 = []
    for categoria in categorias:
        dados_grafico2.append(
            desafio.flashcards.filter(
            Q(flashcard__categoria=categoria) &
            Q(acertou=True)
            ).count()
        )

#TODO FAZER O RANKING DE ACERTOS POR CATEGORIA
        
    context = {
        'desafio': desafio,
        'dados_grafico': json.dumps(dados_grafico),
        'nome_categoria': json.dumps(nome_categoria),
        'dados_grafico2': json.dumps(dados_grafico2),
        'categorias': categorias
    }

    return render(request, 'relatorio.html', context)