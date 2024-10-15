from django.urls import path
from . import views
app_name = 'base'
urlpatterns = [
    #path('carte/', views.afficher_carte, name='carte'),
    path('carte/', views.CarteView.as_view(), name='carte'),
    path('account/<int:pk>/', views.AccountView.as_view(), name='account'),
    path('', views.AccueilView.as_view(), name='accueil'),
    path('apropos/', views.AproposView.as_view(), name='apropos'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('suivi-operations/', views.SuiviOperationsView.as_view(), name='suivi_operations'),
    #signalements
    path('signalements/', views.SignalementsView.as_view(), name='signalements'),
    path('signalements_details/<int:pk>/', views.SignalementDetail.as_view(), name='signalements_details'), 
    path('signalements_delete/<int:pk>/', views.SignalementDelete.as_view(), name='signalements_delete'),
    path('Signaler/', views.SignalementCreate, name='Signaler'),
    #DECHETS
    #POINTS DE COLLECTE
    path('points_collecte/', views.liste_points_collecte, name='liste_points_collecte'),
   
    #path('points_collecte_delete/<int:pk>/', views.PointCollecteDelete.as_view(), name='point_collecte_delete'),
    path('points_collecte_create/', views.creer_point_collecte, name='points_collecte_create'),
    #OPERATIONS
    path('operations/', views.liste_operations, name='liste_operations'),
    path('operations_details/<int:pk>/', views.details_operation, name='operations_details'),
    path('operations_delete/<int:pk>/', views.supprimer_operation, name='operations_delete'),
    path('operations_create/', views.creer_operation, name='operations_create'),
    path('operations_update/<int:pk>/', views.modifier_operation, name='operations_update'),
    #ETATS DE COLLECTE
    path('etats_collecte/', views.liste_etats_collecte, name='liste_etats_collecte'),
    path('etats_collecte_create/', views.creer_etat_collecte, name='etats_collecte_create'),
    path('etats_collecte_update/<int:pk>/', views.modifier_etat_collecte, name='etats_collecte_update'),
    path('etats_collecte_delete/<int:pk>/', views.supprimer_etat_collecte, name='etats_collecte_delete'),
    path('etats_collecte_details/<int:pk>/', views.details_etat_collecte, name='etats_collecte_details'),
    #DECHETS
    path('dechets/', views.liste_dechets, name='liste_dechets'),
    path('dechets_create/', views.creer_dechet, name='dechets_create'),
    path('dechets_update/<int:pk>/', views.modifier_dechet, name='dechets_update'),
    path('dechets_delete/<int:pk>/', views.supprimer_dechet, name='dechets_delete'),
    path('dechets_details/<int:pk>/', views.details_dechet, name='dechets_details'),

]