import uuid  # Importe le module uuid pour générer des identifiants uniques
from datetime import datetime  # Importe datetime (ici non utilisé, mais utile pour gérer les dates)
from .gestion_fichier import (
    charger_tous_trajets,      # Fonction pour charger tous les trajets depuis le stockage
    sauvegarder_trajets,       # Fonction pour sauvegarder la liste des trajets
    charger_utilisateurs,       # Fonction pour charger tous les utilisateurs
    sauvegarder_utilisateurs    # Fonction pour sauvegarder la liste des utilisateurs
)

def ajouter_trajet(trajet_data):
    """Ajoute un nouveau trajet"""
    trajets = charger_tous_trajets()  # Charge la liste actuelle des trajets
    
    # Crée un dictionnaire pour le nouveau trajet
    nouveau_trajet = {
        'id': str(uuid.uuid4()),                  # Génère un identifiant unique pour le trajet
        'conducteur_id': trajet_data['conducteur_id'],   # ID du conducteur
        'conducteur_nom': trajet_data['conducteur_nom'], # Nom du conducteur
        'ville_depart': trajet_data['ville_depart'],     # Ville de départ
        'ville_arrivee': trajet_data['ville_arrivee'],   # Ville d'arrivée
        'date': trajet_data['date'],                     # Date du trajet
        'heure': trajet_data['heure'],                   # Heure du trajet
        'places': trajet_data['places'],                 # Nombre de places disponibles
        'passagers': []                                 # Liste vide de passagers au départ
    }
    
    trajets.append(nouveau_trajet)  # Ajoute le nouveau trajet à la liste
    sauvegarder_trajets(trajets)    # Sauvegarde la liste mise à jour des trajets
    
    # Ajouter le trajet à la liste des trajets de l'utilisateur conducteur
    utilisateurs = charger_utilisateurs()  # Charge la liste des utilisateurs
    for user in utilisateurs:
        if user['id'] == trajet_data['conducteur_id']:
            user['trajets'].append(nouveau_trajet['id'])  # Ajoute l'ID du trajet à l'utilisateur
            break
    
    sauvegarder_utilisateurs(utilisateurs)  # Sauvegarde la liste mise à jour des utilisateurs
    
    return nouveau_trajet  # Retourne le nouveau trajet créé

def modifier_trajet(trajet_id, new_data):
    """Modifie un trajet existant"""
    trajets = charger_tous_trajets()  # Charge la liste des trajets
    
    for trajet in trajets:
        if trajet['id'] == trajet_id:
            # Met à jour les champs du trajet avec les nouvelles données
            trajet.update({
                'ville_depart': new_data['ville_depart'],
                'ville_arrivee': new_data['ville_arrivee'],
                'date': new_data['date'],
                'heure': new_data['heure'],
                'places': new_data['places']
            })
            break  # Sort de la boucle une fois le trajet trouvé et modifié
    
    sauvegarder_trajets(trajets)  # Sauvegarde la liste mise à jour des trajets

def supprimer_trajet(trajet_id):
    """Supprime un trajet"""
    trajets = charger_tous_trajets()  # Charge la liste des trajets
    trajets = [t for t in trajets if t['id'] != trajet_id]  # Garde tous les trajets sauf celui à supprimer
    sauvegarder_trajets(trajets)  # Sauvegarde la nouvelle liste
    
    # Retirer le trajet de la liste des trajets des utilisateurs
    utilisateurs = charger_utilisateurs()  # Charge la liste des utilisateurs
    for user in utilisateurs:
        if trajet_id in user['trajets']:
            user['trajets'].remove(trajet_id)  # Enlève l'ID du trajet de la liste de l'utilisateur
    
    sauvegarder_utilisateurs(utilisateurs)  # Sauvegarde la liste mise à jour des utilisateurs

def rejoindre_trajet(trajet_id, user_id):
    """Permet à un utilisateur de rejoindre un trajet"""
    trajets = charger_tous_trajets()  # Charge la liste des trajets
    
    for trajet in trajets:
        if trajet['id'] == trajet_id:
            if user_id not in trajet['passagers']:
                trajet['passagers'].append(user_id)  # Ajoute l'utilisateur à la liste des passagers
            break  # Sort de la boucle une fois le trajet trouvé
    
    sauvegarder_trajets(trajets)  # Sauvegarde la liste mise à jour des trajets