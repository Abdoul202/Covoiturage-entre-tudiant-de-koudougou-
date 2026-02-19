import sqlite3
from pathlib import Path

# Chemin de la base de données
DATA_DIR = Path(__file__).parent.parent / 'data'
DB_FILE = DATA_DIR / 'covoiturage.db'

def initialiser_base_de_donnees():
    """Crée la base de données et les tables si elles n'existent pas."""
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Créer la table des utilisateurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        mot_de_passe TEXT NOT NULL
    )
    """)

    # Créer la table des trajets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trajets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        depart TEXT NOT NULL,
        destination TEXT NOT NULL,
        date_heure TEXT NOT NULL,
        places_totales INTEGER NOT NULL,
        conducteur_id INTEGER NOT NULL,
        FOREIGN KEY (conducteur_id) REFERENCES utilisateurs (id)
    )
    """)

    # Créer la table des passagers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passagers (
        trajet_id INTEGER NOT NULL,
        utilisateur_id INTEGER NOT NULL,
        PRIMARY KEY (trajet_id, utilisateur_id),
        FOREIGN KEY (trajet_id) REFERENCES trajets (id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id)
    )
    """)

    conn.commit()
    conn.close()

def get_connexion():
    """Retourne une connexion à la base de données."""
    return sqlite3.connect(DB_FILE)
