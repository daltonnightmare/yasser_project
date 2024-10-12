from django.contrib import admin
from base.models import *
# Register your models here.

@admin.register(Municipalite)
class MunicipaliteAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'population')

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('user', 'adresse', 'localisation')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user_admin',)

@admin.register(Citoyen)
class CitoyenAdmin(admin.ModelAdmin):
    list_display = ('user', 'adresse', 'municipalite')

@admin.register(DechetType)
class DechetAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')

@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ('citoyen', 'municipalite', 'type_dechet', 'titre', 'date_signalement', 'statut')

@admin.register(PointCollecte)
class PointCollecteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'municipalite', 'jours_operation')

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('type_operation', 'entreprise', 'point_collecte', 'date_operation')

@admin.register(EtatCollecte)
class EtatCollecteAdmin(admin.ModelAdmin):
    list_display = ('municipalite', 'quartier', 'date_derniere_collecte', 'prochaine_collecte_prevue')

@admin.register(Dechet)
class DechetAdmin(admin.ModelAdmin):
    list_display = ('entreprise', 'type_dechet', 'quantite', 'date_dechet')