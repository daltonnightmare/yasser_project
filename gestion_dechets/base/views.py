from django.shortcuts import render
from authentification.models import *
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def afficher_carte(request):
    return render(request, 'base/carte.html')

class CarteView(TemplateView):
    template_name = 'base/carte.html'

class AccountView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'base/account.html'
    context_object_name = 'user'

class AccueilView(TemplateView):
    template_name = 'base/accueil.html'

class SuiviOperationsView(LoginRequiredMixin, ListView):
    template_name = 'base/suivi_operations.html'