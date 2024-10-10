from django.shortcuts import render
from authentification.models import *
from django.views.generic import TemplateView

# Create your views here.

def afficher_carte(request):
    return render(request, 'base/carte.html')

class CarteView(TemplateView):
    template_name = 'base/carte.html'

    