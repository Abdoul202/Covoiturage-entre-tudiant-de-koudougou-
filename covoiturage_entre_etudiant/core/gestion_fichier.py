import json  # Importe le module json pour lire et écrire des fichiers JSON
import os  # Importe os pour manipuler les fichiers et dossiers (ici peu utilisé)
from hashlib import sha256  # Importe sha256 pour hasher les mots de passe
from pathlib import Path  # Importe Path pour gérer les chemins de fichiers de façon moderne

# Chemins des fichiers
DATA_DIR = Path(__file__).parent.parent / 'data'  # Dossier "data" à la racine du projet
USERS_FILE = DATA_DIR / 'utilisateurs.json'  # Fichier des utilisateurs
TRAJETS_FILE = DATA_DIR / 'trajets.json'  # Fichier des trajets

def initialiser_fichiers():
    """Crée les fichiers et dossiers s'ils n'existent pas"""
    DATA_DIR.mkdir(exist_ok=True)  # Crée le dossier data s'il n'existe pas
    
    if not USERS_FILE.exists():
        USERS_FILE.write_text('[]', encoding='utf-8')  # Crée un fichier vide (liste JSON)
    
    if not TRAJETS_FILE.exists():
        TRAJETS_FILE.write_text('[]', encoding='utf-8')  # Crée un fichier vide (liste JSON)

def charger_utilisateurs():
    """Charge la liste des utilisateurs depuis le fichier JSON"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)  # Charge et retourne la liste des utilisateurs
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Retourne une liste vide si le fichier n'existe pas ou est corrompu

def sauvegarder_utilisateurs(utilisateurs):
    """Sauvegarde la liste des utilisateurs dans le fichier JSON"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(utilisateurs, f, indent=2, ensure_ascii=False)  # Écrit la liste dans le fichier

def charger_tous_trajets():
    """Charge tous les trajets depuis le fichier JSON"""
    try:
        with open(TRAJETS_FILE, 'r', encoding='utf-8') as f:
            trajets = json.load(f)  # Charge la liste des trajets
            
            # Ajouter le nom du conducteur pour chaque trajet
            utilisateurs = {u['id']: u['nom'] for u in charger_utilisateurs()}  # Dictionnaire id->nom
            for trajet in trajets:
                trajet['conducteur_nom'] = utilisateurs.get(trajet['conducteur_id'], 'Inconnu')  # Ajoute le nom
            
            return trajets  # Retourne la liste des trajets enrichie
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Retourne une liste vide si le fichier n'existe pas ou est corrompu

def charger_trajets_utilisateur(user_id):
    """Charge les trajets d'un utilisateur spécifique"""
    trajets = charger_tous_trajets()  # Charge tous les trajets
    return [
        t for t in trajets 
        if t['conducteur_id'] == user_id or user_id in t['passagers']  # Filtre : conducteur ou passager
    ]

def sauvegarder_trajets(trajets):
    """Sauvegarde la liste des trajets dans le fichier JSON"""
    with open(TRAJETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(trajets, f, indent=2, ensure_ascii=False)  # Écrit la liste dans le fichier

def hash_password(password):
    """Hash un mot de passe avec SHA-256"""
    return sha256(password.encode('utf-8')).hexdigest()  # Retourne le hash du mot de passe