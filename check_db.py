import os
import django
from django.db import connection

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

try:
    # Tester la connexion à la base de données
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("Connexion réussie à PostgreSQL!")
        print("Version du serveur:", version[0])
        
        # Vérifier les tables existantes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print("\nTables existantes:")
        for table in tables:
            print("- ", table[0])
            
except Exception as e:
    print("Erreur de connexion à la base de données:", e)
