# Covoiturage-entre-tudiant-de-koudougou-

## Fonctionnalités

* **Authentification Utilisateur**:
    * Connexion pour les utilisateurs existants.
    * Inscription de nouveaux utilisateurs avec vérification de l'email et du mot de passe.
    * Hashage des mots de passe pour la sécurité.
* **Gestion des Trajets**:
    * Affichage de "Mes Trajets" (où l'utilisateur est conducteur ou passager).
    * Affichage de "Tous les Trajets" disponibles.
    * Ajout de nouveaux trajets avec détails (ville de départ, d'arrivée, date, heure, places).
    * Modification des trajets existants (uniquement par le conducteur).
    * Suppression des trajets (uniquement par le conducteur).
    * Rejoindre un trajet en tant que passager (avec vérification des places et de la participation).
* **Visualisation Cartographique**:
    * Génération d'une carte HTML interactive affichant tous les trajets, ouverte dans le navigateur par défaut.
* **Gestion des Données**:
    * Stockage des utilisateurs et des trajets dans des fichiers JSON (`utilisateurs.json`, `trajets.json`).
    * Initialisation automatique des fichiers de données si non existants.

## Structure du Projet

```
.
├── core/
│ 
│   ├── carte.py              # Logique pour la génération de la carte HTML.
│   ├── gestion_fichier.py    # Fonctions de lecture/écriture des fichiers JSON (utilisateurs, trajets).
│   ├── trajet.py             # Fonctions pour gérer les trajets (ajouter, modifier, supprimer, rejoindre).
│   └── utilisateur.py        # Fonctions pour l'authentification et la création d'utilisateurs.
├── gui/
│   
│   ├── dashboard.py          # Interface du tableau de bord principal après connexion.
│   ├── edit_trajet.py        # Fenêtre pour ajouter/modifier un trajet.
│   ├── login.py              # Fenêtre de connexion et d'inscription.
│   └── map_view.py           # Fenêtre pour l'affichage de la carte.
├── web/
│   ├── carte.html            # Modèle HTML pour la carte Leaflet.
│  
├── data/                     # Dossier pour les fichiers de données JSON (créé automatiquement).
│   ├── trajets.json
│   └── utilisateurs.json
└── main.py                   # Point d'entrée principal de l'application.
```

## Technologies Utilisées

* **Python 3.x**
* **Tkinter**: Pour l'interface utilisateur graphique.
* **ttkbootstrap**: Un thème Tkinter pour un look moderne et personnalisable.
* **`json`**: Pour la persistance des données.
* **`hashlib` (SHA-256)**: Pour le hachage sécurisé des mots de passe.
* **`uuid`**: Pour la génération d'identifiants uniques.
* **`datetime`**: Pour la gestion des dates et heures.
* **`webbrowser`**: Pour ouvrir la carte HTML dans le navigateur par défaut.
* **Leaflet.js (via `carte.html`)**: Bibliothèque JavaScript pour les cartes interactives (présumée utilisée dans `carte.html`).

## Installation et Lancement

Pour lancer l'application, suivez les étapes ci-dessous :

1.  **Cloner le dépôt** (si applicable) ou télécharger les fichiers du projet.

2.  **Installer les dépendances Python**:
    Assurez-vous d'avoir `tkinter` (généralement inclus avec Python) et `ttkbootstrap`.
    ```bash
    pip install ttkbootstrap
    ```

3.  **Lancer l'application**:
    Exécutez le fichier `main.py` depuis votre terminal :
    ```bash
    python main.py
    ```

L'application s'ouvrira sur la fenêtre de connexion/inscription.

## Utilisation

1.  **Inscription**: Si vous êtes un nouvel utilisateur, naviguez vers l'onglet "Inscription", remplissez les informations requises et cliquez sur "S'inscrire".
2.  **Connexion**: Utilisez votre email et mot de passe pour vous connecter.
3.  **Tableau de Bord**: Une fois connecté, vous accéderez au tableau de bord.
    * Utilisez les boutons de la barre latérale pour naviguer entre "Mes Trajets", "Tous les Trajets", "Ajouter un Trajet", et "Voir sur la Carte".
    * Sélectionnez un trajet dans la liste pour utiliser les boutons "Rejoindre", "Modifier" ou "Supprimer".
4.  **Ajouter un Trajet**: Cliquez sur "Ajouter un Trajet", remplissez les détails et enregistrez.
5.  **Rejoindre un Trajet**: Sélectionnez un trajet (non le vôtre) et cliquez sur "Rejoindre".
6.  **Voir sur la Carte**: Cliquez sur "Voir sur la Carte" pour ouvrir une page web affichant tous les trajets sur une carte interactive.
7.  **Déconnexion**: Cliquez sur "Déconnexion" pour revenir à l'écran de connexion.

