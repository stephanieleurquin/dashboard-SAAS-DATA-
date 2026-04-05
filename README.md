# Dashboard Data App - Version Pro

![Dashboard Screenshot](assets/screenshot.png)  <!-- Ajoute un screenshot réel dans assets/ -->

## Description

Dashboard Data App est une application de visualisation de données interactive pour les fichiers CSV.  
Elle permet d’explorer vos données, de filtrer par colonnes numériques ou catégorielles et de générer des graphiques dynamiques.

**Fonctionnalités principales :**
- Chargement de fichiers CSV  
- Sélection des colonnes X et Y pour le graphique  
- Filtres numériques et catégoriels  
- Graphiques multiples dans des onglets  
- Export des graphiques en PNG ou PDF  

L’application utilise **PyQt5** et **Matplotlib** pour une interface graphique desktop, et peut être adaptée pour le web avec Dash/Plotly.

---

## Installation

1. Clone le dépôt :

bash
git clone https://github.com/ton-utilisateur/dashboard-pro.git
cd dashboard-pro
##Crée un environnement virtuel (optionnel mais recommandé) :
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
##Installe les dépendances :
pip install -r requirements.txt

Lancement de l’application

Pour lancer le dashboard :
python dashboard_pro.py
Une fenêtre graphique PyQt5 s’ouvrira, permettant de charger vos fichiers CSV et de créer vos graphiques.
