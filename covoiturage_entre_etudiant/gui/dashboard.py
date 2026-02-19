import tkinter as tk
from tkinter import ttk, messagebox
from gui.map_view import MapViewWindow
from gui.edit_trajet import EditTrajetWindow
from core.persistence import charger_trajets_utilisateur, charger_tous_trajets, supprimer_trajet, rejoindre_trajet

class DashboardWindow:
    def __init__(self, root, utilisateur):
        self.root = root
        self.utilisateur = utilisateur
        self.root.title(f"Covoiturage - {utilisateur['nom']}")
        self.root.geometry("1000x400")

        self.creer_interface()
        self.afficher_tous_trajets()

    def creer_interface(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.sidebar = ttk.Frame(self.main_frame, width=200, style='info.TFrame')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.content = ttk.Frame(self.main_frame)
        self.content.pack(expand=True, fill=tk.BOTH)

        ttk.Label(self.sidebar, text=f"Bonjour, {self.utilisateur['nom'].split()[0]}!", style='info.TLabel', font=('Helvetica', 10, 'bold')).pack(pady=(10, 20))

        ttk.Button(self.sidebar, text="Mes Trajets", command=self.afficher_mes_trajets, style='info.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(self.sidebar, text="Tous les Trajets", command=self.afficher_tous_trajets, style='info.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(self.sidebar, text="Ajouter un Trajet", command=self.ajouter_trajet, style='success.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(self.sidebar, text="Voir sur la Carte", command=self.voir_carte, style='primary.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(self.sidebar, text="Déconnexion", command=self.deconnexion, style='danger.TButton').pack(fill=tk.X, pady=5, side=tk.BOTTOM)

        self.trajets_frame = ttk.Frame(self.content)
        self.trajets_frame.pack(expand=True, fill=tk.BOTH)

        columns = ('id', 'depart', 'arrivee', 'date', 'heure', 'places', 'conducteur')
        self.trajets_tree = ttk.Treeview(self.trajets_frame, columns=columns, show='headings', selectmode='browse')

        for col in columns:
            self.trajets_tree.heading(col, text=col.capitalize(), anchor=tk.W)

        self.trajets_tree.column('id', width=40, stretch=tk.NO)
        self.trajets_tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(self.trajets_frame, orient=tk.VERTICAL, command=self.trajets_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.trajets_tree.configure(yscrollcommand=scrollbar.set)

        action_frame = ttk.Frame(self.content)
        action_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(action_frame, text="Rejoindre", command=self.rejoindre_trajet_action, style='success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Modifier", command=self.modifier_trajet_action, style='warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Supprimer", command=self.supprimer_trajet_action, style='danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Actualiser", command=self.actualiser_trajets, style='info.TButton').pack(side=tk.RIGHT, padx=5)

    def afficher_mes_trajets(self):
        self.mode_affichage = "mes_trajets"
        self.actualiser_trajets()

    def afficher_tous_trajets(self):
        self.mode_affichage = "tous_trajets"
        self.actualiser_trajets()

    def actualiser_trajets(self):
        for item in self.trajets_tree.get_children():
            self.trajets_tree.delete(item)

        if getattr(self, 'mode_affichage', 'tous_trajets') == "mes_trajets":
            trajets = charger_trajets_utilisateur(self.utilisateur['id'])
        else:
            trajets = charger_tous_trajets()

        for trajet in trajets:
            date, heure = trajet['date_heure'].split(' ')
            places_str = f"{trajet['places_disponibles']}/{trajet['places_totales']}"
            self.trajets_tree.insert('', tk.END, values=(
                trajet['id'], trajet['depart'], trajet['destination'], date, heure, places_str, trajet['conducteur_nom']
            ))

    def ajouter_trajet(self):
        EditTrajetWindow(self.root, self.utilisateur, None, self.actualiser_trajets)

    def get_selected_trajet_id(self):
        selection = self.trajets_tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un trajet.")
            return None
        return self.trajets_tree.item(selection[0])['values'][0]

    def rejoindre_trajet_action(self):
        trajet_id = self.get_selected_trajet_id()
        if not trajet_id: return

        trajet = next((t for t in charger_tous_trajets() if t['id'] == trajet_id), None)
        if not trajet:
            messagebox.showerror("Erreur", "Trajet introuvable.")
            return

        if trajet['conducteur_id'] == self.utilisateur['id']:
            messagebox.showerror("Action impossible", "Vous ne pouvez pas rejoindre votre propre trajet.")
            return

        if trajet['places_disponibles'] <= 0:
            messagebox.showinfo("Complet", "Ce trajet est complet.")
            return

        try:
            rejoindre_trajet(trajet_id, self.utilisateur['id'])
            messagebox.showinfo("Succès", "Vous avez rejoint le trajet!")
            self.actualiser_trajets()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de rejoindre le trajet: {e}")

    def modifier_trajet_action(self):
        trajet_id = self.get_selected_trajet_id()
        if not trajet_id: return

        trajet = next((t for t in charger_tous_trajets() if t['id'] == trajet_id), None)
        if not trajet:
            messagebox.showerror("Erreur", "Trajet non trouvé.")
            return

        if trajet['conducteur_id'] != self.utilisateur['id']:
            messagebox.showerror("Interdit", "Vous ne pouvez modifier que vos propres trajets.")
            return

        EditTrajetWindow(self.root, self.utilisateur, trajet, self.actualiser_trajets)

    def supprimer_trajet_action(self):
        trajet_id = self.get_selected_trajet_id()
        if not trajet_id: return

        trajet = next((t for t in charger_tous_trajets() if t['id'] == trajet_id), None)
        if not trajet:
            messagebox.showerror("Erreur", "Trajet non trouvé.")
            return

        if trajet['conducteur_id'] != self.utilisateur['id']:
            messagebox.showerror("Interdit", "Vous ne pouvez supprimer que vos propres trajets.")
            return

        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce trajet?"):
            supprimer_trajet(trajet_id)
            self.actualiser_trajets()
            messagebox.showinfo("Succès", "Trajet supprimé.")

    def voir_carte(self):
        MapViewWindow(self.root, self.utilisateur)

    def deconnexion(self):
        from gui.login import LoginWindow
        self.main_frame.destroy()
        LoginWindow(self.root)
