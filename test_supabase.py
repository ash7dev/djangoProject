import psycopg2
from psycopg2 import sql
import ssl

# Paramètres de connexion depuis .env.example
db_params = {
    'dbname': 'coursdb',
    'user': 'postgres',
    'password': 'Senegale1228/',
    'host': 'db.xsepgmurvwguoygdmlza.supabase.co',
    'port': '5432',
    'sslmode': 'require',
    'options': '-c search_path=public',
    'connect_timeout': 10  # Timeout de 10 secondes
}

# Note: L'URL de l'API est différente de l'URL de la base de données
# API: https://xsepgmurvwguoygdmlza.supabase.co
# Base de données: db.xsepgmurvwguoygdmlza.supabase.co:5432/coursdb

try:
    # Établir une connexion SSL
    conn = psycopg2.connect(**db_params)
    
    # Créer un curseur
    cur = conn.cursor()
    
    # Exécuter une requête de test
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Connexion réussie à PostgreSQL!")
    print("Version du serveur:", version[0])
    
    # Fermer la communication avec la base de données
    cur.close()
    conn.close()
    
except Exception as e:
    print("Erreur de connexion à la base de données:", e)
