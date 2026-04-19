"""
Update installer for MMO 2D - Downloads and installs updates
"""

import os
import sys
import requests
import shutil
import subprocess
import platform
from pathlib import Path


class UpdateInstaller:
    """Handles downloading and installing updates"""

    def __init__(self, checker):
        self.checker = checker
        self.platform = platform.system()
        self.temp_dir = Path(os.path.expanduser("~/.mmo2d_updates"))

    def download_update(self):
        """Download the update file"""
        if not self.checker.has_update:
            return False, "Pas de mise à jour disponible"

        platform_name = "windows" if self.platform == "Windows" else "linux"
        url = self.checker.get_download_url(platform=platform_name)

        if not url:
            return False, f"Fichier de mise à jour non trouvé pour {platform_name}"

        try:
            # Create temp directory
            self.temp_dir.mkdir(parents=True, exist_ok=True)

            # Determine filename
            filename = url.split('/')[-1]
            filepath = self.temp_dir / filename

            print(f"📥 Téléchargement: {filename}...")

            # Download with progress
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            print(f"  {percent:.1f}%", end='\r')

            print(f"✅ Téléchargement terminé: {filepath}")
            return True, filepath

        except requests.exceptions.RequestException as e:
            return False, f"Erreur de téléchargement: {str(e)}"
        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def install_update(self, filepath):
        """Install the downloaded update"""
        try:
            if self.platform == "Windows":
                return self._install_windows(filepath)
            elif self.platform == "Linux":
                return self._install_linux(filepath)
            else:
                return False, f"Plateforme non supportée: {self.platform}"

        except Exception as e:
            return False, f"Erreur d'installation: {str(e)}"

    def _install_windows(self, filepath):
        """Install EXE on Windows"""
        try:
            # For .exe, simply download to AppData or Program Files
            app_data = Path(os.getenv('APPDATA', os.path.expanduser('~/AppData/Roaming')))
            mmo2d_dir = app_data / "MMO2D"
            mmo2d_dir.mkdir(parents=True, exist_ok=True)

            install_path = mmo2d_dir / filepath.name
            shutil.copy2(filepath, install_path)

            print(f"✅ Mise à jour installée: {install_path}")
            print("⚠️  Veuillez relancer l'application")

            return True, str(install_path)

        except Exception as e:
            return False, str(e)

    def _install_linux(self, filepath):
        """Install Flatpak on Linux"""
        try:
            # Use flatpak to install the bundle
            result = subprocess.run(
                ["flatpak", "install", "--assumeyes", str(filepath)],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                print("✅ Mise à jour Flatpak installée")
                print("⚠️  Veuillez relancer l'application")
                return True, str(filepath)
            else:
                return False, result.stderr or "Erreur Flatpak inconnue"

        except subprocess.TimeoutExpired:
            return False, "Délai d'installation dépassé"
        except FileNotFoundError:
            return False, "Flatpak non installé - impossible de procéder"
        except Exception as e:
            return False, str(e)

    def cleanup(self):
        """Clean up temporary files"""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
        except:
            pass


def prompt_for_update(checker):
    """Prompt user to install update"""
    if not checker.has_update:
        return False

    latest = checker.get_latest_version()
    current = checker.current_version

    print(f"\n⚠️  Mise à jour disponible: {current} → {latest}")
    response = input("Voulez-vous mettre à jour maintenant? [O/n]: ").strip().lower()

    return response in ['o', 'oui', 'yes', 'y', '']
