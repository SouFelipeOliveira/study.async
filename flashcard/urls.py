from django.urls import path
from .views import (
    novo_flashcard,
    deleteFlashcard

)


urlpatterns = [
    path('novo_flashcard/', novo_flashcard, name='novo_flashcard'),
    path('delete/<int:id>/', deleteFlashcard, name='delete_flashcard')
]