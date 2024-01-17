from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.pageLogin, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]