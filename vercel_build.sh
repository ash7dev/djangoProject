#!/bin/bash

# Activer le mode erreur
set -e

# Installer les dépendances PostgreSQL
apt-get update
apt-get install -y libpq-dev

# Installer les dépendances Python
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate --noinput

# Créer un superutilisateur si nécessaire (désactivé en production par défaut)
if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "Création du superutilisateur..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD') if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() else None" | python manage.py shell
fi

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "Construction terminée avec succès!"
