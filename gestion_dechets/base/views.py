from django.shortcuts import render, redirect, get_object_or_404
from authentification.models import *
from .models import *
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.urls import reverse_lazy
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.core.serializers import serialize
# Create your views here.

def afficher_carte(request):
    return render(request, 'base/carte.html')

class CarteView(TemplateView):
    template_name = 'base/carte.html'

class AproposView(TemplateView):
    template_name = 'base/àpropos.html'

class ContactView(TemplateView):
    template_name = 'base/contact.html'

class AccountView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'base/account.html'
    context_object_name = 'user'

class AccueilView(TemplateView):
    template_name = 'base/accueil.html'

class SuiviOperationsView(LoginRequiredMixin, ListView):
    template_name = 'base/suivi_operations/suivi_operations.html'

class SignalementsView(LoginRequiredMixin, ListView):
    template_name = 'base/signalements/signalements.html'
    model = Signalement
    paginate_by = 10
    context_object_name = 'signalements'
    def get_queryset(self):
        user = self.request.user
        if user.is_citoyen:
            return Signalement.objects.filter(citoyen=user).order_by('-date_signalement')

        elif user.is_municipalite:
            return Signalement.objects.filter(municipalite=user.municipalite).order_by('-date_signalement')
        
        return Signalement.objects.all().order_by('-date_signalement')

    


class SignalementDetail(LoginRequiredMixin, DetailView):
    template_name = 'base/signalements/signalement_details.html'
    model = Signalement

class SignalementDelete(LoginRequiredMixin, DeleteView):
    template_name = 'base/signalements/signalement_delete.html'
    model = Signalement
    success_url = reverse_lazy('base:signalements')


@login_required
def SignalementCreate(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        municipalite_id = request.POST.get('municipalite')
        type_dechet_id = request.POST.get('type_dechet')
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        adresse = request.POST.get('adresse')
        localisation = request.POST.get('localisation')  # Récupération de la localisation
        photo = request.FILES.get('photo')  # Pour gérer l'upload de fichier

        # Valider les données
        if not all([municipalite_id, type_dechet_id, titre, description, adresse, localisation]):
            messages.error(request, 'Tous les champs doivent être remplis.')
            return redirect('base:Signaler')

        # Convertir la localisation en objet Point
        try:
            lat, lng = map(float, localisation.split(','))  # Séparer latitude et longitude
            point = Point(lng, lat)  # Notez que l'ordre est (longitude, latitude)
        except ValueError:
            messages.error(request, 'La localisation fournie est invalide.')
            return redirect('base:signalements')

        # Récupérer les objets `Municipalite` et `TypeDechet` correspondants
        municipalite = Municipalite.objects.get(id=municipalite_id)
        type_dechet = DechetType.objects.get(id=type_dechet_id)
        citoyen = get_object_or_404(Citoyen, user=request.user)

        # Créer et sauvegarder l'objet Signalement
        signalement = Signalement(
            municipalite=municipalite,
            type_dechet=type_dechet,
            titre=titre,
            description=description,
            adresse=adresse,
            localisation=point,  # Utiliser l'objet Point
            photo=photo,
            citoyen=citoyen
        )
        signalement.save()

        messages.success(request, 'Le signalement a été créé avec succès.')
        return redirect('base:signalements')
    else:
        municipalites = Municipalite.objects.all()
        type_dechets = DechetType.objects.all()
        context = {
            'municipalites': municipalites,
            'type_dechets': type_dechets,
        }
        return render(request, 'base/signalements/signalements_create.html', context)

class DechetsList(LoginRequiredMixin, ListView):
    model = Dechet
    template_name = 'base/dechets/index.html'
    context_object_name = 'dechets'
    pass

#######################POINTS DE COLLECTE########################

@login_required
def liste_points_collecte(request):
    points_collecte = PointCollecte.objects.all()
    
    # Préparation des données pour la carte
    points_collecte_json = json.dumps([
        {
            'nom': point.nom,
            'localisation': point.localisation.coords  # Supposant que localisation est un champ PointField
        } for point in points_collecte
    ], cls=DjangoJSONEncoder)
    
    return render(request, 'base/pointsdecollecte/index.html', {
        'points_collecte': points_collecte,
        'points_collecte_json': points_collecte_json
    })

@login_required
def creer_point_collecte(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        municipalite_id = request.POST.get('municipalite')
        types_dechets_ids = request.POST.getlist('types_dechets')
        jours_operation = request.POST.get('jours_operation')
        localisation = request.POST.get('localisation')

        if nom and adresse and municipalite_id and types_dechets_ids and jours_operation and localisation:
            latitude, longitude = map(float, localisation.split(','))
            municipalite = Municipalite.objects.get(id=municipalite_id)
            point_collecte = PointCollecte.objects.create(
                nom=nom,
                adresse=adresse,
                municipalite=municipalite,
                jours_operation=jours_operation,
                localisation=Point(longitude, latitude)  # Notez l'ordre : longitude d'abord, puis latitude
            )
            point_collecte.types_dechets.set(DechetType.objects.filter(id__in=types_dechets_ids))
            messages.success(request, 'Le point de collecte a été créé avec succès.')
            return redirect('base:liste_points_collecte')
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')

    municipalites = Municipalite.objects.all()
    types_dechets = DechetType.objects.all()
    jours_choices = PointCollecte.JOURS_CHOICES
    return render(request, 'base/pointsdecollecte/create.html', {
        'municipalites': municipalites,
        'types_dechets': types_dechets,
        'jours_choices': jours_choices
    })


@login_required
def supprimer_point_collecte(request, pk):
    point_collecte = get_object_or_404(PointCollecte, pk=pk)
    if request.method == 'POST':
        point_collecte.delete()
        messages.success(request, 'Le point de collecte a été supprimé avec succès.')
        return redirect('liste_points_collecte')
    return render(request, 'base/pointsdecollecte/supprimer.html', {'point_collecte': point_collecte})

@login_required
def details_point_collecte(request, pk):
    point_collecte = get_object_or_404(PointCollecte, pk=pk)
    return render(request, 'base/pointsdecollecte/details.html', {'point_collecte': point_collecte})

@login_required
def liste_operations(request):
    operations = Operation.objects.all()
    operations_json = json.dumps(list(operations.values()), cls=DjangoJSONEncoder)
    return render(request, 'base/operations/index.html', {
        'operations': operations,
        'operations_json': operations_json
    })

@login_required
def creer_operation(request):
    if request.method == 'POST':
        type_operation = request.POST.get('type_operation')
        entreprise_id = request.POST.get('entreprise')
        point_collecte_id = request.POST.get('point_collecte')
        type_dechet_id = request.POST.get('type_dechet')
        quantite = request.POST.get('quantite')
        date_operation = request.POST.get('date_operation')

        if all([type_operation, entreprise_id, type_dechet_id, quantite, date_operation]):
            entreprise = Entreprise.objects.get(id=entreprise_id)
            type_dechet = DechetType.objects.get(id=type_dechet_id)
            point_collecte = PointCollecte.objects.get(id=point_collecte_id) if point_collecte_id else None

            Operation.objects.create(
                type_operation=type_operation,
                entreprise=entreprise,
                point_collecte=point_collecte,
                type_dechet=type_dechet,
                quantite=float(quantite),
                date_operation=timezone.datetime.strptime(date_operation, '%Y-%m-%dT%H:%M')
            )
            messages.success(request, "L'opération a été créée avec succès.")
            return redirect('base:liste_operations')
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')

    entreprises = Entreprise.objects.all()
    points_collecte = PointCollecte.objects.all()
    types_dechets = DechetType.objects.all()
    return render(request, 'base/operations/create.html', {
        'entreprises': entreprises,
        'points_collecte': points_collecte,
        'types_dechets': types_dechets,
        'operation_types': Operation.OPERATION_TYPES
    })

@login_required
def modifier_operation(request, pk):
    operation = get_object_or_404(Operation, pk=pk)
    if request.method == 'POST':
        type_operation = request.POST.get('type_operation')
        entreprise_id = request.POST.get('entreprise')
        point_collecte_id = request.POST.get('point_collecte')
        type_dechet_id = request.POST.get('type_dechet')
        quantite = request.POST.get('quantite')
        date_operation = request.POST.get('date_operation')

        if all([type_operation, entreprise_id, type_dechet_id, quantite, date_operation]):
            operation.type_operation = type_operation
            operation.entreprise = Entreprise.objects.get(id=entreprise_id)
            operation.point_collecte = PointCollecte.objects.get(id=point_collecte_id) if point_collecte_id else None
            operation.type_dechet = DechetType.objects.get(id=type_dechet_id)
            operation.quantite = float(quantite)
            operation.date_operation = timezone.datetime.strptime(date_operation, '%Y-%m-%dT%H:%M')
            operation.save()
            messages.success(request, "L'opération a été modifiée avec succès.")
            return redirect('base:liste_operations')
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')

    entreprises = Entreprise.objects.all()
    points_collecte = PointCollecte.objects.all()
    types_dechets = DechetType.objects.all()
    return render(request, 'base/operations/update.html', {
        'operation': operation,
        'entreprises': entreprises,
        'points_collecte': points_collecte,
        'types_dechets': types_dechets,
        'operation_types': Operation.OPERATION_TYPES 
    })

@login_required
def supprimer_operation(request, pk):
    operation = get_object_or_404(Operation, pk=pk)
    if request.method == 'POST':
        operation.delete()
        messages.success(request, "L'opération a été supprimée avec succès.")
        return redirect('base:liste_operations')
    return render(request, 'base/operations/delete.html', {'operation': operation})

@login_required
def details_operation(request, pk):
    operation = get_object_or_404(Operation, pk=pk)
    return render(request, 'base/operations/details.html', {'operation': operation})

@login_required
def liste_etats_collecte(request):
    etats_collecte = EtatCollecte.objects.all()
    etats_collecte_json = serialize('geojson', etats_collecte)
    return render(request, 'base/EtatsCollecte/index.html', {
        'etats_collecte': etats_collecte,
        'etats_collecte_json': etats_collecte_json
    })

@login_required
def creer_etat_collecte(request):
    if request.method == 'POST':
        municipalite_id = request.POST.get('municipalite')
        quartier = request.POST.get('quartier')
        date_derniere_collecte = request.POST.get('date_derniere_collecte')
        prochaine_collecte_prevue = request.POST.get('prochaine_collecte_prevue')
        localisation = request.POST.get('localisation')

        if all([municipalite_id, quartier, date_derniere_collecte, prochaine_collecte_prevue]):
            municipalite = Municipalite.objects.get(id=municipalite_id)
            lat, lon = map(float, localisation.split(',')) if localisation else (None, None)
            
            EtatCollecte.objects.create(
                municipalite=municipalite,
                quartier=quartier,
                date_derniere_collecte=timezone.datetime.strptime(date_derniere_collecte, '%Y-%m-%dT%H:%M'),
                prochaine_collecte_prevue=timezone.datetime.strptime(prochaine_collecte_prevue, '%Y-%m-%dT%H:%M'),
                localisation=Point(lon, lat) if lat and lon else None
            )
            messages.success(request, "L'état de collecte a été créé avec succès.")
            return redirect('base:liste_etats_collecte')
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')

    municipalites = Municipalite.objects.all()
    return render(request, 'base/EtatsCollecte/create.html', {'municipalites': municipalites})

@login_required
def modifier_etat_collecte(request, pk):
    etat_collecte = get_object_or_404(EtatCollecte, pk=pk)
    if request.method == 'POST':
        municipalite_id = request.POST.get('municipalite')
        quartier = request.POST.get('quartier')
        date_derniere_collecte = request.POST.get('date_derniere_collecte')
        prochaine_collecte_prevue = request.POST.get('prochaine_collecte_prevue')
        localisation = request.POST.get('localisation')

        if all([municipalite_id, quartier, date_derniere_collecte, prochaine_collecte_prevue]):
            etat_collecte.municipalite = Municipalite.objects.get(id=municipalite_id)
            etat_collecte.quartier = quartier
            etat_collecte.date_derniere_collecte = timezone.datetime.strptime(date_derniere_collecte, '%Y-%m-%dT%H:%M')
            etat_collecte.prochaine_collecte_prevue = timezone.datetime.strptime(prochaine_collecte_prevue, '%Y-%m-%dT%H:%M')
            
            if localisation:
                try:
                    lat, lon = map(float, localisation.strip().split(','))
                    etat_collecte.localisation = Point(lon, lat)
                except ValueError:
                    messages.error(request, 'Format de localisation invalide. Utilisez le format "latitude,longitude".')
                    return render(request, 'base/EtatsCollecte/update.html', {
                        'etat_collecte': etat_collecte,
                        'municipalites': Municipalite.objects.all()
                    })
            else:
                etat_collecte.localisation = None
            
            etat_collecte.save()
            messages.success(request, "L'état de collecte a été modifié avec succès.")
            return redirect('base:liste_etats_collecte')
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')

    municipalites = Municipalite.objects.all()
    return render(request, 'base/EtatsCollecte/update.html', {
        'etat_collecte': etat_collecte,
        'municipalites': municipalites
    })

@login_required
def supprimer_etat_collecte(request, pk):
    etat_collecte = get_object_or_404(EtatCollecte, pk=pk)
    if request.method == 'POST':
        etat_collecte.delete()
        messages.success(request, "L'état de collecte a été supprimé avec succès.")
        return redirect('base:liste_etats_collecte')
    return render(request, 'base/EtatsCollecte/delete.html', {'etat_collecte': etat_collecte})

@login_required
def details_etat_collecte(request, pk):
    etat_collecte = get_object_or_404(EtatCollecte, pk=pk)
    return render(request, 'base/EtatsCollecte/detail.html', {'etat_collecte': etat_collecte})

@login_required
def liste_dechets(request):
    dechets = Dechet.objects.all()
    dechets_json = serialize('geojson', dechets)
    return render(request, 'base/dechets/index.html', {
        'dechets': dechets,
        'dechets_json': dechets_json
    })

@login_required
def creer_dechet(request):
    user = request.user
    
    # Vérifier si l'utilisateur est une municipalité
    try:
        municipalite = user.municipalite
        entreprise = municipalite.entreprise
    except Municipalite.DoesNotExist:
        entreprise = None

    if request.method == 'POST':
        type_dechet_id = request.POST.get('type_dechet')
        quantite = request.POST.get('quantite')
        date_dechet = request.POST.get('date_dechet')
        localisation = request.POST.get('localisation')

        if all([type_dechet_id, quantite, date_dechet]):
            if not entreprise:
                entreprise_id = request.POST.get('entreprise')
                if not entreprise_id:
                    messages.error(request, 'Veuillez sélectionner une entreprise.')
                    return render(request, 'base/dechets/create.html', {
                        'types_dechets': DechetType.objects.all(),
                        'entreprises': Entreprise.objects.all()
                    })
                entreprise = Entreprise.objects.get(id=entreprise_id)

            type_dechet = DechetType.objects.get(id=type_dechet_id)
            
            dechet = Dechet(
                entreprise=entreprise,
                type_dechet=type_dechet,
                quantite=float(quantite),
                date_dechet=timezone.datetime.strptime(date_dechet, '%Y-%m-%dT%H:%M')
            )
            
            if localisation:
                try:
                    lat, lon = map(float, localisation.strip().split(','))
                    dechet.localisation = Point(lon, lat)
                except ValueError:
                    messages.error(request, 'Format de localisation invalide. Utilisez le format "latitude,longitude".')
                    return render(request, 'base/dechets/create.html', {
                        'types_dechets': DechetType.objects.all(),
                        'entreprises': Entreprise.objects.all() if not entreprise else None
                    })
            
            dechet.save()
            messages.success(request, 'Le déchet a été créé avec succès.')
            return redirect('liste_dechets')
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')

    types_dechets = DechetType.objects.all()
    context = {
        'types_dechets': types_dechets,
        'entreprise': entreprise
    }
    
    if not entreprise:
        context['entreprises'] = Entreprise.objects.all()

    return render(request, 'base/dechets/create.html', context)

@login_required
def modifier_dechet(request, pk):
    dechet = get_object_or_404(Dechet, pk=pk)
    if request.method == 'POST':
        entreprise_id = request.POST.get('entreprise')
        type_dechet_id = request.POST.get('type_dechet')
        quantite = request.POST.get('quantite')
        date_dechet = request.POST.get('date_dechet')
        localisation = request.POST.get('localisation')

        if all([entreprise_id, type_dechet_id, quantite, date_dechet]):
            dechet.entreprise = Entreprise.objects.get(id=entreprise_id)
            dechet.type_dechet = DechetType.objects.get(id=type_dechet_id)
            dechet.quantite = float(quantite)
            dechet.date_dechet = timezone.datetime.strptime(date_dechet, '%Y-%m-%dT%H:%M')
            
            if localisation:
                try:
                    lat, lon = map(float, localisation.strip().split(','))
                    dechet.localisation = Point(lon, lat)
                except ValueError:
                    messages.error(request, 'Format de localisation invalide. Utilisez le format "latitude,longitude".')
                    return render(request, 'base/dechets/modifier.html', {
                        'dechet': dechet,
                        'entreprises': Entreprise.objects.all(),
                        'types_dechets': DechetType.objects.all()
                    })
            else:
                dechet.localisation = None
            
            dechet.save()
            messages.success(request, 'Le déchet a été modifié avec succès.')
            return redirect('liste_dechets')
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')

    entreprises = Entreprise.objects.all()
    types_dechets = DechetType.objects.all()
    return render(request, 'base/dechets/modifier.html', {
        'dechet': dechet,
        'entreprises': entreprises,
        'types_dechets': types_dechets
    })

@login_required
def supprimer_dechet(request, pk):
    dechet = get_object_or_404(Dechet, pk=pk)
    if request.method == 'POST':
        dechet.delete()
        messages.success(request, "Le déchet a été supprimé avec succès.")
        return redirect('liste_dechets')
    return render(request, 'base/dechets/delete.html', {'dechet': dechet})

@login_required
def details_dechet(request, pk):
    dechet = get_object_or_404(Dechet, pk=pk)
    return render(request, 'base/dechets/details.html', {'dechet': dechet})