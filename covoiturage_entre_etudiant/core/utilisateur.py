import uuid  # Importe le module uuid pour générer des identifiants uniques
from .gestion_fichier import (
    charger_utilisateurs,      # Fonction pour charger la liste des utilisateurs depuis le stockage
    sauvegarder_utilisateurs,  # Fonction pour sauvegarder la liste des utilisateurs
    hash_password              # Fonction pour hasher (chiffrer) les mots de passe
)

def authentifier_utilisateur(email, password):
    """Authentifie un utilisateur avec email et mot de passe"""
    utilisateurs = charger_utilisateurs()  # Charge tous les utilisateurs existants
    hashed_pw = hash_password(password)    # Hash le mot de passe fourni pour comparer

    # Parcourt tous les utilisateurs pour trouver une correspondance
    for user in utilisateurs:
        # Si l'email et le mot de passe hashé correspondent, retourne l'utilisateur
        if user['email'] == email and user['mot_de_passe'] == hashed_pw:
            return user

    # Si aucun utilisateur ne correspond, retourne None
    return None

def creer_utilisateur(nom, email, password):
    """Crée un nouvel utilisateur"""
    utilisateurs = charger_utilisateurs()  # Charge la liste actuelle des utilisateurs

    # Crée un dictionnaire pour le nouvel utilisateur
    nouveau_user = {
        'id': str(uuid.uuid4()),           # Génère un identifiant unique
        'nom': nom.strip(),                # Enlève les espaces autour du nom
        'email': email.strip(),            # Enlève les espaces autour de l'email
        'mot_de_passe': hash_password(password),  # Hash le mot de passe
        'trajets': []                      # Initialise la liste des trajets de l'utilisateur
    }

    utilisateurs.append(nouveau_user)      # Ajoute le nouvel utilisateur à la liste
    sauvegarder_utilisateurs(utilisateurs) # Sauvegarde la liste mise à jour

    return nouveau_user                    # Retourne le nouvel utilisateur créé