import psycopg2
import socket

def test_connection():
    # Paramètres de connexion
    db_params = {
        'dbname': 'coursdb',
        'user': 'postgres',
        'password': 'Senegale1',
        'host': 'db.xsepgmurvwguoygdmlza.supabase.co',
        'port': 5432,
        'sslmode': 'require'
    }
    
    print("Test de connexion à la base de données Supabase...")
    print(f"Hôte: {db_params['host']}")
    print(f"Port: {db_params['port']}")
    print(f"Base de données: {db_params['dbname']}")
    
    # Test de résolution DNS
    try:
        ip_address = socket.gethostbyname(db_params['host'])
        print(f"Résolution DNS réussie: {db_params['host']} -> {ip_address}")
    except socket.gaierror as e:
        print(f"Échec de la résolution DNS: {e}")
        print("Vérifiez votre connexion Internet et vos paramètres DNS.")
        print("Essayez de modifier vos serveurs DNS pour utiliser ceux de Google (8.8.8.8) ou Cloudflare (1.1.1.1).")
        return
    
    # Test de connexion
    try:
        print("\nTentative de connexion à la base de données...")
        conn = psycopg2.connect(**db_params)
        
        # Exécuter une requête de test
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print("\nConnexion réussie!")
            print("Version de PostgreSQL:", version[0])
            
            # Lister les tables
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = cur.fetchall()
            print("\nTables dans la base de données:")
            for table in tables:
                print(f"- {table[0]}")
        
        conn.close()
        
    except psycopg2.Error as e:
        print("\nErreur de connexion à la base de données:")
        print(f"Type d'erreur: {type(e).__name__}")
        print(f"Message d'erreur: {e}")
        
        # Détails supplémentaires pour le débogage
        print("\nDétails supplémentaires:")
        print("1. Vérifiez que l'hôte et le port sont corrects")
        print("2. Vérifiez vos identifiants de connexion")
        print("3. Vérifiez que votre adresse IP est autorisée dans les paramètres de Supabase")
        print("4. Vérifiez votre connexion Internet et votre pare-feu")

if __name__ == "__main__":
    test_connection()
