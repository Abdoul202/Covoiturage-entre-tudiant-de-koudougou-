import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from core.persistence import creer_trajet, modifier_trajet

class EditTrajetWindow:
    def __init__(self, root, utilisateur, trajet=None, callback=None):
        self.root = root
        self.utilisateur = utilisateur
        self.trajet = trajet
        self.callback = callback

        self.window = tk.Toplevel(self.root)
        self.window.title("Nouveau Trajet" if not trajet else "Modifier Trajet")
        self.window.geometry("500x400")

        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.creer_formulaire()

    def creer_formulaire(self):
        ttk.Label(self.main_frame, text="Ville de départ:").pack(pady=(10, 0))
        self.depart_entry = ttk.Entry(self.main_frame)
        self.depart_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self.main_frame, text="Ville d'arrivée:").pack()
        self.arrivee_entry = ttk.Entry(self.main_frame)
        self.arrivee_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self.main_frame, text="Date (AAAA-MM-JJ):").pack()
        self.date_entry = ttk.Entry(self.main_frame)
        self.date_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self.main_frame, text="Heure (HH:MM):").pack()
        self.heure_entry = ttk.Entry(self.main_frame)
        self.heure_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self.main_frame, text="Places disponibles:").pack()
        self.places_spinbox = ttk.Spinbox(self.main_frame, from_=1, to=10)
        self.places_spinbox.pack(fill=tk.X, pady=(0, 20))

        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Annuler", command=self.window.destroy, style='danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Enregistrer", command=self.enregistrer, style='success.TButton').pack(side=tk.RIGHT, padx=5)

        if self.trajet:
            self.depart_entry.insert(0, self.trajet['depart'])
            self.arrivee_entry.insert(0, self.trajet['destination'])
            date, heure = self.trajet['date_heure'].split(' ')
            self.date_entry.insert(0, date)
            self.heure_entry.insert(0, heure)
            self.places_spinbox.set(self.trajet['places_totales'])

    def enregistrer(self):
        depart = self.depart_entry.get().strip()
        arrivee = self.arrivee_entry.get().strip()
        date = self.date_entry.get().strip()
        heure = self.heure_entry.get().strip()
        places = self.places_spinbox.get().strip()

        if not all([depart, arrivee, date, heure, places]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        try:
            places_int = int(places)
            if not (1 <= places_int <= 10): raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Le nombre de places doit être un entier entre 1 et 10.")
            return

        try:
            date_heure_str = f"{date} {heure}"
            datetime.strptime(date_heure_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date (AAAA-MM-JJ) ou d'heure (HH:MM) invalide.")
            return

        if self.trajet:
            modifier_trajet(self.trajet['id'], depart, arrivee, date_heure_str, places_int)
            messagebox.showinfo("Succès", "Trajet modifié avec succès.")
        else:
            creer_trajet(depart, arrivee, date_heure_str, places_int, self.utilisateur['id'])
            messagebox.showinfo("Succès", "Trajet ajouté avec succès.")

        self.window.destroy()
        if self.callback:
            self.callback()
