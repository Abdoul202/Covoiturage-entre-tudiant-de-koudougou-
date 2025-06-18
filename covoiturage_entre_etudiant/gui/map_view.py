import tkinter as tk  # Importe le module principal de Tkinter pour l'interface graphique
from tkinter import ttk  # Importe les widgets améliorés de Tkinter (boutons, labels, etc.)
import webbrowser  # Permet d'ouvrir une page web dans le navigateur par défaut
import os  # Permet de manipuler les fichiers et chemins (pas utilisé ici mais souvent utile)
from core.carte import generer_carte_html  # Fonction pour générer le fichier HTML de la carte
from core.gestion_fichier import charger_tous_trajets  # Fonction pour charger tous les trajets

class MapViewWindow:
    def __init__(self, root, utilisateur):
        self.root = root  # Fenêtre principale de l'application
        self.utilisateur = utilisateur  # Dictionnaire avec les infos de l'utilisateur connecté
        
        # Créer une fenêtre Toplevel (nouvelle fenêtre indépendante)
        self.window = tk.Toplevel(self.root)
        self.window.title("Carte des Trajets - Koudougou")  # Titre de la fenêtre
        self.window.geometry("900x600")  # Taille de la fenêtre
        
        # Frame principale pour organiser les widgets
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Charger tous les trajets depuis le fichier ou la base de données
        trajets = charger_tous_trajets()
        
        # Générer le fichier HTML pour la carte avec tous les trajets
        html_file = generer_carte_html(trajets)
        
        # Ouvrir le fichier HTML dans le navigateur par défaut (new=2 = nouvel onglet)
        webbrowser.open(f'file://{html_file}', new=2)
        
        # Afficher un message d'information dans la fenêtre
        ttk.Label(
            self.main_frame, 
            text="La carte des trajets a été ouverte dans votre navigateur par défaut.",
            font=('Helvetica', 12)
        ).pack(expand=True)
        
        # Bouton pour fermer la fenêtre de la carte
        ttk.Button(
            self.main_frame,
            text="Fermer",
            command=self.window.destroy,
            style='danger.TButton'
        ).pack(pady=20)