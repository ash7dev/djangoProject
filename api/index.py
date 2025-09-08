"""
Point d'entrée Vercel pour Django: expose un WSGI callable nommé `app`.
"""

import os
import sys
from pathlib import Path

# Ajouter le chemin du projet au PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')

# Importation de l'application WSGI Django
from django.core.wsgi import get_wsgi_application

# Vercel Python recherche un objet WSGI appelé `app`
app = get_wsgi_application()

# Pour compatibilité avec certaines docs/examples
application = app
