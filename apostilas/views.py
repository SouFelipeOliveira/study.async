from django.shortcuts import render, redirect
from .models import Apostila, ViewApostila
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404

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
    apostila = get_object_or_404(Apostila, id=id, user=request.user)
    if apostila.arquivo:
        apostila.arquivo.delete()

    apostila.delete()
    messages.add_message(
        request,
        constants.SUCCESS,
        'Apostila excluída com sucesso!'
    )
    return redirect('adicionar_apostilas')


def apostila(request, id):
    apostila = Apostila.objects.get(id=id)

    ViewApostila.objects.create(
        ip = request.META['REMOTE_ADDR'],
        apostila = apostila
    )

    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
    views_totais = ViewApostila.objects.filter(apostila=apostila).count()

    context = {
        'apostila': apostila,
        'views_unicas': views_unicas,
        'views_totais': views_totais
        }
    return render(request, 'apostilas.html', context)
