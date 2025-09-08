#!/usr/bin/env python3
"""
Script de nettoyage pour Vercel.
Supprime les fichiers inutiles en production pour réduire la taille du déploiement.
"""
import os
import shutil
from pathlib import Path

def clean_unnecessary_files():
    """Supprime les fichiers inutiles pour la production."""
    base_dir = Path(__file__).parent
    
    # Dossiers à conserver
    keep_dirs = {
        'monprojet',  # Fichiers du projet
        'cours',      # Application principale
        'static',     # Fichiers statiques
        'templates',  # Templates HTML
    }
    
    # Fichiers à conserver
    keep_files = {
        'manage.py',
        'requirements.txt',
        'vercel.json',
        'vercel_build.sh',
        'runtime.txt',
        'Procfile',
    }
    
    # Supprimer les dossiers inutiles
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        
        # Ne pas supprimer les dossiers importants
        if item in keep_dirs or item in keep_files:
            continue
            
        # Supprimer les dossiers de développement
        if os.path.isdir(item_path):
            if item.endswith(('__pycache__', '.git', 'venv', 'env', '.github')):
                print(f"Suppression du dossier: {item}")
                shutil.rmtree(item_path, ignore_errors=True)
        # Supprimer les fichiers inutiles
        elif os.path.isfile(item_path):
            if item.endswith(('.pyc', '.pyo', '.pyd', '.so', '.o', '.a')):
                print(f"Suppression du fichier: {item}")
                os.remove(item_path)

if __name__ == "__main__":
    clean_unnecessary_files()
