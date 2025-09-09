import psycopg2
from urllib.parse import urlparse

def test_connection():
    # URL de connexion complète (format correct avec deux-points avant le mot de passe)
    db_url = "postgresql://postgres:Senegale1228@db.xsepgmurvwguoygdmlza.supabase.co:5432/coursdb"
    
    try:
        # Parser l'URL
        result = urlparse(db_url)
        
        # Extraire les informations de connexion
        username = result.username
        password = result.password
        database = result.path[1:]  # Enlever le slash initial
        hostname = result.hostname
        port = result.port
        
        print(f"Tentative de connexion à {hostname}:{port}/{database}...")
        
        # Établir la connexion
        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=hostname,
            port=port,
            sslmode='require'
        )
        
        # Tester la connexion
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        
        print("Connexion réussie!")
        print("Version de PostgreSQL:", version[0])
        
        # Nettoyage
        cur.close()
        conn.close()
        
    except Exception as e:
        print("Erreur de connexion:")
        print(f"Type d'erreur: {type(e).__name__}")
        print(f"Message d'erreur: {e}")
        print("\nDétails de la configuration:")
        print(f"URL: {db_url}")
        print(f"Host: {hostname}")
        print(f"Port: {port}")
        print(f"Database: {database}")
        print(f"User: {username}")
        
        # Vérifier la résolution DNS
        import socket
        try:
            ip = socket.gethostbyname(hostname)
            print(f"\nRésolution DNS réussie pour {hostname} -> {ip}")
        except socket.gaierror as e:
            print(f"\nÉchec de la résolution DNS pour {hostname}: {e}")
        
        # Vérifier la connectivité réseau
        import subprocess
        try:
            print("\nTest de ping...")
            subprocess.run(["ping", "-c", "4", hostname], check=True)
        except subprocess.CalledProcessError:
            print("Le ping a échoué. Problème de connectivité réseau.")

if __name__ == "__main__":
    test_connection()
