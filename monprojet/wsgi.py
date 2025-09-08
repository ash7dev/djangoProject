"""
WSGI config for monprojet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')

# Application WSGI de base
application = get_wsgi_application()

# Configuration WhiteNoise pour les fichiers statiques
# Ne fonctionne que si DEBUG=False dans les paramètres
if not os.getenv('DEBUG', '').lower() in ['true', '1']:
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Dossier où collectstatic copie les fichiers statiques
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    # Dossier contenant les fichiers statiques de l'application
    STATICFILES_DIR = os.path.join(BASE_DIR, 'static')
    
    # Configuration de WhiteNoise
    application = WhiteNoise(application, root=STATIC_ROOT, prefix='/static/')
    
    # Ajout des répertoires statiques supplémentaires
    if os.path.exists(STATICFILES_DIR):
        application.add_files(STATICFILES_DIR, prefix='/static/')
    
    # Configuration des en-têtes de sécurité
    from django.conf import settings
    if not settings.DEBUG:
        from whitenoise.middleware import WhiteNoiseMiddleware
        application = WhiteNoiseMiddleware(application)
