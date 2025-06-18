import tkinter as tk  # Importe le module principal de Tkinter pour l'interface graphique
from tkinter import ttk  # Importe les widgets améliorés de Tkinter (boutons, labels, etc.)
from tkinter import messagebox  # Importe les boîtes de dialogue pour afficher des messages à l'utilisateur
from core.utilisateur import authentifier_utilisateur, creer_utilisateur  # Fonctions pour gérer les utilisateurs
from core.gestion_fichier import charger_utilisateurs  # Fonction pour charger la liste des utilisateurs
from gui.dashboard import DashboardWindow  # Importe la fenêtre principale après connexion

class LoginWindow:
    def __init__(self, root):
        self.root = root  # Fenêtre principale de l'application
        self.root.geometry("400x300")  # Définit la taille de la fenêtre
        self.frame = ttk.Frame(self.root, padding="20")  # Crée un cadre principal avec du padding
        self.frame.pack(expand=True, fill=tk.BOTH)  # Affiche le cadre dans la fenêtre
        
        self.creer_widgets()  # Crée tous les widgets de l'interface
    
    def creer_widgets(self):
        # Titre de l'application
        ttk.Label(self.frame, text="Covoiturage Étudiant", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        # Notebook pour les onglets Connexion et Inscription
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Onglet Connexion
        self.login_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.login_tab, text="Connexion")
        self.creer_formulaire_connexion()  # Crée le formulaire de connexion
        
        # Onglet Inscription
        self.register_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.register_tab, text="Inscription")
        self.creer_formulaire_inscription()  # Crée le formulaire d'inscription
    
    def creer_formulaire_connexion(self):
        # Champ Email
        ttk.Label(self.login_tab, text="Email:").pack(pady=(10, 0))
        self.login_email = ttk.Entry(self.login_tab)
        self.login_email.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Champ Mot de passe
        ttk.Label(self.login_tab, text="Mot de passe:").pack()
        self.login_password = ttk.Entry(self.login_tab, show="*")  # Affiche des étoiles pour le mot de passe
        self.login_password.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Bouton de connexion
        ttk.Button(
            self.login_tab, 
            text="Se connecter", 
            command=self.connexion,  # Appelle la méthode connexion
            style='success.TButton'
        ).pack(pady=10)
    
    def creer_formulaire_inscription(self):
        # Champ Nom complet
        ttk.Label(self.register_tab, text="Nom complet:").pack(pady=(10, 0))
        self.register_name = ttk.Entry(self.register_tab)
        self.register_name.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Champ Email
        ttk.Label(self.register_tab, text="Email:").pack()
        self.register_email = ttk.Entry(self.register_tab)
        self.register_email.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Champ Mot de passe
        ttk.Label(self.register_tab, text="Mot de passe:").pack()
        self.register_password = ttk.Entry(self.register_tab, show="*")
        self.register_password.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Champ Confirmation mot de passe
        ttk.Label(self.register_tab, text="Confirmer mot de passe:").pack()
        self.register_confirm = ttk.Entry(self.register_tab, show="*")
        self.register_confirm.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Bouton d'inscription
        ttk.Button(
            self.register_tab, 
            text="S'inscrire", 
            command=self.inscription,  # Appelle la méthode inscription
            style='primary.TButton'
        ).pack(pady=10)
    
    def connexion(self):
        # Récupère les valeurs saisies dans les champs de connexion
        email = self.login_email.get()
        password = self.login_password.get()
        
        # Vérifie que tous les champs sont remplis
        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        # Tente d'authentifier l'utilisateur
        user = authentifier_utilisateur(email, password)
        if user:
            self.frame.destroy()  # Ferme la fenêtre de connexion
            DashboardWindow(self.root, user)  # Ouvre le tableau de bord
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect")
    
    def inscription(self):
        # Récupère les valeurs saisies dans les champs d'inscription
        nom = self.register_name.get()
        email = self.register_email.get()
        password = self.register_password.get()
        confirm = self.register_confirm.get()
        
        # Vérifie que tous les champs sont remplis
        if not all([nom, email, password, confirm]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        # Vérifie que les deux mots de passe sont identiques
        if password != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            return
        
        # Vérifie si l'email existe déjà dans la base d'utilisateurs
        utilisateurs = charger_utilisateurs()
        if any(u['email'] == email for u in utilisateurs):
            messagebox.showerror("Erreur", "Cet email est déjà utilisé")
            return
        
        # Crée le nouvel utilisateur
        creer_utilisateur(nom, email, password)
        messagebox.showinfo("Succès", "Compte créé avec succès! Vous pouvez maintenant vous connecter.")
        
        # Bascule vers l'onglet de connexion et vide les champs d'inscription
        self.notebook.select(0)
        self.register_name.delete(0, tk.END)
        self.register_email.delete(0, tk.END)
        self.register_password.delete(0, tk.END)
        self.register_confirm.delete(0, tk.END)