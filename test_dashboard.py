#!/usr/bin/env python
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.test import RequestFactory
from cours.views import dashboard
from cours.models import Matiere

print("=== TEST VUE DASHBOARD ===")
print()

# Vérifier les matières dans la base
print("1. MATIÈRES DANS LA BASE:")
matieres_count = Matiere.objects.filter(actif=True).count()
print(f"   Matières actives: {matieres_count}")
for matiere in Matiere.objects.filter(actif=True):
    print(f"   - {matiere.nom} (ID: {matiere.id})")

print()

# Tester la vue dashboard
print("2. TEST VUE DASHBOARD:")
factory = RequestFactory()
request = factory.get('/')
response = dashboard(request)

print(f"   Status code: {response.status_code}")

# Extraire le contexte
context = response.context_data
print(f"   Variables dans le contexte: {len(context)}")

print("\n3. VARIABLES IMPORTANTES:")
for key, value in context.items():
    if 'total' in key or 'matiere' in key:
        print(f"   - {key}: {value} (type: {type(value)})")

print("\n4. TEST SPÉCIFIQUE total_matieres:")
total_matieres = context.get('total_matieres')
print(f"   total_matieres: {total_matieres}")
print(f"   total_matieres est None: {total_matieres is None}")
print(f"   total_matieres == 0: {total_matieres == 0}")

print()
print("=== FIN TEST ===") 