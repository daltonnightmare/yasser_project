from django.urls import path
from . import views

urlpatterns = [
    path('carte/', views.afficher_carte, name='carte'),
]