import tkinter as tk  # Importe le module principal de Tkinter pour créer l'interface graphique
from tkinter import ttk  # Importe les widgets améliorés de Tkinter (boutons, labels, etc.)
from tkinter import messagebox  # Importe les boîtes de dialogue pour afficher des messages à l'utilisateur
from gui.map_view import MapViewWindow  # Importe la fenêtre pour afficher la carte des trajets
from gui.edit_trajet import EditTrajetWindow  # Importe la fenêtre pour ajouter ou modifier un trajet
from core.gestion_fichier import charger_trajets_utilisateur, charger_tous_trajets  # Importe les fonctions pour charger les trajets

class DashboardWindow:
    def __init__(self, root, utilisateur):
        # Constructeur de la classe DashboardWindow
        self.root = root  # La fenêtre principale Tkinter
        self.utilisateur = utilisateur  # Dictionnaire contenant les infos de l'utilisateur connecté
        self.root.title(f"Covoiturage Entre Étudiant - {utilisateur['nom']}")  # Définit le titre de la fenêtre
        self.root.geometry("1000x400")  # Définit la taille de la fenêtre
        
        self.creer_interface()  # Crée tous les widgets de l'interface graphique
        self.actualiser_trajets()  # Affiche la liste des trajets au démarrage
    
    def creer_interface(self):
        # Crée l'interface graphique du tableau de bord
        
        # Frame principale qui contient tout le contenu
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Barre latérale à gauche pour la navigation
        self.sidebar = ttk.Frame(self.main_frame, width=200, style='info.TFrame')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Zone principale à droite pour afficher les trajets
        self.content = ttk.Frame(self.main_frame)
        self.content.pack(expand=True, fill=tk.BOTH)
        
        # Message de bienvenue dans la barre latérale
        ttk.Label(
            self.sidebar, 
            text=f"Bonjour, {self.utilisateur['nom'].split()[0]}!",  # Affiche le prénom de l'utilisateur
            style='info.TLabel',
            font=('Helvetica', 10, 'bold')
        ).pack(pady=(10, 20))
        
        # Bouton pour afficher les trajets de l'utilisateur
        ttk.Button(
            self.sidebar, 
            text="Mes Trajets", 
            command=self.afficher_mes_trajets,  # Appelle la fonction afficher_mes_trajets
            style='info.TButton'
        ).pack(fill=tk.X, pady=5)
        
        # Bouton pour afficher tous les trajets
        ttk.Button(
            self.sidebar, 
            text="Tous les Trajets", 
            command=self.afficher_tous_trajets,  # Appelle la fonction afficher_tous_trajets
            style='info.TButton'
        ).pack(fill=tk.X, pady=5)
        
        # Bouton pour ajouter un nouveau trajet
        ttk.Button(
            self.sidebar, 
            text="Ajouter un Trajet", 
            command=self.ajouter_trajet,  # Appelle la fonction ajouter_trajet
            style='success.TButton'
        ).pack(fill=tk.X, pady=5)
        
        # Bouton pour voir les trajets sur la carte
        ttk.Button(
            self.sidebar, 
            text="Voir sur la Carte", 
            command=self.voir_carte,  # Appelle la fonction voir_carte
            style='primary.TButton'
        ).pack(fill=tk.X, pady=5)
        
        # Bouton pour se déconnecter (en bas de la barre latérale)
        ttk.Button(
            self.sidebar, 
            text="Déconnexion", 
            command=self.deconnexion,  # Appelle la fonction deconnexion
            style='danger.TButton'
        ).pack(fill=tk.X, pady=5, side=tk.BOTTOM)
        
        # Frame qui contient la liste des trajets
        self.trajets_frame = ttk.Frame(self.content)
        self.trajets_frame.pack(expand=True, fill=tk.BOTH)
        
        # Définition des colonnes pour le tableau des trajets
        columns = ('id', 'depart', 'arrivee', 'date', 'heure', 'places', 'conducteur')
        self.trajets_tree = ttk.Treeview(
            self.trajets_frame, 
            columns=columns, 
            show='headings',  # N'affiche que les titres de colonnes
            selectmode='browse'  # Permet de sélectionner une seule ligne à la fois
        )
        
        # Configuration des titres de colonnes
        self.trajets_tree.heading('id', text='ID', anchor=tk.W)
        self.trajets_tree.heading('depart', text='Départ', anchor=tk.W)
        self.trajets_tree.heading('arrivee', text='Arrivée', anchor=tk.W)
        self.trajets_tree.heading('date', text='Date', anchor=tk.W)
        self.trajets_tree.heading('heure', text='Heure', anchor=tk.W)
        self.trajets_tree.heading('places', text='Places', anchor=tk.W)
        self.trajets_tree.heading('conducteur', text='Conducteur', anchor=tk.W)
        
        # Largeur des colonnes
        self.trajets_tree.column('id', width=50, stretch=tk.NO)
        self.trajets_tree.column('depart', width=120)
        self.trajets_tree.column('arrivee', width=120)
        self.trajets_tree.column('date', width=80)
        self.trajets_tree.column('heure', width=60)
        self.trajets_tree.column('places', width=60)
        self.trajets_tree.column('conducteur', width=120)
        
        self.trajets_tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
        # Barre de défilement verticale pour le tableau
        scrollbar = ttk.Scrollbar(
            self.trajets_frame, 
            orient=tk.VERTICAL, 
            command=self.trajets_tree.yview  # Lie la scrollbar au tableau
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.trajets_tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame pour les boutons d'action sous la liste
        action_frame = ttk.Frame(self.content)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Bouton pour rejoindre un trajet
        ttk.Button(
            action_frame, 
            text="Rejoindre", 
            command=self.rejoindre_trajet,  # Appelle la fonction rejoindre_trajet
            style='success.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Bouton pour modifier un trajet
        ttk.Button(
            action_frame, 
            text="Modifier", 
            command=self.modifier_trajet,  # Appelle la fonction modifier_trajet
            style='warning.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Bouton pour supprimer un trajet
        ttk.Button(
            action_frame, 
            text="Supprimer", 
            command=self.supprimer_trajet,  # Appelle la fonction supprimer_trajet
            style='danger.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Bouton pour rafraîchir la liste des trajets
        ttk.Button(
            action_frame, 
            text="Actualiser", 
            command=self.actualiser_trajets,  # Appelle la fonction actualiser_trajets
            style='info.TButton'
        ).pack(side=tk.RIGHT, padx=5)
    
    def afficher_mes_trajets(self):
        # Affiche uniquement les trajets où l'utilisateur est conducteur
        self.mode = "mes_trajets"
        self.actualiser_trajets()
    
    def afficher_tous_trajets(self):
        # Affiche tous les trajets disponibles
        self.mode = "tous_trajets"
        self.actualiser_trajets()
    
    def actualiser_trajets(self):
        # Rafraîchit la liste des trajets affichés dans le tableau
        
        # Efface les anciennes lignes du tableau
        for item in self.trajets_tree.get_children():
            self.trajets_tree.delete(item)
        
        # Charge les trajets selon le mode choisi (tous ou seulement ceux de l'utilisateur)
        if hasattr(self, 'mode') and self.mode == "mes_trajets":
            trajets = charger_trajets_utilisateur(self.utilisateur['id'])
        else:
            trajets = charger_tous_trajets()
            self.mode = "tous_trajets"
        
        # Ajoute chaque trajet dans le tableau
        for trajet in trajets:
            self.trajets_tree.insert('', tk.END, values=(
                trajet['id'],
                trajet['ville_depart'],
                trajet['ville_arrivee'],
                trajet['date'],
                trajet['heure'],
                f"{len(trajet['passagers'])}/{trajet['places']}",
                trajet['conducteur_nom']
            ))
    
    def ajouter_trajet(self):
        # Ouvre la fenêtre pour ajouter un nouveau trajet
        EditTrajetWindow(self.root, self.utilisateur, None, self.actualiser_trajets)
    
    def modifier_trajet(self):
        # Permet de modifier un trajet sélectionné
        selection = self.trajets_tree.selection()  # Récupère la sélection dans le tableau
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un trajet à modifier")
            return
        
        item = self.trajets_tree.item(selection[0])  # Récupère les infos du trajet sélectionné
        trajet_id = item['values'][0]  # Récupère l'ID du trajet
        
        # Vérifie que l'utilisateur est bien le conducteur du trajet
        trajets = charger_tous_trajets()
        trajet = next((t for t in trajets if t['id'] == trajet_id), None)
        
        if not trajet:
            messagebox.showerror("Erreur", "Trajet introuvable")
            return
        
        if trajet['conducteur_id'] != self.utilisateur['id']:
            messagebox.showerror("Erreur", "Vous ne pouvez modifier que vos propres trajets")
            return
        
        # Ouvre la fenêtre d'édition du trajet
        EditTrajetWindow(self.root, self.utilisateur, trajet, self.actualiser_trajets)
    
    def supprimer_trajet(self):
        # Permet de supprimer un trajet sélectionné
        selection = self.trajets_tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un trajet à supprimer")
            return
        
        item = self.trajets_tree.item(selection[0])
        trajet_id = item['values'][0]
        
        # Vérifie que l'utilisateur est bien le conducteur du trajet
        trajets = charger_tous_trajets()
        trajet = next((t for t in trajets if t['id'] == trajet_id), None)
        
        if not trajet:
            messagebox.showerror("Erreur", "Trajet introuvable")
            return
        
        if trajet['conducteur_id'] != self.utilisateur['id']:
            messagebox.showerror("Erreur", "Vous ne pouvez supprimer que vos propres trajets")
            return
        
        # Demande confirmation avant suppression
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce trajet?"):
            from core.trajet import supprimer_trajet  # Importe la fonction de suppression
            supprimer_trajet(trajet_id)  # Supprime le trajet
            self.actualiser_trajets()    # Rafraîchit la liste des trajets affichés
            messagebox.showinfo("Succès", "Trajet supprimé avec succès")  # Affiche un message de succès
    
    def rejoindre_trajet(self):
        # Permet à l'utilisateur de rejoindre un trajet comme passager
        selection = self.trajets_tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un trajet à rejoindre")
            return
        
        item = self.trajets_tree.item(selection[0])
        trajet_id = item['values'][0]
        
        # Recherche le trajet sélectionné
        trajets = charger_tous_trajets()
        trajet = next((t for t in trajets if t['id'] == trajet_id), None)
        
        if not trajet:
            messagebox.showerror("Erreur", "Trajet introuvable")
            return
        
        # Vérifie que l'utilisateur n'est pas le conducteur
        if trajet['conducteur_id'] == self.utilisateur['id']:
            messagebox.showerror("Erreur", "Vous ne pouvez pas rejoindre votre propre trajet")
            return
        
        # Vérifie que l'utilisateur n'a pas déjà rejoint ce trajet
        if self.utilisateur['id'] in trajet['passagers']:
            messagebox.showerror("Erreur", "Vous avez déjà rejoint ce trajet")
            return
        
        # Vérifie qu'il reste des places disponibles
        if len(trajet['passagers']) >= trajet['places']:
            messagebox.showerror("Erreur", "Plus de places disponibles pour ce trajet")
            return
        
        # Demande confirmation avant de rejoindre
        if messagebox.askyesno("Confirmation", f"Rejoindre le trajet de {trajet['ville_depart']} à {trajet['ville_arrivee']}?"):
            from core.trajet import rejoindre_trajet  # Importe la fonction pour rejoindre un trajet
            rejoindre_trajet(trajet_id, self.utilisateur['id'])  # Ajoute l'utilisateur comme passager
            self.actualiser_trajets()  # Rafraîchit la liste des trajets
            messagebox.showinfo("Succès", "Vous avez rejoint le trajet avec succès")  # Message de succès
    
    def voir_carte(self):
        # Ouvre la fenêtre de visualisation des trajets sur une carte
        MapViewWindow(self.root, self.utilisateur)
    
    def deconnexion(self):
        # Déconnecte l'utilisateur et retourne à la fenêtre de connexion
        from gui.login import LoginWindow
        self.main_frame.destroy()  # Détruit le contenu du tableau de bord
        LoginWindow(self.root)  # Affiche la fenêtre de connexion