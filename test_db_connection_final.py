import psycopg2
import socket
import ssl
import sys
from urllib.parse import urlparse

def test_dns(hostname):
    """Teste la résolution DNS d'un nom d'hôte"""
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ Résolution DNS réussie pour {hostname} -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ Échec de la résolution DNS pour {hostname}: {e}")
        print("   Vérifiez votre connexion Internet et vos paramètres DNS.")
        print("   Essayez de modifier vos serveurs DNS pour utiliser 8.8.8.8 (Google) ou 1.1.1.1 (Cloudflare).")
        return False

def test_port(hostname, port, timeout=5):
    """Teste si un port est accessible sur un hôte"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((hostname, port))
            if result == 0:
                print(f"✅ Le port {port} est accessible sur {hostname}")
                return True
            else:
                print(f"❌ Le port {port} n'est pas accessible sur {hostname} (code: {result})")
                return False
    except Exception as e:
        print(f"❌ Erreur lors du test du port {port} sur {hostname}: {e}")
        return False

def test_db_connection():
    """Teste la connexion à la base de données Supabase"""
    # Paramètres de connexion
    db_params = {
        'dbname': 'coursdb',
        'user': 'postgres',
        'password': 'Senegale1228/',
        'host': 'db.xsepgmurvwguoygdmlza.supabase.co',
        'port': 5432,
        'sslmode': 'require',
        'connect_timeout': 10
    }
    
    print("\n🔍 Test de connexion à Supabase PostgreSQL")
    print("=" * 50)
    
    # 1. Test de résolution DNS
    print("\n1. Test de résolution DNS...")
    if not test_dns(db_params['host']):
        print("\n❌ Impossible de continuer sans résolution DNS.")
        return
    
    # 2. Test de connexion au port
    print("\n2. Test de connexion au port...")
    if not test_port(db_params['host'], db_params['port']):
        print("\n❌ Impossible de se connecter au port de la base de données.")
        print("   Vérifiez votre pare-feu et que votre IP est autorisée dans les paramètres Supabase.")
        return
    
    # 3. Test de connexion à la base de données
    print("\n3. Test de connexion à la base de données...")
    try:
        # Créer un contexte SSL personnalisé
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Établir la connexion avec SSL
        conn = psycopg2.connect(
            dbname=db_params['dbname'],
            user=db_params['user'],
            password=db_params['password'],
            host=db_params['host'],
            port=db_params['port'],
            sslmode=db_params['sslmode'],
            sslrootcert=None,
            sslcert=None,
            sslkey=None,
            sslcrl=None,
            sslsni=0,
            ssl_min_protocol_version=None,
            ssl_max_protocol_version=None,
            ssl_compression=False,
            ssl_context=ssl_context,
            connect_timeout=db_params['connect_timeout']
        )
        
        # Tester la connexion
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"✅ Connexion réussie à PostgreSQL!")
            print(f"   Version du serveur: {version[0]}")
            
            # Lister les tables
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = cur.fetchall()
            print("\n📋 Tables dans la base de données:")
            for table in tables:
                print(f"   - {table[0]}")
            
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        print("\n🔧 Solutions possibles:")
        print("1. Vérifiez que l'hôte et le port sont corrects")
        print("2. Vérifiez vos identifiants de connexion")
        print("3. Vérifiez que votre adresse IP est autorisée dans les paramètres de Supabase")
        print("4. Vérifiez votre connexion Internet et votre pare-feu")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔄 Démarrage du test de connexion à Supabase...")
    test_db_connection()
    print("\n✅ Test terminé!")
