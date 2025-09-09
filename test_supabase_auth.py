import os
from supabase import create_client, Client

# Récupérer les variables d'environnement
url = "https://xsepgmurvwguoygdmlza.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhzZXBnbXVydndndW95Z2RtbHphIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTczMzg5OTUsImV4cCI6MjA3MjkxNDk5NX0.HxQ8bXr0JyfvB7U9hP1EHC1tj-twgrqN5q1hn4Te2Sg"

def test_supabase_connection():
    try:
        print(f"🔗 Tentative de connexion à Supabase...")
        print(f"URL: {url}")
        
        # Créer le client Supabase
        supabase: Client = create_client(url, key)
        
        # Tester une requête simple
        response = supabase.table('filiere').select("*").limit(1).execute()
        
        print("✅ Connexion réussie à Supabase!")
        print(f"Données récupérées: {response.data}")
        
    except Exception as e:
        print(f"❌ Erreur de connexion à Supabase: {str(e)}")
        print("\n🔧 Vérifiez que:")
        print("1. Votre projet Supabase est actif")
        print("2. L'URL et la clé sont correctes")
        print("3. Votre adresse IP est autorisée dans les règles de sécurité")
        print("4. Votre connexion Internet est stable")

if __name__ == "__main__":
    test_supabase_connection()
