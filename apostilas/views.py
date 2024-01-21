from django.shortcuts import render, redirect, HttpResponse
from .models import Apostila, ViewApostila
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def adicionar_apostilas(request):

    apostilas = Apostila.objects.filter(user=request.user)

    views_totais = ViewApostila.objects.filter(
        apostila__user=request.user
    ).count()

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        arquivo = request.FILES['arquivo']

        Apostila.objects.create(
            user = request.user,
            titulo = titulo,
            arquivo = arquivo
        )
        messages.add_message(
            request,
            constants.SUCCESS,
            'Apostila adicionada com sucesso!'
        )


        return redirect('adicionar_apostilas')
    context = {
        'apostilas': apostilas,
        'views_totais': views_totais
    }
    return render(request, 'adicionar_apostilas.html', context)


def excluir_apostila(request, id):
    apostila = Apostila.objects.get(id=id)

    if apostila.user != request.user:
        messages.add_message(
            request,
            constants.ERROR,
            'Você não tem permissão para excluir essa apostila'
        )
    apostila.delete()
    messages.add_message(
        request,
        constants.SUCCESS,
        'Apostila excluída com sucesso!'
    )
    return render(request, 'adicionar_apostilas')