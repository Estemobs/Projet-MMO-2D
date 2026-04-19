#!/usr/bin/env python3
"""
Script de lancement et vérification du jeu MMO 2D
Ce script vérifie l'intégrité de l'installation et lance le jeu proprement.
"""

import sys
import importlib
import argparse
from pathlib import Path

# Couleurs pour l'affichage terminal
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(text, color=Colors.WHITE):
    """Affiche du texte coloré"""
    print(f"{color}{text}{Colors.END}")

def print_header(title):
    """Affiche un titre avec une ligne de séparation"""
    print_colored(f"\n{title}", Colors.BOLD + Colors.BLUE)
    print_colored("=" * len(title), Colors.BLUE)

def check_python_version():
    """Vérifie la version de Python"""
    print_header("🐍 Vérification de Python")
    
    if sys.version_info < (3, 8):
        print_colored("❌ Python 3.8+ requis", Colors.RED)
        print_colored(f"   Version actuelle: {sys.version}", Colors.YELLOW)
        return False
    
    print_colored(f"✅ Python {sys.version.split()[0]} détecté", Colors.GREEN)
    return True

def check_virtual_env():
    """Vérifie si on est dans un environnement virtuel"""
    print_header("🌐 Vérification de l'environnement virtuel")
    
    venv_path = Path(".venv")
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if venv_path.exists() and not in_venv:
        print_colored("⚠️  Environnement virtuel détecté mais non activé", Colors.YELLOW)
        print_colored("💡 Conseil: Activez-le avec 'source .venv/bin/activate'", Colors.CYAN)
        return False
    elif in_venv:
        print_colored("✅ Environnement virtuel actif", Colors.GREEN)
        return True
    else:
        print_colored("⚠️  Aucun environnement virtuel détecté", Colors.YELLOW)
        return True

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print_header("📦 Vérification des dépendances")
    
    required_modules = [
        ('pygame', 'Interface graphique du jeu'),
        ('numpy', 'Calculs mathématiques'),
        ('psutil', 'Informations système'),
    ]
    
    missing_modules = []
    
    for module, description in required_modules:
        try:
            importlib.import_module(module)
            print_colored(f"  ✅ {module:<12} - {description}", Colors.GREEN)
        except ImportError:
            print_colored(f"  ❌ {module:<12} - {description}", Colors.RED)
            missing_modules.append(module)
    
    if missing_modules:
        print_colored(f"\n❌ Modules manquants: {', '.join(missing_modules)}", Colors.RED)
        print_colored("💡 Installez avec: pip install -r requirements.txt", Colors.CYAN)
        return False
    
    print_colored("\n✅ Toutes les dépendances sont installées", Colors.GREEN)
    return True

def check_game_files():
    """Vérifie que tous les fichiers du jeu sont présents"""
    print_header("📁 Vérification des fichiers du jeu")
    
    # Ajuster les chemins relatifs au répertoire parent
    project_root = Path(__file__).parent.parent
    
    required_files = [
        (project_root / 'game/core.py', 'Module principal du jeu'),
        (project_root / 'game/__init__.py', 'Package de jeu'),
        (project_root / 'data/config.py', 'Configuration du jeu'),
        (project_root / 'ui/inventory.py', 'Système d\'inventaire'),
        (project_root / 'ui/menu.py', 'Interface des menus'),
        (project_root / 'requirements.txt', 'Liste des dépendances'),
    ]
    
    missing_files = []
    
    for file_path, description in required_files:
        if file_path.exists():
            print_colored(f"  ✅ {str(file_path.relative_to(project_root)):<15} - {description}", Colors.GREEN)
        else:
            print_colored(f"  ❌ {str(file_path.relative_to(project_root)):<15} - {description}", Colors.RED)
            missing_files.append(str(file_path.relative_to(project_root)))
    
    if missing_files:
        print_colored(f"\n❌ Fichiers manquants: {', '.join(missing_files)}", Colors.RED)
        return False
    
    print_colored("\n✅ Tous les fichiers requis sont présents", Colors.GREEN)
    return True

def check_for_updates():
    """Vérifie s'il y a une mise à jour disponible"""
    print_header("⚙️  Vérification des mises à jour")

    try:
        # Import du module de vérification des updates
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from systems.update_checker import check_for_updates_sync
        from systems.update_installer import prompt_for_update, UpdateInstaller

        print_colored("🔍 Vérification sur GitHub...", Colors.CYAN)
        checker = check_for_updates_sync()

        if checker.error:
            print_colored(f"⚠️  {checker.error}", Colors.YELLOW)
            return True  # Non-blocking: continue même si erreur

        if checker.has_update:
            latest = checker.get_latest_version()
            current = checker.current_version
            print_colored(f"✨ Mise à jour disponible: {current} → {latest}", Colors.YELLOW)

            if prompt_for_update(checker):
                print_colored("📥 Téléchargement de la mise à jour...", Colors.BLUE)
                installer = UpdateInstaller(checker)
                success, filepath = installer.download_update()

                if success:
                    success, message = installer.install_update(filepath)
                    installer.cleanup()

                    if success:
                        print_colored("✅ Mise à jour complète, redémarrage...", Colors.GREEN)
                        sys.exit(0)
                    else:
                        print_colored(f"❌ Erreur d'installation: {message}", Colors.RED)
                        return True  # Continue anyway
                else:
                    print_colored(f"❌ Erreur de téléchargement: {filepath}", Colors.RED)
                    return True  # Continue anyway
            else:
                print_colored("⏭️  Mise à jour ignorée", Colors.YELLOW)
                return True
        else:
            print_colored(f"✅ Vous avez la dernière version ({checker.current_version})", Colors.GREEN)
            return True

    except ImportError:
        print_colored("⚠️  Modules de mise à jour non disponibles", Colors.YELLOW)
        return True  # Non-blocking
    except Exception as e:
        print_colored(f"⚠️  Erreur lors de la vérification: {e}", Colors.YELLOW)
        return True  # Non-blocking
    """Exécute toutes les vérifications d'intégrité"""
    print_colored("🔍 VÉRIFICATION DE L'INTÉGRITÉ DU PROJET", Colors.BOLD + Colors.PURPLE)
    print_colored("=" * 50, Colors.PURPLE)
    
    checks = [
        ("Version Python", check_python_version),
        ("Environnement virtuel", check_virtual_env),
        ("Dépendances", check_dependencies),
        ("Fichiers du jeu", check_game_files),
        ("Mises à jour", check_for_updates),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_colored(f"❌ Erreur lors de {check_name}: {e}", Colors.RED)
            results.append((check_name, False))
    
    # Résumé
    print_header("📊 Résumé des vérifications")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHEC"
        color = Colors.GREEN if result else Colors.RED
        print_colored(f"  {check_name:<25} {status}", color)
    
    print_colored(f"\n📈 Score: {passed}/{total} vérifications réussies", 
                 Colors.GREEN if passed == total else Colors.YELLOW)
    
    return passed == total

def show_controls():
    """Affiche les contrôles du jeu"""
    print_header("🎮 CONTRÔLES DU JEU")
    
    controls = [
        ("🚶 Se déplacer", "WASD ou flèches directionnelles"),
        ("🔨 Récolter/Construire", "Clic gauche"),
        ("🏗️  Mode construction", "Touche B"),
        ("🧱 Fondation", "Touche 1"),
        ("🏠 Mur", "Touche 2"),
        ("🎒 Inventaire", "Touche I"),
        ("💾 Sauvegarder", "Touche F5"),
        ("🏃 Quitter", "Touche Échap"),
    ]
    
    for action, control in controls:
        print_colored(f"  {action:<20} {control}", Colors.CYAN)

def launch_game():
    """Lance le jeu principal"""
    print_header("🚀 LANCEMENT DU JEU")
    
    try:
        # Ajouter le répertoire parent au path pour les imports
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        print_colored("📥 Importation des modules...", Colors.BLUE)
        from core import GameManager
        
        print_colored("✅ Modules chargés avec succès", Colors.GREEN)
        print_colored("🎯 Initialisation du jeu...", Colors.BLUE)
        
        game_manager = GameManager()
        print_colored("✅ Jeu initialisé", Colors.GREEN)
        
        show_controls()
        
        print_colored("\n🎯 Que la partie commence !", Colors.BOLD + Colors.GREEN)
        print_colored("=" * 40, Colors.GREEN)
        
        game_manager.run()
        
    except ImportError as e:
        print_colored(f"❌ Erreur d'importation: {e}", Colors.RED)
        print_colored("💡 Exécutez d'abord les vérifications avec --check", Colors.CYAN)
        return False
        
    except Exception as e:
        print_colored(f"❌ Erreur lors du lancement: {e}", Colors.RED)
        print_colored(f"💡 Détails de l'erreur: {type(e).__name__}", Colors.YELLOW)
        return False
    
    return True

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description="Script de lancement du jeu MMO 2D",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
    python launch.py                  # Lance le jeu depuis la racine
    python launch.py --check          # Vérifie puis lance
    python launch.py --check-only     # Vérifie seulement
    python scripts/launch.py --check  # Lance directement le script interne
        """
    )
    
    parser.add_argument('--check', action='store_true',
                       help='Effectue les vérifications d\'intégrité avant le lancement')
    parser.add_argument('--check-only', action='store_true',
                       help='Effectue seulement les vérifications sans lancer le jeu')
    
    args = parser.parse_args()
    
    # Affichage du titre
    print_colored("🎮 GESTIONNAIRE DE JEU MMO 2D", Colors.BOLD + Colors.PURPLE)
    print_colored("=" * 35, Colors.PURPLE)
    
    # Vérifications d'intégrité
    if args.check or args.check_only:
        integrity_ok = run_integrity_check()
        
        if args.check_only:
            if integrity_ok:
                print_colored("\n🎉 Le projet est prêt à être lancé !", Colors.BOLD + Colors.GREEN)
                sys.exit(0)
            else:
                print_colored("\n❌ Des problèmes ont été détectés", Colors.BOLD + Colors.RED)
                sys.exit(1)
        
        if not integrity_ok:
            print_colored("\n❌ Impossible de lancer le jeu en raison des erreurs détectées", Colors.RED)
            print_colored("💡 Corrigez les problèmes et relancez", Colors.CYAN)
            sys.exit(1)
    
    # Lancement du jeu
    success = launch_game()
    
    if success:
        print_colored("\n👋 Merci d'avoir joué ! À bientôt !", Colors.BOLD + Colors.BLUE)
    else:
        print_colored("\n❌ Le jeu s'est arrêté de manière inattendue", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
