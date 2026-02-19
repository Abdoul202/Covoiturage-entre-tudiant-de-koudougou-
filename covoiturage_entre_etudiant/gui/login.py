import tkinter as tk
from tkinter import ttk, messagebox
from core.persistence import authentifier_utilisateur, creer_utilisateur, UserExistsError, PersistenceError
from gui.dashboard import DashboardWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.creer_widgets()

    def creer_widgets(self):
        ttk.Label(self.frame, text="Covoiturage Étudiant", font=('Helvetica', 16, 'bold')).pack(pady=10)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill=tk.BOTH, pady=10)

        self.login_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.login_tab, text="Connexion")
        self.creer_formulaire_connexion()

        self.register_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.register_tab, text="Inscription")
        self.creer_formulaire_inscription()

    def creer_formulaire_connexion(self):
        ttk.Label(self.login_tab, text="Email:").pack(pady=(10, 0))
        self.login_email = ttk.Entry(self.login_tab)
        self.login_email.pack(fill=tk.X, padx=20, pady=(0, 10))

        ttk.Label(self.login_tab, text="Mot de passe:").pack()
        self.login_password = ttk.Entry(self.login_tab, show="*")
        self.login_password.pack(fill=tk.X, padx=20, pady=(0, 10))

        ttk.Button(self.login_tab, text="Se connecter", command=self.connexion, style='success.TButton').pack(pady=10)

    def creer_formulaire_inscription(self):
        ttk.Label(self.register_tab, text="Nom complet:").pack(pady=(10, 0))
        self.register_name = ttk.Entry(self.register_tab)
        self.register_name.pack(fill=tk.X, padx=20, pady=(0, 10))

        ttk.Label(self.register_tab, text="Email:").pack()
        self.register_email = ttk.Entry(self.register_tab)
        self.register_email.pack(fill=tk.X, padx=20, pady=(0, 10))

        ttk.Label(self.register_tab, text="Mot de passe:").pack()
        self.register_password = ttk.Entry(self.register_tab, show="*")
        self.register_password.pack(fill=tk.X, padx=20, pady=(0, 10))

        ttk.Label(self.register_tab, text="Confirmer mot de passe:").pack()
        self.register_confirm = ttk.Entry(self.register_tab, show="*")
        self.register_confirm.pack(fill=tk.X, padx=20, pady=(0, 10))

        ttk.Button(self.register_tab, text="S'inscrire", command=self.inscription, style='primary.TButton').pack(pady=10)

    def connexion(self):
        email = self.login_email.get()
        password = self.login_password.get()

        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        user = authentifier_utilisateur(email, password)
        if user:
            self.frame.destroy()
            DashboardWindow(self.root, user)
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")

    def inscription(self):
        nom = self.register_name.get()
        email = self.register_email.get()
        password = self.register_password.get()
        confirm = self.register_confirm.get()

        if not all([nom, email, password, confirm]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        if password != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        try:
            creer_utilisateur(nom, email, password)
            messagebox.showinfo("Succès", "Compte créé avec succès! Vous pouvez maintenant vous connecter.")
            self.notebook.select(0)
            # Effacer les champs d'inscription
            for entry in [self.register_name, self.register_email, self.register_password, self.register_confirm]:
                entry.delete(0, tk.END)
        except UserExistsError:
            messagebox.showerror("Erreur", "Cet email est déjà utilisé.")
        except PersistenceError as e:
            messagebox.showerror("Erreur de base de données", str(e))
