"""
Fichier de point d'entrée pour Vercel Serverless Functions
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
application = get_wsgi_application()

# Handler pour Vercel
def handler(request, context):
    from django.http import HttpRequest, HttpResponse
    from django.core.handlers.wsgi import WSGIHandler
    
    # Convertir la requête Vercel en requête Django
    environ = {
        'REQUEST_METHOD': request.get('httpMethod', 'GET'),
        'PATH_INFO': request.get('path', '/'),
        'QUERY_STRING': request.get('queryStringParameters', ''),
        'wsgi.input': request.get('body', ''),
        'wsgi.url_scheme': request.get('headers', {}).get('x-forwarded-proto', 'http'),
        'SERVER_NAME': request.get('headers', {}).get('host', 'localhost'),
        'SERVER_PORT': request.get('headers', {}).get('x-forwarded-port', '80'),
    }
    
    # Ajouter les en-têtes HTTP
    for key, value in request.get('headers', {}).items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # Gérer la requête avec Django
    response = WSGIHandler()(environ, lambda x, y: None)
    
    # Convertir la réponse Django en réponse Vercel
    return {
        'statusCode': response.status_code,
        'headers': dict(response.items()),
        'body': response.content.decode('utf-8')
    }
