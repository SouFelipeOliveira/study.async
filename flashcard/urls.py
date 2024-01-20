from django.urls import path
from .views import (
    novo_flashcard,
    deleteFlashcard,
    iniciar_desafio
)


urlpatterns = [
    path('novo_flashcard/', novo_flashcard, name='novo_flashcard'),
    path('delete/<int:id>/', deleteFlashcard, name='delete_flashcard'),
    path('iniciar_desafio/', iniciar_desafio, name='iniciar_desafio')
]