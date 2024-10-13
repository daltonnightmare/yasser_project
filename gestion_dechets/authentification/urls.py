from django.urls import path
from . import views

app_name = 'authentification'
urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('register_entreprise/', views.register_entreprise, name='register_entreprise'),
    path('register_municipalite/', views.register_Municipalite, name='register_municipalite'),
    path('register_admin/', views.register_Admin, name='register_admin'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    
]