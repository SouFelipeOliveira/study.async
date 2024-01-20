from django.urls import path
from .views import (
    novo_flashcard,
    deleteFlashcard,
    iniciar_desafio,
    listar_desafio,
    desafio
)


urlpatterns = [
    path('novo_flashcard/', novo_flashcard, name='novo_flashcard'),
    path('delete/<int:id>/', deleteFlashcard, name='delete_flashcard'),
    path('iniciar_desafio/', iniciar_desafio, name='iniciar_desafio'),
    path('listar_desafio/', listar_desafio, name='listar_desafio'),
    path('listar_desafio/<int:id>/', desafio, name='desafio'),
]