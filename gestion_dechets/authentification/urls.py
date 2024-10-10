from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('register_entreprise/', views.register_entreprise, name='register_entreprise'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]