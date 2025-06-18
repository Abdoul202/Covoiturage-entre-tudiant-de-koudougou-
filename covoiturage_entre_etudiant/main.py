import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from gui.login import LoginWindow
from core.gestion_fichier import initialiser_fichiers

def main():
    # Initialiser les fichiers de données s'ils n'existent pas
    initialiser_fichiers()
    
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