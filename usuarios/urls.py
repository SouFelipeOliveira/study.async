from django.urls import path, include
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.pageLogin, name='login'),
    path('logout/', views.logout, name='logout'),
]