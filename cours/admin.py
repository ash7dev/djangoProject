from django.contrib import admin
from .models import Filiere, Classe, Professeur, Matiere, Cours


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'actif')
    list_filter = ('actif',)
    search_fields = ('nom', 'description')
    list_editable = ('actif',)


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'effectif_max', 'actif', 'filieres_display')
    list_filter = ('niveau', 'actif', 'filieres')
    search_fields = ('nom', 'filieres__nom')
    autocomplete_fields = ('filieres',)
    list_editable = ('actif', 'effectif_max')
    
    def filieres_display(self, obj):
        return ", ".join([f.nom for f in obj.filieres.all()])
    filieres_display.short_description = 'Filières'


@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'specialite', 'telephone', 'actif')
    list_filter = ('actif', 'specialite')
    search_fields = ('nom', 'prenom', 'email', 'specialite')
    list_editable = ('actif',)


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'professeur', 'volume_horaire', 'actif')
    list_filter = ('actif', 'professeur')
    search_fields = ('nom', 'description', 'professeur__nom', 'professeur__prenom')
    autocomplete_fields = ('professeur',)
    list_editable = ('actif',)


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = (
        'libelle', 'classe', 'professeur', 'matiere', 'date', 
        'heure_debut', 'heure_fin', 'duree_affichage', 'salle', 'actif'
    )
    list_filter = (
        'actif', 'date', 'salle', 'classe__filieres', 'classe__niveau', 
        'professeur', 'matiere'
    )
    search_fields = (
        'libelle', 'description', 'classe__nom',
        'professeur__nom', 'professeur__prenom', 'matiere__nom'
    )
    autocomplete_fields = ('classe', 'professeur', 'matiere')
    date_hierarchy = 'date'
    list_editable = ('actif',)
    readonly_fields = ('created_at', 'updated_at')
    
    def duree_affichage(self, obj):
        return f"{obj.duree:.1f}h"
    duree_affichage.short_description = 'Durée'