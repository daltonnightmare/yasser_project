from django.db import models
from authentification.models import User
from django.conf import settings
from django.contrib.gis.db import models as gis_models

# Create your models here.
class Municipalite(models.Model):
    REGION_CHOICES = [
        ('BOUCLE DU MOUHOUN', 'boucle du mouhoun'),('CASCADES', 'cascades'),('CENTRE', 'centre'), ('CENTRE-EST', 'centre-est'),
        ('CENTRE-NORD','centre-nord'), ('CENTRE-OUEST', 'centre-ouest'),( 'CENTRE-SUD', 'centre-sud'), ('EST', 'est'), 
        ('HAUTS-BASSINS', 'hauts-bassins'), ('NORD', 'nord'), ('PLATEAU-CENTRAL', 'plateau-central'), ('SAHEL', 'sahel'), 
        ('SUD-OUEST', 'sud-ouest'), 
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='municipalite')
    region = models.CharField(max_length=100, unique=True, choices = REGION_CHOICES)
    population = models.IntegerField()
    zone_geographique = gis_models.PolygonField(srid=4326, null=True, blank=True)
    
    def __str__(self):
        return self.nom

class Entreprise(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entreprise')
    type_activite = models.CharField(max_length=100, choices=[('COLLECTE', 'Collecte'), ('TRAITEMENT', 'Traitement'), ('RECYCLAGE', 'Recyclage')])
    adresse = models.CharField(max_length=200)
    localisation = gis_models.PointField(srid=4326, null=True, blank=True)
    
    def __str__(self):
        return self.nom

class Admin(models.Model):
    user_admin = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pass

class DechetType(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nom
    
class Citoyen(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citoyen')   
    adresse = models.CharField(max_length=200)
    municipalite = models.ForeignKey(Municipalite, on_delete=models.SET_NULL, null=True, related_name='citoyens')
    localisation = gis_models.PointField(srid=4326, null=True, blank=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Signalement(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours de traitement'),
        ('RESOLU', 'Résolu'),
        ('REJETE', 'Rejeté'),
    ]

    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name='signalements')
    municipalite = models.ForeignKey(Municipalite, on_delete=models.CASCADE, related_name='signalements_recus')
    type_dechet = models.ForeignKey(DechetType, on_delete=models.SET_NULL, null=True, related_name='signalements')
    
    titre = models.CharField(max_length=100)
    description = models.TextField()
    adresse = models.CharField(max_length=200)
    date_signalement = models.DateTimeField(auto_now_add=True)
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_resolution = models.DateTimeField(null=True, blank=True)
    
    photo = models.ImageField(upload_to='signalements/', null=True, blank=True)
    localisation = gis_models.PointField(srid=4326, null=True, blank=True)
    
    def __str__(self):
        return f"Signalement {self.id} - {self.titre} ({self.get_statut_display()})"

class PointCollecte(models.Model):
    JOURS_CHOICES = [
        ('LUNDI', 'Lundi'),
        ('MARDI', 'Mardi'),
        ('MERCREDI', 'Mercredi'),
        ('JEUDI', 'Jeudi'),
        ('VENDREDI', 'Vendredi'),
        ('SAMEDI', 'Samedi'),
        ('DIMANCHE', 'Dimanche'),
    ]
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    municipalite = models.ForeignKey(Municipalite, on_delete=models.CASCADE, related_name='points_collecte')
    types_dechets = models.ManyToManyField(DechetType)
    jours_operation = models.CharField(max_length=100, choices=JOURS_CHOICES)
    localisation = gis_models.PointField(srid=4326)

    def __str__(self):
        return f"{self.nom} - {self.municipalite.nom}"

class Operation(models.Model):
    OPERATION_TYPES = [
        ('COLLECTE', 'Collecte'),
        ('TRAITEMENT', 'Traitement'),
        ('RECYCLAGE', 'Recyclage'),
    ]
    type_operation = models.CharField(max_length=20, choices=OPERATION_TYPES)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='operations')
    point_collecte = models.ForeignKey(PointCollecte, on_delete=models.SET_NULL, null=True, blank=True)
    type_dechet = models.ForeignKey(DechetType, on_delete=models.CASCADE)
    quantite = models.FloatField(help_text="Quantité en tonnes")
    date_operation = models.DateTimeField()
    
    def __str__(self):
        return f"{self.get_type_operation_display()} - {self.entreprise.nom} - {self.date_operation}"

class EtatCollecte(models.Model):
    municipalite = models.ForeignKey(Municipalite, on_delete=models.CASCADE, related_name='etats_collecte')
    quartier = models.CharField(max_length=100)
    date_derniere_collecte = models.DateTimeField()
    prochaine_collecte_prevue = models.DateTimeField()
    localisation = gis_models.PointField(srid=4326, null=True, blank=True)

    def __str__(self):
        return f"État collecte - {self.municipalite.nom} - {self.quartier}"
    
class Dechet(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='dechets')
    type_dechet = models.ForeignKey(DechetType, on_delete=models.CASCADE)
    quantite = models.FloatField(help_text="Quantité en tonnes")
    date_dechet = models.DateTimeField()
    localisation = gis_models.PointField(srid=4326, null=True, blank=True)

    def __str__(self):
        return f"Déchet - {self.entreprise.nom} - {self.type_dechet.nom} ({self.quantite} tonnes)"
