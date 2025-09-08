from django.urls import path
from .views import (
    dashboard, 
    liste_filieres, ajouter_filiere, modifier_filiere, supprimer_filiere,
    liste_classes, ajouter_classe, modifier_classe, supprimer_classe,
    liste_professeurs, ajouter_professeur, modifier_professeur, supprimer_professeur,
    liste_matieres, ajouter_matiere, modifier_matiere, supprimer_matiere,
    liste_cours, ajouter_cours, modifier_cours, supprimer_cours
)

urlpatterns = [
    # Tableau de bord
    path('', dashboard, name='dashboard'),
    
    # URLs pour Filières
    path('filieres/', liste_filieres, name='liste_filieres'),
    path('filieres/ajouter/', ajouter_filiere, name='ajouter_filiere'),
    path('filieres/<int:pk>/modifier/', modifier_filiere, name='modifier_filiere'),
    path('filieres/<int:pk>/supprimer/', supprimer_filiere, name='supprimer_filiere'),
    
    # URLs pour Classes
    path('classes/', liste_classes, name='liste_classes'),
    path('classes/ajouter/', ajouter_classe, name='ajouter_classe'),
    path('classes/<int:pk>/modifier/', modifier_classe, name='modifier_classe'),
    path('classes/<int:pk>/supprimer/', supprimer_classe, name='supprimer_classe'),
    
    # URLs pour Professeurs
    path('professeurs/', liste_professeurs, name='liste_professeurs'),
    path('professeurs/ajouter/', ajouter_professeur, name='ajouter_professeur'),
    path('professeurs/<int:pk>/modifier/', modifier_professeur, name='modifier_professeur'),
    path('professeurs/<int:pk>/supprimer/', supprimer_professeur, name='supprimer_professeur'),
    
    # URLs pour Matières
    path('matieres/', liste_matieres, name='liste_matieres'),
    path('matieres/ajouter/', ajouter_matiere, name='ajouter_matiere'),
    path('matieres/<int:pk>/modifier/', modifier_matiere, name='modifier_matiere'),
    path('matieres/<int:pk>/supprimer/', supprimer_matiere, name='supprimer_matiere'),
    
    # URLs pour Cours
    path('cours/', liste_cours, name='liste_cours'),
    path('cours/ajouter/', ajouter_cours, name='ajouter_cours'),
    path('cours/<int:pk>/modifier/', modifier_cours, name='modifier_cours'),
    path('cours/<int:pk>/supprimer/', supprimer_cours, name='supprimer_cours'),
]