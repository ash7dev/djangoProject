#!/usr/bin/env python
import os
import django
from datetime import date, time

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from cours.models import Filiere, Classe, Professeur, Matiere, Cours

def verifier_et_corriger_donnees():
    print("🔍 VÉRIFICATION ET CORRECTION DES DONNÉES")
    print("=" * 50)
    
    try:
        # 1. Vérifier les données existantes
        print("\n1. 📊 ÉTAT ACTUEL DE LA BASE:")
        print(f"   - Filières: {Filiere.objects.count()}")
        print(f"   - Classes: {Classe.objects.count()}")
        print(f"   - Professeurs: {Professeur.objects.count()}")
        print(f"   - Matières: {Matiere.objects.count()}")
        print(f"   - Cours: {Cours.objects.count()}")
        
        # 2. Vérifier les relations many-to-many
        print("\n2. 🔗 VÉRIFICATION DES RELATIONS:")
        
        # Vérifier les filières
        filieres = Filiere.objects.all()
        for filiere in filieres:
            classes_count = filiere.classes.count()
            print(f"   - {filiere.nom}: {classes_count} classes")
        
        # Vérifier les classes
        classes = Classe.objects.all()
        for classe in classes:
            filieres_count = classe.filieres.count()
            print(f"   - {classe.nom}: {filieres_count} filières")
        
        # 3. Corriger les relations manquantes
        print("\n3. 🔧 CORRECTION DES RELATIONS:")
        
        # Récupérer ou créer les filières
        filiere_info, created = Filiere.objects.get_or_create(
            nom="Informatique",
            defaults={"description": "Formation en informatique et technologies"}
        )
        if created:
            print(f"   ✅ Filière 'Informatique' créée")
        else:
            print(f"   ℹ️  Filière 'Informatique' existe déjà")
            
        filiere_math, created = Filiere.objects.get_or_create(
            nom="Mathématiques",
            defaults={"description": "Formation en mathématiques appliquées"}
        )
        if created:
            print(f"   ✅ Filière 'Mathématiques' créée")
        else:
            print(f"   ℹ️  Filière 'Mathématiques' existe déjà")
        
        # Corriger les relations des classes
        for classe in classes:
            if "informatique" in classe.nom.lower():
                if filiere_info not in classe.filieres.all():
                    classe.filieres.add(filiere_info)
                    print(f"   ✅ Ajouté filière 'Informatique' à {classe.nom}")
            elif "mathématique" in classe.nom.lower():
                if filiere_math not in classe.filieres.all():
                    classe.filieres.add(filiere_math)
                    print(f"   ✅ Ajouté filière 'Mathématiques' à {classe.nom}")
            elif "math-info" in classe.nom.lower():
                if filiere_info not in classe.filieres.all():
                    classe.filieres.add(filiere_info)
                if filiere_math not in classe.filieres.all():
                    classe.filieres.add(filiere_math)
                print(f"   ✅ Ajouté filières 'Informatique' et 'Mathématiques' à {classe.nom}")
        
        # 4. Vérifier les cours
        print("\n4. 📅 VÉRIFICATION DES COURS:")
        cours = Cours.objects.all()
        if cours.exists():
            print(f"   - {cours.count()} cours existent")
            for c in cours[:3]:  # Afficher les 3 premiers
                print(f"     • {c.libelle} - {c.classe.nom} - {c.date}")
        else:
            print("   - Aucun cours trouvé")
            
            # Créer quelques cours de test si possible
            if classes.exists() and Professeur.objects.exists() and Matiere.objects.exists():
                print("   🔧 Création de cours de test...")
                classe = classes.first()
                professeur = Professeur.objects.first()
                matiere = Matiere.objects.first()
                
                cours_test = Cours.objects.create(
                    libelle="Cours de test",
                    classe=classe,
                    professeur=professeur,
                    matiere=matiere,
                    date=date.today(),
                    heure_debut=time(9, 0),
                    heure_fin=time(11, 0),
                    salle="SENGHOR",
                    description="Cours de test créé automatiquement"
                )
                print(f"   ✅ Cours de test créé: {cours_test.libelle}")
        
        # 5. Résumé final
        print("\n5. 📋 RÉSUMÉ FINAL:")
        print(f"   - Filières: {Filiere.objects.count()}")
        print(f"   - Classes: {Classe.objects.count()}")
        print(f"   - Professeurs: {Professeur.objects.count()}")
        print(f"   - Matières: {Matiere.objects.count()}")
        print(f"   - Cours: {Cours.objects.count()}")
        
        # Afficher les relations finales
        print(f"\n🔗 RELATIONS FINALES:")
        for classe in Classe.objects.all():
            filieres = ", ".join([f.nom for f in classe.filieres.all()])
            print(f"   - {classe.nom}: {filieres}")
        
        print("\n" + "=" * 50)
        print("🎉 VÉRIFICATION ET CORRECTION TERMINÉES!")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verifier_et_corriger_donnees() 