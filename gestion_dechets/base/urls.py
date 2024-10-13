from django.urls import path
from . import views
app_name = 'base'
urlpatterns = [
    #path('carte/', views.afficher_carte, name='carte'),
    path('carte/', views.CarteView.as_view(), name='carte'),
    path('account/<int:pk>/', views.AccountView.as_view(), name='account'),
    path('', views.AccueilView.as_view(), name='accueil'),
    path('suivi-operations/', views.SuiviOperationsView.as_view(), name='suivi_operations'),
    path('signalements/', views.SignalementsView.as_view(), name='signalements'),
    path('signalements_details/<int:pk>/', views.SignalementDetail.as_view(), name='signalements_details'),
    path('Signaler/', views.SignalementCreate.as_view(), name='Signaler'),
]
