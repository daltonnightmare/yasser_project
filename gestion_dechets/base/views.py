from django.shortcuts import render

# Create your views here.

def afficher_carte(request):
    return render(request, 'base/carte.html')