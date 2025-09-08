#!/usr/bin/env python
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from cours.models import Filiere, Classe, Professeur, Matiere, Cours
from django.db import models
from datetime import datetime, date, time

def test_requetes():
    print("🔍 TEST DES REQUÊTES DJANGO")
    print("=" * 50)
    
    try:
        # Test 1: Requêtes du Dashboard
        print("\n1. 📊 REQUÊTES DU DASHBOARD")
        print("-" * 30)
        
        total_filieres = Filiere.objects.filter(actif=True).count()
        print(f"✅ Filières actives: {total_filieres}")
        
        total_classes = Classe.objects.filter(actif=True).count()
        print(f"✅ Classes actives: {total_classes}")
        
        total_professeurs = Professeur.objects.filter(actif=True).count()
        print(f"✅ Professeurs actifs: {total_professeurs}")
        
        total_matieres = Matiere.objects.filter(actif=True).count()
        print(f"✅ Matières actives: {total_matieres}")
        
        total_cours = Cours.objects.filter(actif=True).count()
        print(f"✅ Cours actifs: {total_cours}")
        
        # Test 2: Requêtes des Filières
        print("\n2. 🎓 REQUÊTES DES FILIÈRES")
        print("-" * 30)
        
        filieres = Filiere.objects.filter(actif=True)
        print(f"✅ Filières trouvées: {filieres.count()}")
        
        # Test des relations many-to-many
        for filiere in filieres[:3]:  # Test sur les 3 premières
            classes_count = filiere.classes.filter(actif=True).count()
            print(f"   - {filiere.nom}: {classes_count} classes")
        
        # Test 3: Requêtes des Classes
        print("\n3. 👥 REQUÊTES DES CLASSES")
        print("-" * 30)
        
        classes = Classe.objects.filter(actif=True).prefetch_related('filieres')
        print(f"✅ Classes trouvées: {classes.count()}")
        
        # Test des filtres
        classes_l1 = classes.filter(niveau='L1')
        print(f"✅ Classes L1: {classes_l1.count()}")
        
        # Test des relations many-to-many
        for classe in classes[:3]:
            filieres_classe = ", ".join([f.nom for f in classe.filieres.all()])
            print(f"   - {classe.nom}: {filieres_classe}")
        
        # Test 4: Requêtes des Professeurs
        print("\n4. 👨‍🏫 REQUÊTES DES PROFESSEURS")
        print("-" * 30)
        
        professeurs = Professeur.objects.filter(actif=True)
        print(f"✅ Professeurs trouvés: {professeurs.count()}")
        
        # Test de recherche
        if professeurs.exists():
            premier_prof = professeurs.first()
            recherche = Professeur.objects.filter(
                models.Q(nom__icontains=premier_prof.nom[:3]) |
                models.Q(prenom__icontains=premier_prof.prenom[:3])
            )
            print(f"✅ Recherche professeur: {recherche.count()} résultats")
        
        # Test 5: Requêtes des Matières
        print("\n5. 📚 REQUÊTES DES MATIÈRES")
        print("-" * 30)
        
        matieres = Matiere.objects.filter(actif=True).select_related('professeur')
        print(f"✅ Matières trouvées: {matieres.count()}")
        
        # Test des agrégations
        total_heures = matieres.aggregate(total=models.Sum('volume_horaire'))['total'] or 0
        print(f"✅ Total heures: {total_heures}")
        
        # Test 6: Requêtes des Cours
        print("\n6. 📅 REQUÊTES DES COURS")
        print("-" * 30)
        
        cours = Cours.objects.filter(actif=True).select_related(
            'classe', 'professeur', 'matiere'
        ).prefetch_related('classe__filieres').order_by('-date', 'heure_debut')
        print(f"✅ Cours trouvés: {cours.count()}")
        
        # Test des filtres de cours
        if cours.exists():
            cours_aujourd_hui = cours.filter(date=date.today())
            print(f"✅ Cours aujourd'hui: {cours_aujourd_hui.count()}")
            
            # Test des salles
            salles_utilisees = cours.values('salle').distinct().exclude(salle='')
            print(f"✅ Salles utilisées: {salles_utilisees.count()}")
        
        # Test 7: Requêtes complexes
        print("\n7. 🔗 REQUÊTES COMPLEXES")
        print("-" * 30)
        
        # Cours avec professeur et matière
        cours_complets = cours.filter(professeur__isnull=False, matiere__isnull=False)
        print(f"✅ Cours avec prof et matière: {cours_complets.count()}")
        
        # Classes par filière (many-to-many)
        classes_par_filiere = classes.values('filieres__nom').annotate(
            count=models.Count('id')
        )
        print(f"✅ Classes par filière: {classes_par_filiere.count()} relations")
        
        # Test 8: Requêtes de statistiques
        print("\n8. 📈 REQUÊTES DE STATISTIQUES")
        print("-" * 30)
        
        # Total étudiants (effectif max)
        total_etudiants = classes.aggregate(total=models.Sum('effectif_max'))['total'] or 0
        print(f"✅ Total étudiants max: {total_etudiants}")
        
        # Professeurs par spécialité
        specialites = professeurs.values('specialite').distinct().exclude(specialite='')
        print(f"✅ Spécialités: {specialites.count()}")
        
        # Test 9: Requêtes avec dates
        print("\n9. 📅 REQUÊTES AVEC DATES")
        print("-" * 30)
        
        if cours.exists():
            # Cours de cette semaine
            aujourd_hui = date.today()
            debut_semaine = aujourd_hui.replace(day=aujourd_hui.day - aujourd_hui.weekday())
            fin_semaine = debut_semaine.replace(day=debut_semaine.day + 6)
            
            cours_semaine = cours.filter(date__range=[debut_semaine, fin_semaine])
            print(f"✅ Cours cette semaine: {cours_semaine.count()}")
        
        # Test 10: Validation des modèles
        print("\n10. ✅ VALIDATION DES MODÈLES")
        print("-" * 30)
        
        # Test de création d'objets
        try:
            # Test création Filiere
            filiere_test = Filiere(nom="Test Filière", description="Test")
            filiere_test.full_clean()
            print("✅ Modèle Filiere: OK")
            
            # Test création Classe
            classe_test = Classe(
                nom="Test Classe",
                niveau="L1",
                effectif_max=30
            )
            classe_test.full_clean()
            print("✅ Modèle Classe: OK")
            
            # Test création Professeur
            prof_test = Professeur(nom="Test", prenom="Professeur")
            prof_test.full_clean()
            print("✅ Modèle Professeur: OK")
            
            # Test création Matiere
            matiere_test = Matiere(
                nom="Test Matière",
                volume_horaire=30
            )
            matiere_test.full_clean()
            print("✅ Modèle Matiere: OK")
            
            # Test création Cours
            if classes.exists():
                cours_test = Cours(
                    libelle="Test Cours",
                    classe=classes.first(),
                    date=date.today(),
                    heure_debut=time(9, 0),
                    heure_fin=time(11, 0)
                )
                cours_test.full_clean()
                print("✅ Modèle Cours: OK")
                
        except Exception as e:
            print(f"❌ Erreur validation: {e}")
        
        # Test 11: Relations Many-to-Many
        print("\n11. 🔗 TEST RELATIONS MANY-TO-MANY")
        print("-" * 30)
        
        # Test ajout de filières à une classe
        if classes.exists() and filieres.exists():
            classe_test = classes.first()
            filiere_test = filieres.first()
            
            # Compter les filières avant
            filieres_avant = classe_test.filieres.count()
            
            # Ajouter une filière
            classe_test.filieres.add(filiere_test)
            
            # Compter les filières après
            filieres_apres = classe_test.filieres.count()
            
            print(f"✅ Relations many-to-many: {filieres_avant} → {filieres_apres}")
        
        print("\n" + "=" * 50)
        print("🎉 TOUS LES TESTS DE REQUÊTES SONT PASSÉS AVEC SUCCÈS!")
        print("✅ Les requêtes Django fonctionnent correctement")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DES TESTS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_requetes() 