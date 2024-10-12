from django.urls import path
from . import views

app_name = 'authentification'
urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('register_entreprise/', views.register_entreprise, name='register_entreprise'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    
]