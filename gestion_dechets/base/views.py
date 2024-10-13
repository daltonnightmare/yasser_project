from django.shortcuts import render
from authentification.models import *
from .models import *
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
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
    template_name = 'base/suivi_operations/suivi_operations.html'

class SignalementsView(LoginRequiredMixin, ListView):
    template_name = 'base/signalements/signalements.html'
    model = Signalement
    paginate_by = 10
    context_object_name = 'signalements'
    def get_queryset(self):
        user = self.request.user
        if user.is_citoyen:
            return Signalement.objects.filter(citoyen=user).order_by('-date_signalement')

        elif user.is_municipalite:
            return Signalement.objects.filter(municipalite=user.municipalite).order_by('-date_signalement')
        
        return Signalement.objects.all().order_by('-date_signalement')

    


class SignalementDetail(LoginRequiredMixin, DetailView):
    template_name = 'base/signalement/signalement_details.html'
    model = Signalement

class SignalementCreate(LoginRequiredMixin, CreateView):
    template_name = 'base/signalements/signalements_create.html'
    model = Signalement
    fields = ['municipalite', 'type_dechet', 'titre', 'description', 'adresse', 'photo', 'localisation']

    def save(self):
        pass