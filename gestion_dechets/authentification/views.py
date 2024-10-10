from django.shortcuts import render
from .models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
# Create your views here.

def register(request):
    if request.method == 'POST':
        nom_utilisateur = request.POST.get('username')
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('password1')
        confirmer_mot_de_passe = request.POST.get('password2')
        if mot_de_passe == confirmer_mot_de_passe:
            user = User.objects.create_user(username=nom_utilisateur, email=email, password=mot_de_passe, is_citoyen=True)
            user.save()
            return redirect('login')
    return render(request, 'authentification/registrer.html')
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
            return redirect('login')
    return render(request, 'authentification/register_entreprise.html')
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('password')
        user = authenticate(email=email, password=mot_de_passe)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'authentification/login.html')

def logout(request):
    logout(request)
    return redirect('login')