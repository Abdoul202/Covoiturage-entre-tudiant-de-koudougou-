import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from gui.login import LoginWindow
from core.database import initialiser_base_de_donnees

def main():
    # Initialiser la base de données
    initialiser_base_de_donnees()

    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Covoiturage Entre Étudiant - Koudougou")

    # Appliquer le style ttkbootstrap
    style = Style(theme='flatly')

    # Démarrer avec la fenêtre de connexion
    LoginWindow(root)

    root.mainloop()

if __name__ == "__main__":
    main()
