from django.urls import path
from . import views

urlpatterns = [
    #path('carte/', views.afficher_carte, name='carte'),
    path('carte/', views.CarteView.as_view(), name='carte'),
]