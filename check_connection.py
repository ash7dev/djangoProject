import psycopg2
from psycopg2 import OperationalError

def check_connection():
    try:
        # Paramètres de connexion
        conn_params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'Senegale1228/',
            'host': 'db.zxyxyemjtllphzrqdplk.supabase.co',
            'port': '5432',
            'sslmode': 'require'
        }
        
        print("🔄 Tentative de connexion à la base de données...")
        print(f"Hôte: {conn_params['host']}")
        print(f"Base de données: {conn_params['dbname']}")
        
        # Établir la connexion
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Exécuter une requête simple
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("✅ Connexion réussie!")
        print(f"Version du serveur PostgreSQL: {version[0]}")
        
        # Fermer la connexion
        cursor.close()
        conn.close()
        
    except OperationalError as e:
        print("❌ Erreur de connexion à la base de données:")
        print(str(e))
        print("\nVérifiez que:")
        print("1. Votre connexion Internet est active")
        print("2. L'hôte et le port sont corrects")
        print("3. Vos identifiants sont valides")
        print("4. Votre adresse IP est autorisée dans les paramètres Supabase")
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")

if __name__ == "__main__":
    check_connection()
