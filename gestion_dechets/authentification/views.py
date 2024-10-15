from django.shortcuts import render
from .models import User
from base.models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from base.models import *
from django.contrib.messages import Message
# Create your views here.

def register(request):
    municipalitees = Municipalite.objects.all()
    context = {
        'municipalitees': municipalitees
    }
    if request.method == 'POST':
        nom_utilisateur = request.POST.get('username')
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('password1')
        confirmer_mot_de_passe = request.POST.get('password2')
        municipalite = request.POST.get('municipalite')
        adresse = request.POST.get('adresse') 
        if mot_de_passe == confirmer_mot_de_passe:
            user = User.objects.create_user(username=nom_utilisateur, email=email, password=mot_de_passe, is_citoyen=True)
            user.save()
            citoyen = Citoyen.objects.create(user=user, adresse=adresse, municipalite=municipalite)
            citoyen.save()
            return redirect('authentification:login')
    return render(request, 'authentification/registrer.html', context)

def register_Municipalite(request):
    return render(request, 'authentification/register_municipalite.html')

def register_entreprise(request):
    if request.method == 'POST':
        nom_entreprise = request.POST.get('username')
        email = request.POST.get('email')
        numero_IFU = request.POST.get('numero_IFU')
        mot_de_passe = request.POST.get('password1')
        confirmer_mot_de_passe = request.POST.get('password2')

        if mot_de_passe == confirmer_mot_de_passe:
            user = User.objects.create_user(username=nom_entreprise, email=email, password=mot_de_passe, is_entreprise=True)
            user.save()
            return redirect('authentification:login')
    return render(request, 'authentification/register_entreprise.html')

def register_Municipalite(request):
    if request.method == 'POST':
        nom_municipalite = request.POST.get('nom_municipalite')
        email = request.POST.get('email')
        region = request.POST.get('region')
        population = request.POST.get('population')
        mot_de_passe = request.POST.get('password1')
        confirmer_mot_de_passe = request.POST.get('password2')
        if mot_de_passe == confirmer_mot_de_passe:
            user = User.objects.create_user(username=nom_municipalite, email=email, password=mot_de_passe, is_municipalite=True)
            user.save()
            municipalite = Municipalite.objects.create(user = user, region = region, population = population)
            municipalite.save()
            return redirect('authentification:login')
        return render(request, 'authentification/register_municipalite.html')
    return render(request, 'authentification/register_municipalite.html')

def register_Admin(request):
    if request.method == 'POST':
        nom_admin = request.POST.get('username')
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('password1')
        confirmer_mot_de_passe = request.POST.get('password2')
        if mot_de_passe == confirmer_mot_de_passe:
            user = User.objects.create_user(username=nom_admin, email=email, password=mot_de_passe, is_superuser=True, is_staff=True)
            user.save()
            admin = Admin.objects.create(user = user)
            admin.save()
            return redirect('authentification:login')
        return render(request, 'authentification/register_admin.html')
    return render(request, 'authentification/register_admin.html')


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('password')
        user = authenticate(email=email, password=mot_de_passe)
        if user is not None:
            login(request, user)
            return redirect('base:accueil')
    return render(request, 'authentification/login.html')

def Logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('base:accueil')
    return render(request, 'authentification/logout.html')
