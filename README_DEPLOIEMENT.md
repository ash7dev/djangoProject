# Guide de déploiement pour Vercel avec Supabase

Ce guide explique comment déployer cette application Django sur Vercel avec une base de données PostgreSQL hébergée sur Supabase.

## Prérequis

- Un compte [Vercel](https://vercel.com)
- Un compte [Supabase](https://supabase.com)
- Git installé localement
- Python 3.9+ installé localement

## Configuration de la base de données Supabase

1. Créez un nouveau projet sur Supabase
2. Allez dans l'onglet "Database" et notez les informations de connexion :
   - Host
   - Port (généralement 5432)
   - Database name
   - Username
   - Password
3. Activez les extensions nécessaires dans la base de données :
   ```sql
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   ```

## Configuration des variables d'environnement

1. Créez un fichier `.env` à la racine du projet avec les variables suivantes :
   ```env
   # Configuration de base
   DEBUG=False
   SECRET_KEY=votre_clé_secrète_ici
   ALLOWED_HOSTS=.vercel.app,.now.sh,localhost,127.0.0.1

   # Configuration Supabase (PostgreSQL)
   DB_NAME=votre_nom_de_base
   DB_USER=postgres
   DB_PASSWORD=votre_mot_de_passe
   DB_HOST=db.xxxxx.supabase.co
   DB_PORT=5432

   # Clé API Supabase
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=votre_clé_api_supabase_ici
   ```

## Déploiement sur Vercel

1. Installez la CLI Vercel si ce n'est pas déjà fait :
   ```bash
   npm install -g vercel
   ```

2. Connectez-vous à Vercel :
   ```bash
   vercel login
   ```

3. Configurez les variables d'environnement dans Vercel :
   ```bash
   vercel env add
   ```
   Ajoutez toutes les variables du fichier `.env`.

4. Déployez l'application :
   ```bash
   vercel --prod
   ```

## Configuration des variables d'environnement dans l'interface Vercel

1. Allez sur le tableau de bord Vercel
2. Sélectionnez votre projet
3. Allez dans "Settings" > "Environment Variables"
4. Ajoutez toutes les variables du fichier `.env`

## Configuration de la base de données

1. Appliquez les migrations :
   ```bash
   python manage.py migrate
   ```

2. Créez un superutilisateur (optionnel) :
   ```bash
   python manage.py createsuperuser
   ```

## Déploiement continu avec GitHub

1. Poussez votre code sur un dépôt GitHub
2. Connectez votre dépôt GitHub à Vercel
3. Vercel déploiera automatiquement les changements à chaque push sur la branche principale

## Dépannage

### Erreurs de connexion à la base de données
- Vérifiez que l'adresse IP de Vercel est autorisée dans les paramètres de sécurité de Supabase
- Vérifiez les identifiants de la base de données

### Problèmes de fichiers statiques
- Vérifiez que `collectstatic` s'exécute correctement
- Vérifiez les permissions des dossiers

## Sécurité

- Ne commettez jamais le fichier `.env` dans Git
- Utilisez des variables d'environnement pour les informations sensibles
- Activez le SSL dans les paramètres de votre base de données
