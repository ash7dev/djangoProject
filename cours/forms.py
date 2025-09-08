from django import forms
from .models import Filiere, Classe, Professeur, Matiere, Cours

class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = ['nom', 'description', 'actif']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'filieres', 'niveau', 'effectif_max', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'effectif_max': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class ProfesseurForm(forms.ModelForm):
    class Meta:
        model = Professeur
        fields = ['nom', 'prenom', 'email', 'specialite', 'telephone', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nom', 'description', 'volume_horaire', 'professeur', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'volume_horaire': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['libelle', 'classe', 'professeur', 'matiere', 'date', 'heure_debut', 'heure_fin', 'salle', 'description', 'actif']
        widgets = {
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'salle': forms.Select(attrs={'class': 'form-control'}),
        } 