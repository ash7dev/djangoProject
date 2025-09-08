#!/usr/bin/env python
import os
import django
from datetime import date, time, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from cours.models import Filiere, Classe, Professeur, Matiere, Cours

def creer_donnees_test():
    print("🔄 CRÉATION DE DONNÉES DE TEST")
    print("=" * 50)
    
    try:
        # 0. Nettoyer la base de données
        print("\n0. 🧹 Nettoyage de la base de données...")
        Cours.objects.all().delete()
        Matiere.objects.all().delete()
        Professeur.objects.all().delete()
        Classe.objects.all().delete()
        Filiere.objects.all().delete()
        print("✅ Base de données nettoyée")
        
        # 1. Créer des Filières
        print("\n1. 🎓 Création des filières...")
        filiere_info = Filiere.objects.create(
            nom="Informatique",
            description="Formation en informatique et technologies"
        )
        filiere_math = Filiere.objects.create(
            nom="Mathématiques",
            description="Formation en mathématiques appliquées"
        )
        print(f"✅ Filières créées: {Filiere.objects.count()}")
        
        # 2. Créer des Classes
        print("\n2. 👥 Création des classes...")
        classe_l1_info = Classe.objects.create(
            nom="L1 Informatique",
            niveau="L1",
            effectif_max=40
        )
        classe_l1_info.filieres.add(filiere_info)
        
        classe_l2_info = Classe.objects.create(
            nom="L2 Informatique", 
            niveau="L2",
            effectif_max=35
        )
        classe_l2_info.filieres.add(filiere_info)
        
        classe_l1_math = Classe.objects.create(
            nom="L1 Mathématiques",
            niveau="L1",
            effectif_max=30
        )
        classe_l1_math.filieres.add(filiere_math)
        
        # Classe commune (peut appartenir à plusieurs filières)
        classe_commune = Classe.objects.create(
            nom="L1 Math-Info",
            niveau="L1",
            effectif_max=25
        )
        classe_commune.filieres.add(filiere_info, filiere_math)
        
        print(f"✅ Classes créées: {Classe.objects.count()}")
        
        # 3. Créer des Professeurs
        print("\n3. 👨‍🏫 Création des professeurs...")
        prof_durand = Professeur.objects.create(
            nom="Durand",
            prenom="Jean",
            email="jean.durand@univ.fr",
            specialite="Programmation",
            telephone="0123456789"
        )
        prof_martin = Professeur.objects.create(
            nom="Martin",
            prenom="Marie",
            email="marie.martin@univ.fr", 
            specialite="Mathématiques",
            telephone="0987654321"
        )
        prof_dupont = Professeur.objects.create(
            nom="Dupont",
            prenom="Pierre",
            email="pierre.dupont@univ.fr",
            specialite="Base de données",
            telephone="0555666777"
        )
        print(f"✅ Professeurs créés: {Professeur.objects.count()}")
        
        # 4. Créer des Matières
        print("\n4. 📚 Création des matières...")
        matiere_python = Matiere.objects.create(
            nom="Programmation Python",
            description="Introduction à la programmation Python",
            volume_horaire=30,
            professeur=prof_durand
        )
        matiere_math = Matiere.objects.create(
            nom="Algèbre linéaire",
            description="Cours d'algèbre linéaire",
            volume_horaire=25,
            professeur=prof_martin
        )
        matiere_bdd = Matiere.objects.create(
            nom="Base de données",
            description="Conception et gestion de bases de données",
            volume_horaire=35,
            professeur=prof_dupont
        )
        print(f"✅ Matières créées: {Matiere.objects.count()}")
        
        # 5. Créer des Cours
        print("\n5. 📅 Création des cours...")
        
        # Dates sécurisées
        aujourd_hui = date.today()
        demain = aujourd_hui + timedelta(days=1)
        apres_demain = aujourd_hui + timedelta(days=2)
        
        cours1 = Cours.objects.create(
            libelle="Introduction Python",
            classe=classe_l1_info,
            professeur=prof_durand,
            matiere=matiere_python,
            date=aujourd_hui,
            heure_debut=time(9, 0),
            heure_fin=time(11, 0),
            salle="SENGHOR",
            description="Premier cours de Python"
        )
        
        cours2 = Cours.objects.create(
            libelle="Algèbre linéaire - Cours 1",
            classe=classe_l1_math,
            professeur=prof_martin,
            matiere=matiere_math,
            date=aujourd_hui,
            heure_debut=time(14, 0),
            heure_fin=time(16, 0),
            salle="MANDELA",
            description="Introduction aux matrices"
        )
        
        cours3 = Cours.objects.create(
            libelle="Base de données - SQL",
            classe=classe_l2_info,
            professeur=prof_dupont,
            matiere=matiere_bdd,
            date=aujourd_hui,
            heure_debut=time(10, 0),
            heure_fin=time(12, 0),
            salle="KANE",
            description="Langage SQL"
        )
        
        # Cours pour demain
        cours4 = Cours.objects.create(
            libelle="Python - TP",
            classe=classe_l1_info,
            professeur=prof_durand,
            matiere=matiere_python,
            date=demain,
            heure_debut=time(13, 0),
            heure_fin=time(15, 0),
            salle="SECK",
            description="Travaux pratiques Python"
        )
        
        # Cours pour après-demain
        cours5 = Cours.objects.create(
            libelle="Mathématiques pour l'informatique",
            classe=classe_commune,
            professeur=prof_martin,
            matiere=matiere_math,
            date=apres_demain,
            heure_debut=time(8, 0),
            heure_fin=time(10, 0),
            salle="FAYE",
            description="Cours commun math-info"
        )
        
        print(f"✅ Cours créés: {Cours.objects.count()}")
        
        print("\n" + "=" * 50)
        print("🎉 DONNÉES DE TEST CRÉÉES AVEC SUCCÈS!")
        
        # Afficher un résumé
        print(f"\n📊 RÉSUMÉ:")
        print(f"   - Filières: {Filiere.objects.count()}")
        print(f"   - Classes: {Classe.objects.count()}")
        print(f"   - Professeurs: {Professeur.objects.count()}")
        print(f"   - Matières: {Matiere.objects.count()}")
        print(f"   - Cours: {Cours.objects.count()}")
        
        # Afficher les relations many-to-many
        print(f"\n🔗 RELATIONS MANY-TO-MANY:")
        for classe in Classe.objects.all():
            filieres = ", ".join([f.nom for f in classe.filieres.all()])
            print(f"   - {classe.nom}: {filieres}")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DE LA CRÉATION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    creer_donnees_test() 