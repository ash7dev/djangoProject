"""
WSGI config for monprojet project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Ajouter le chemin du projet au PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')

# Application WSGI de base
application = get_wsgi_application()

# Configuration pour Vercel
app = application
handler = app  # Pour la compatibilité avec Vercel
