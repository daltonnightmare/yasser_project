from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .manager import UserManager
from django.conf import settings
from django.contrib.gis.db import models as gis_models

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_citoyen = models.BooleanField(default=False, help_text="Designates whether this user is a citizen.")
    is_entreprise = models.BooleanField(default=False, help_text="Designates whether this user is an enterprise.")
    is_municipalite = models.BooleanField(default=False, help_text="Designates whether this user is a municipalite.")

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first name plus the last name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)



class Municipalite(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='municipalite')
    nom = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    population = models.IntegerField()
    zone_geographique = gis_models.PolygonField(srid=4326, null=True, blank=True)
    
    def __str__(self):
        return self.nom

class Entreprise(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entreprise')
    nom = models.CharField(max_length=100)
    type_activite = models.CharField(max_length=100, choices=[('COLLECTE', 'Collecte'), ('TRAITEMENT', 'Traitement'), ('RECYCLAGE', 'Recyclage')])
    adresse = models.CharField(max_length=200)
    localisation = gis_models.PointField(srid=4326)
    
    def __str__(self):
        return self.nom

class Admin(models.Model):
    user_admin = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pass

class DechetType(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.nom
    
class Citoyen(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citoyen')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    municipalite = models.ForeignKey(Municipalite, on_delete=models.SET_NULL, null=True, related_name='citoyens')
    localisation = gis_models.PointField(srid=4326)
    
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
    localisation = gis_models.PointField(srid=4326)
    
    def __str__(self):
        return f"Signalement {self.id} - {self.titre} ({self.get_statut_display()})"

class PointCollecte(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    municipalite = models.ForeignKey(Municipalite, on_delete=models.CASCADE, related_name='points_collecte')
    types_dechets = models.ManyToManyField(DechetType)
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
    taux_remplissage = models.FloatField(help_text="Taux de remplissage en pourcentage")
    localisation = gis_models.PointField(srid=4326)

    def __str__(self):
        return f"État collecte - {self.municipalite.nom} - {self.quartier}"