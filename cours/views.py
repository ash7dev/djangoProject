from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Filiere, Classe, Professeur, Matiere, Cours
from .forms import FiliereForm, ClasseForm, ProfesseurForm, MatiereForm, CoursForm
import datetime
from django.db import models

# Tableau de bord
def dashboard(request):
    # Récupération des données de base
    filieres = Filiere.objects.filter(actif=True)
    classes = Classe.objects.filter(actif=True)
    professeurs = Professeur.objects.filter(actif=True)
    matieres = Matiere.objects.filter(actif=True)
    cours = Cours.objects.filter(actif=True)
    
    # Calcul des statistiques
    total_heures = sum(matiere.volume_horaire for matiere in matieres)
    total_etudiants = sum(classe.effectif_max for classe in classes)
    salles_utilisees = cours.values('salle').distinct().count()
    
    # Cours récents (5 derniers)
    cours_recents = cours.order_by('-date', '-heure_debut')[:5]
    
    context = {
        'total_filieres': filieres.count(),
        'total_classes': classes.count(),
        'total_professeurs': professeurs.count(),
        'total_matieres': matieres.count(),
        'total_cours': cours.count(),
        'total_heures': total_heures,
        'total_etudiants': total_etudiants,
        'salles_utilisees': salles_utilisees,
        'cours_recents': cours_recents,
        'filieres': filieres[:5],
        'classes': classes[:5],
        'professeurs': professeurs[:5],
        'matieres': matieres[:5],
    }
    return render(request, 'dashboard.html', context)

# Vues pour Filiere
def liste_filieres(request):
    filieres = Filiere.objects.filter(actif=True)
    
    # Statistiques pour le contexte
    total_classes = sum(filiere.classes.filter(actif=True).count() for filiere in filieres)
    total_cours = sum(filiere.classes.filter(actif=True).aggregate(
        total=models.Count('cours', filter=models.Q(cours__actif=True))
    )['total'] or 0 for filiere in filieres)
    
    context = {
        'filieres': filieres,
        'total_classes': total_classes,
        'total_cours': total_cours,
    }
    return render(request, 'filieres/liste_filieres.html', context)

def ajouter_filiere(request):
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Filière ajoutée avec succès!')
            return redirect('liste_filieres')
    else:
        form = FiliereForm()
    return render(request, 'filieres/form_filiere.html', {'form': form, 'titre': 'Ajouter une filière'})

def modifier_filiere(request, pk):
    filiere = get_object_or_404(Filiere, pk=pk)
    if request.method == 'POST':
        form = FiliereForm(request.POST, instance=filiere)
        if form.is_valid():
            form.save()
            messages.success(request, 'Filière modifiée avec succès!')
            return redirect('liste_filieres')
    else:
        form = FiliereForm(instance=filiere)
    return render(request, 'filieres/form_filiere.html', {'form': form, 'titre': 'Modifier la filière'})

def supprimer_filiere(request, pk):
    filiere = get_object_or_404(Filiere, pk=pk)
    if request.method == 'POST':
        filiere.delete()
        messages.success(request, 'Filière supprimée avec succès!')
        return redirect('liste_filieres')
    return render(request, 'filieres/confirmer_suppression.html', {'objet': filiere, 'type': 'filière'})

# Vues pour Classe
def liste_classes(request):
    classes = Classe.objects.filter(actif=True).prefetch_related('filieres')
    
    # Filtres
    filiere_id = request.GET.get('filiere')
    niveau = request.GET.get('niveau')
    
    if filiere_id:
        classes = classes.filter(filieres__id=filiere_id)
    if niveau:
        classes = classes.filter(niveau=niveau)
    
    # Statistiques
    total_etudiants = sum(classe.effectif_max for classe in classes)
    filieres_actives = classes.values('filieres').distinct().count()
    cours_programmes = sum(classe.cours.filter(actif=True).count() for classe in classes)
    
    # Listes pour les filtres
    filieres_list = Filiere.objects.filter(actif=True)
    
    context = {
        'classes': classes,
        'total_etudiants': total_etudiants,
        'filieres_actives': filieres_actives,
        'cours_programmes': cours_programmes,
        'filieres_list': filieres_list,
    }
    return render(request, 'classes/liste_classes.html', context)

def ajouter_classe(request):
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe ajoutée avec succès!')
            return redirect('liste_classes')
    else:
        form = ClasseForm()
    return render(request, 'classes/form_classe.html', {'form': form, 'titre': 'Ajouter une classe'})

def modifier_classe(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        form = ClasseForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe modifiée avec succès!')
            return redirect('liste_classes')
    else:
        form = ClasseForm(instance=classe)
    return render(request, 'classes/form_classe.html', {'form': form, 'titre': 'Modifier la classe'})

def supprimer_classe(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        classe.delete()
        messages.success(request, 'Classe supprimée avec succès!')
        return redirect('liste_classes')
    return render(request, 'classes/confirmer_suppression.html', {'objet': classe, 'type': 'classe'})

# Vues pour Professeur
def liste_professeurs(request):
    professeurs = Professeur.objects.filter(actif=True)
    
    # Filtres
    specialite = request.GET.get('specialite')
    recherche = request.GET.get('recherche')
    
    if specialite:
        professeurs = professeurs.filter(specialite=specialite)
    if recherche:
        professeurs = professeurs.filter(
            models.Q(nom__icontains=recherche) |
            models.Q(prenom__icontains=recherche) |
            models.Q(email__icontains=recherche)
        )
    
    # Statistiques
    total_cours = sum(professeur.cours.filter(actif=True).count() for professeur in professeurs)
    specialites_count = professeurs.values('specialite').distinct().count()
    total_heures = sum(professeur.cours.filter(actif=True).aggregate(
        total=models.Sum('matiere__volume_horaire')
    )['total'] or 0 for professeur in professeurs)
    
    # Liste pour les filtres
    specialites_list = professeurs.values_list('specialite', flat=True).distinct().exclude(specialite='')
    
    context = {
        'professeurs': professeurs,
        'total_cours': total_cours,
        'specialites_count': specialites_count,
        'total_heures': total_heures,
        'specialites_list': specialites_list,
    }
    return render(request, 'professeurs/liste_professeurs.html', context)

def ajouter_professeur(request):
    if request.method == 'POST':
        form = ProfesseurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professeur ajouté avec succès!')
            return redirect('liste_professeurs')
    else:
        form = ProfesseurForm()
    return render(request, 'professeurs/form_professeur.html', {'form': form, 'titre': 'Ajouter un professeur'})

def modifier_professeur(request, pk):
    professeur = get_object_or_404(Professeur, pk=pk)
    if request.method == 'POST':
        form = ProfesseurForm(request.POST, instance=professeur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professeur modifié avec succès!')
            return redirect('liste_professeurs')
    else:
        form = ProfesseurForm(instance=professeur)
    return render(request, 'professeurs/form_professeur.html', {'form': form, 'titre': 'Modifier le professeur'})

def supprimer_professeur(request, pk):
    professeur = get_object_or_404(Professeur, pk=pk)
    if request.method == 'POST':
        professeur.delete()
        messages.success(request, 'Professeur supprimé avec succès!')
        return redirect('liste_professeurs')
    return render(request, 'professeurs/confirmer_suppression.html', {'objet': professeur, 'type': 'professeur'})

# Vues pour Matiere
def liste_matieres(request):
    matieres = Matiere.objects.filter(actif=True).select_related('professeur')
    
    # Filtres
    professeur_id = request.GET.get('professeur')
    filiere_id = request.GET.get('filiere')
    recherche = request.GET.get('recherche')
    
    if professeur_id:
        matieres = matieres.filter(professeur_id=professeur_id)
    if filiere_id:
        # Filtrer par filière (si on ajoute une relation filieres à Matiere)
        pass
    if recherche:
        matieres = matieres.filter(
            models.Q(nom__icontains=recherche) |
            models.Q(description__icontains=recherche)
        )
    
    # Statistiques
    profs_assignes = matieres.filter(professeur__isnull=False).values('professeur').distinct().count()
    heures_total = matieres.aggregate(total=models.Sum('volume_horaire'))['total'] or 0
    cours_programmes = sum(matiere.cours.filter(actif=True).count() for matiere in matieres)
    
    # Listes pour les filtres
    professeurs_list = Professeur.objects.filter(actif=True)
    filieres_list = Filiere.objects.filter(actif=True)
    
    context = {
        'matieres': matieres,
        'profs_assignes': profs_assignes,
        'heures_total': heures_total,
        'cours_programmes': cours_programmes,
        'professeurs_list': professeurs_list,
        'filieres_list': filieres_list,
    }
    return render(request, 'matieres/liste_matieres.html', context)

def ajouter_matiere(request):
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière ajoutée avec succès!')
            return redirect('liste_matieres')
    else:
        form = MatiereForm()
    return render(request, 'matieres/form_matiere.html', {'form': form, 'titre': 'Ajouter une matière'})

def modifier_matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == 'POST':
        form = MatiereForm(request.POST, instance=matiere)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière modifiée avec succès!')
            return redirect('liste_matieres')
    else:
        form = MatiereForm(instance=matiere)
    return render(request, 'matieres/form_matiere.html', {'form': form, 'titre': 'Modifier la matière'})

def supprimer_matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == 'POST':
        matiere.delete()
        messages.success(request, 'Matière supprimée avec succès!')
        return redirect('liste_matieres')
    return render(request, 'matieres/confirmer_suppression.html', {'objet': matiere, 'type': 'matière'})

# Vues pour Cours
def liste_cours(request):
    cours = Cours.objects.filter(actif=True).select_related(
        'classe', 'professeur', 'matiere'
    ).prefetch_related('classe__filieres')
    
    # Filtres
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    classe_id = request.GET.get('classe')
    professeur_id = request.GET.get('professeur')
    matiere_id = request.GET.get('matiere')
    salle = request.GET.get('salle')
    
    if date_debut:
        cours = cours.filter(date__gte=date_debut)
    if date_fin:
        cours = cours.filter(date__lte=date_fin)
    if classe_id:
        cours = cours.filter(classe_id=classe_id)
    if professeur_id:
        cours = cours.filter(professeur_id=professeur_id)
    if matiere_id:
        cours = cours.filter(matiere_id=matiere_id)
    if salle:
        cours = cours.filter(salle=salle)
    
    # Statistiques
    total_heures = sum(c.duree for c in cours)
    classes_impliquees = cours.values('classe').distinct().count()
    professeurs_impliques = cours.values('professeur').distinct().count()
    
    # Listes pour les filtres
    classes_list = Classe.objects.filter(actif=True)
    professeurs_list = Professeur.objects.filter(actif=True)
    matieres_list = Matiere.objects.filter(actif=True)
    salles_list = Cours.TYPE_SALLE
    
    context = {
        'cours': cours,
        'total_heures': total_heures,
        'classes_impliquees': classes_impliquees,
        'professeurs_impliques': professeurs_impliques,
        'classes_list': classes_list,
        'professeurs_list': professeurs_list,
        'matieres_list': matieres_list,
        'salles_list': salles_list,
    }
    return render(request, 'cours/liste_cours.html', context)

def ajouter_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours ajouté avec succès!')
            return redirect('liste_cours')
    else:
        form = CoursForm()
    return render(request, 'cours/form_cours.html', {'form': form, 'titre': 'Ajouter un cours'})

def modifier_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours modifié avec succès!')
            return redirect('liste_cours')
    else:
        form = CoursForm(instance=cours)
    return render(request, 'cours/form_cours.html', {'form': form, 'titre': 'Modifier le cours'})

def supprimer_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        cours.delete()
        messages.success(request, 'Cours supprimé avec succès!')
        return redirect('liste_cours')
    return render(request, 'cours/confirmer_suppression.html', {'objet': cours, 'type': 'cours'})