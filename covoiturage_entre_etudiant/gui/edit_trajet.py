import tkinter as tk  # Importe le module principal de Tkinter pour l'interface graphique
from tkinter import ttk  # Importe les widgets améliorés de Tkinter (boutons, labels, etc.)
from tkinter import messagebox  # Importe les boîtes de dialogue pour afficher des messages à l'utilisateur
from datetime import datetime  # Importe la classe datetime pour valider les dates et heures
from core.trajet import ajouter_trajet, modifier_trajet  # Importe les fonctions pour ajouter ou modifier un trajet

class EditTrajetWindow:
    def __init__(self, root, utilisateur, trajet=None, callback=None):
        self.root = root  # Fenêtre principale de l'application
        self.utilisateur = utilisateur  # Dictionnaire avec les infos de l'utilisateur connecté
        self.trajet = trajet  # Dictionnaire du trajet à modifier, ou None si c'est un ajout
        self.callback = callback  # Fonction à appeler après ajout/modification
        
        # Créer une nouvelle fenêtre (Toplevel) indépendante de la fenêtre principale
        self.window = tk.Toplevel(self.root)
        # Définit le titre de la fenêtre selon si on ajoute ou modifie
        self.window.title("Nouveau Trajet" if not trajet else "Modifier Trajet")
        self.window.geometry("500x400")  # Définit la taille de la fenêtre
        
        # Crée un cadre principal avec du padding
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        self.creer_formulaire()  # Crée les champs du formulaire
    
    def creer_formulaire(self):
        # Champ pour la ville de départ
        ttk.Label(self.main_frame, text="Ville de départ:").pack(pady=(10, 0))
        self.depart_entry = ttk.Entry(self.main_frame)
        self.depart_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Champ pour la ville d'arrivée
        ttk.Label(self.main_frame, text="Ville d'arrivée:").pack()
        self.arrivee_entry = ttk.Entry(self.main_frame)
        self.arrivee_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Champ pour la date
        ttk.Label(self.main_frame, text="Date (AAAA-MM-JJ):").pack()
        self.date_entry = ttk.Entry(self.main_frame)
        self.date_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Champ pour l'heure
        ttk.Label(self.main_frame, text="Heure (HH:MM):").pack()
        self.heure_entry = ttk.Entry(self.main_frame)
        self.heure_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Champ pour le nombre de places disponibles (spinbox)
        ttk.Label(self.main_frame, text="Places disponibles:").pack()
        self.places_spinbox = ttk.Spinbox(self.main_frame, from_=1, to=10)
        self.places_spinbox.pack(fill=tk.X, pady=(0, 20))
        
        # Cadre pour les boutons Annuler et Enregistrer
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X)
        
        # Bouton Annuler : ferme la fenêtre sans rien faire
        ttk.Button(
            button_frame, 
            text="Annuler", 
            command=self.window.destroy,
            style='danger.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Bouton Enregistrer : lance la méthode enregistrer
        ttk.Button(
            button_frame, 
            text="Enregistrer", 
            command=self.enregistrer,
            style='success.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        # Si on modifie un trajet, pré-remplit les champs avec les valeurs existantes
        if self.trajet:
            self.depart_entry.insert(0, self.trajet['ville_depart'])
            self.arrivee_entry.insert(0, self.trajet['ville_arrivee'])
            self.date_entry.insert(0, self.trajet['date'])
            self.heure_entry.insert(0, self.trajet['heure'])
            self.places_spinbox.set(self.trajet['places'])
    
    def enregistrer(self):
        # Récupère les valeurs saisies dans les champs
        depart = self.depart_entry.get().strip()
        arrivee = self.arrivee_entry.get().strip()
        date = self.date_entry.get().strip()
        heure = self.heure_entry.get().strip()
        places = self.places_spinbox.get().strip()
        
        # Vérifie que tous les champs sont remplis
        if not all([depart, arrivee, date, heure, places]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        # Vérifie que le nombre de places est un entier entre 1 et 10
        try:
            places = int(places)
            if places < 1 or places > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Le nombre de places doit être entre 1 et 10")
            return
        
        # Vérifie que la date est au bon format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide (AAAA-MM-JJ requis)")
            return
        
        # Vérifie que l'heure est au bon format
        try:
            datetime.strptime(heure, "%H:%M")
        except ValueError:
            messagebox.showerror("Erreur", "Format d'heure invalide (HH:MM requis)")
            return
        
        # Prépare les données du trajet sous forme de dictionnaire
        trajet_data = {
            'ville_depart': depart,
            'ville_arrivee': arrivee,
            'date': date,
            'heure': heure,
            'places': places,
            'conducteur_id': self.utilisateur['id'],
            'conducteur_nom': self.utilisateur['nom']
        }
        
        # Si on modifie un trajet existant, on le met à jour
        if self.trajet:
            modifier_trajet(self.trajet['id'], trajet_data)
            messagebox.showinfo("Succès", "Trajet modifié avec succès")
        else:
            # Sinon, on ajoute un nouveau trajet
            ajouter_trajet(trajet_data)
            messagebox.showinfo("Succès", "Trajet ajouté avec succès")
        
        # Ferme la fenêtre d'édition
        self.window.destroy()
        # Si un callback est fourni, on l'appelle (ex : pour rafraîchir la liste)
        if self.callback:
            self.callback()