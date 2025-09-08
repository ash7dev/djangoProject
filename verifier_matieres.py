#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from cours.models import Matiere, Filiere, Classe, Professeur, Cours

print("=== DIAGNOSTIC MATIÈRES ===")
print()

# Vérifier toutes les matières
print("1. TOUTES LES MATIÈRES:")
matieres_all = Matiere.objects.all()
print(f"   Total matières (tous statuts): {matieres_all.count()}")
for matiere in matieres_all:
    print(f"   - ID: {matiere.id}, Nom: '{matiere.nom}', Actif: {matiere.actif}")

print()

# Vérifier les matières actives
print("2. MATIÈRES ACTIVES:")
matieres_actives = Matiere.objects.filter(actif=True)
print(f"   Total matières actives: {matieres_actives.count()}")
for matiere in matieres_actives:
    print(f"   - ID: {matiere.id}, Nom: '{matiere.nom}'")

print()

# Vérifier les autres modèles
print("3. AUTRES MODÈLES:")
print(f"   Filières actives: {Filiere.objects.filter(actif=True).count()}")
print(f"   Classes actives: {Classe.objects.filter(actif=True).count()}")
print(f"   Professeurs actifs: {Professeur.objects.filter(actif=True).count()}")
print(f"   Cours actifs: {Cours.objects.filter(actif=True).count()}")

print()

# Test de la vue dashboard
print("4. TEST VUE DASHBOARD:")
from cours.views import dashboard
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/')
context = dashboard(request).context_data

print(f"   total_matieres dans context: {context.get('total_matieres', 'NON TROUVÉ')}")
print(f"   total_classes dans context: {context.get('total_classes', 'NON TROUVÉ')}")
print(f"   total_professeurs dans context: {context.get('total_professeurs', 'NON TROUVÉ')}")
print(f"   total_cours dans context: {context.get('total_cours', 'NON TROUVÉ')}")

print()

# Vérifier si le problème vient du template
print("5. TEST TEMPLATE:")
print("   Variables disponibles dans le template dashboard:")
for key, value in context.items():
    if 'total' in key or 'matiere' in key:
        print(f"   - {key}: {value}")

print()
print("=== FIN DIAGNOSTIC ===") 