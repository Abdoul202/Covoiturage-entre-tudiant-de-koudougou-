import sqlite3
from hashlib import sha256
from .database import get_connexion

class PersistenceError(Exception):
    """Exception de base pour les erreurs de persistance."""
    pass

class UserExistsError(PersistenceError):
    """Exception levée lorsqu'un utilisateur existe déjà."""
    pass

def hash_password(password):
    """Hash un mot de passe avec SHA-256."""
    return sha256(password.encode('utf-8')).hexdigest()

def get_user_by_email(email):
    """Récupère un utilisateur par son email."""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM utilisateurs WHERE email = ?", (email,))
        return cursor.fetchone()
    finally:
        conn.close()

def creer_utilisateur(nom, email, mot_de_passe):
    """Crée un nouvel utilisateur dans la base de données."""
    if get_user_by_email(email):
        raise UserExistsError("Un utilisateur avec cet email existe déjà.")

    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO utilisateurs (nom, email, mot_de_passe) VALUES (?, ?, ?)",
            (nom, email, hash_password(mot_de_passe))
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise PersistenceError(f"Erreur d'intégrité de la base de données: {e}")
    finally:
        conn.close()

def authentifier_utilisateur(email, mot_de_passe):
    """Authentifie un utilisateur."""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM utilisateurs WHERE email = ? AND mot_de_passe = ?",
            (email, hash_password(mot_de_passe))
        )
        user = cursor.fetchone()
        if user:
            return {'id': user[0], 'nom': user[1], 'email': user[2]}
        return None
    finally:
        conn.close()

def charger_utilisateurs():
    """Charge tous les utilisateurs de la base de données."""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nom, email FROM utilisateurs")
        return [{'id': row[0], 'nom': row[1], 'email': row[2]} for row in cursor.fetchall()]
    finally:
        conn.close()

def charger_tous_trajets():
    """Charge tous les trajets de la base de données."""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.id, t.depart, t.destination, t.date_heure, t.places_totales, t.conducteur_id, u.nom,
                   (SELECT COUNT(*) FROM passagers WHERE trajet_id = t.id) as passagers_inscrits
            FROM trajets t
            JOIN utilisateurs u ON t.conducteur_id = u.id
        """)
        trajets = []
        for row in cursor.fetchall():
            trajets.append({
                'id': row[0],
                'depart': row[1],
                'destination': row[2],
                'date_heure': row[3],
                'places_disponibles': row[4] - row[7],
                'places_totales': row[4],
                'conducteur_id': row[5],
                'conducteur_nom': row[6],
                'passagers': []
            })
        return trajets
    finally:
        conn.close()

def charger_trajets_utilisateur(user_id):
    """Charge les trajets d'un utilisateur spécifique (conducteur ou passager)."""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.id, t.depart, t.destination, t.date_heure, t.places_totales, t.conducteur_id, u.nom,
                   (SELECT COUNT(*) FROM passagers WHERE trajet_id = t.id) as passagers_inscrits
            FROM trajets t
            JOIN utilisateurs u ON t.conducteur_id = u.id
            WHERE t.conducteur_id = ? OR t.id IN (SELECT trajet_id FROM passagers WHERE utilisateur_id = ?)
        """, (user_id, user_id))
        trajets = []
        for row in cursor.fetchall():
            trajets.append({
                'id': row[0],
                'depart': row[1],
                'destination': row[2],
                'date_heure': row[3],
                'places_disponibles': row[4] - row[7],
                'places_totales': row[4],
                'conducteur_id': row[5],
                'conducteur_nom': row[6],
                'passagers': []
            })
        return trajets
    finally:
        conn.close()

def creer_trajet(depart, destination, date_heure, places, conducteur_id):
    """Crée un nouveau trajet."""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO trajets (depart, destination, date_heure, places_totales, conducteur_id) VALUES (?, ?, ?, ?, ?)",
            (depart, destination, date_heure, places, conducteur_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        raise PersistenceError(f"Erreur lors de la création du trajet: {e}")
    finally:
        conn.close()

def modifier_trajet(trajet_id, depart, destination, date_heure, places):
    """Modifie un trajet existant."""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE trajets SET depart = ?, destination = ?, date_heure = ?, places_totales = ? WHERE id = ?",
            (depart, destination, date_heure, places, trajet_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        raise PersistenceError(f"Erreur lors de la modification du trajet: {e}")
    finally:
        conn.close()

def rejoindre_trajet(trajet_id, utilisateur_id):
    """Ajoute un passager à un trajet."""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO passagers (trajet_id, utilisateur_id) VALUES (?, ?)", (trajet_id, utilisateur_id))
        conn.commit()
    except sqlite3.IntegrityError:
        raise PersistenceError("Vous avez déjà rejoint ce trajet.")
    except sqlite3.Error as e:
        raise PersistenceError(f"Erreur lors de la jointure du trajet: {e}")
    finally:
        conn.close()

def supprimer_trajet(trajet_id):
    """Supprime un trajet de la base de données."""
    conn = get_connexion()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM passagers WHERE trajet_id = ?", (trajet_id,))
        cursor.execute("DELETE FROM trajets WHERE id = ?", (trajet_id,))
        conn.commit()
    except sqlite3.Error as e:
        raise PersistenceError(f"Erreur lors de la suppression du trajet: {e}")
    finally:
        conn.close()
