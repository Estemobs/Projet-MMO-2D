#!/usr/bin/env python3
"""
Point d'entrée principal du jeu MMO 2D
Ce fichier lance simplement le script de lancement complet.
"""

import sys
import os

# Ajouter le répertoire scripts au path
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, 'scripts')
sys.path.insert(0, scripts_dir)

if __name__ == "__main__":
    from launch import main
    main()
