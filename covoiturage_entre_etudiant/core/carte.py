import json  # Importe le module json pour manipuler les données au format JSON
from pathlib import Path  # Importe Path pour gérer les chemins de fichiers
import webbrowser  # Importe webbrowser pour éventuellement ouvrir des fichiers HTML dans le navigateur

# Chemins des fichiers
WEB_DIR = Path(__file__).parent.parent / 'web'  # Dossier "web" à la racine du projet
HTML_TEMPLATE = WEB_DIR / 'carte.html'  # Fichier template HTML de la carte

def generer_carte_html(trajets):
    """Génère un fichier HTML avec les trajets affichés sur une carte"""
    # Lire le template HTML
    with open(HTML_TEMPLATE, 'r', encoding='utf-8') as f:
        html_content = f.read()  # Lit le contenu du fichier HTML de base
    
    # Préparer les données des trajets pour JavaScript
    trajets_js = []
    for trajet in trajets:
        trajets_js.append({
            'id': trajet['id'],  # Identifiant du trajet
            'depart': trajet['ville_depart'],  # Ville de départ
            'arrivee': trajet['ville_arrivee'],  # Ville d'arrivée
            'conducteur': trajet['conducteur_nom'],  # Nom du conducteur
            'date': trajet['date'],  # Date du trajet
            'heure': trajet['heure'],  # Heure du trajet
            'places': f"{len(trajet['passagers'])}/{trajet['places']}"  # Places occupées/total
        })
    
    # Remplacer les placeholders dans le template
    html_content = html_content.replace(
        '/* TRAJETS_PLACEHOLDER */',  # Cherche ce texte dans le template
        f'var trajets = {json.dumps(trajets_js, ensure_ascii=False)};'  # Insère les trajets au format JS
    )
    
    # Écrire le fichier HTML temporaire
    output_file = WEB_DIR / 'carte_temp.html'  # Chemin du fichier temporaire à générer
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)  # Écrit le HTML final dans le fichier
    
    return output_file.absolute()  # Retourne le chemin absolu du fichier généré