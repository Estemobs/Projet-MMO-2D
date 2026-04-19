"""
Update checker for MMO 2D - Fetches latest release from GitHub
"""

import requests
import json
from packaging import version
from systems.version import get_current_version

class UpdateChecker:
    """Checks for available updates from GitHub releases"""

    REPO = "Estemobs/Projet-MMO-2D"
    API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"

    def __init__(self):
        self.current_version = get_current_version()
        self.latest_release = None
        self.has_update = False
        self.error = None

    def check(self):
        """Check for updates from GitHub API"""
        try:
            response = requests.get(self.API_URL, timeout=5)
            response.raise_for_status()
            self.latest_release = response.json()

            latest_tag = self.latest_release.get("tag_name", "")
            latest_version_str = self._parse_version(latest_tag)

            if latest_version_str:
                self.has_update = self._compare_versions(
                    self.current_version,
                    latest_version_str
                )

            return True

        except requests.exceptions.Timeout:
            self.error = "Délai d'attente dépassé (réseau lent)"
            return False
        except requests.exceptions.ConnectionError:
            self.error = "Pas de connexion Internet"
            return False
        except requests.exceptions.RequestException as e:
            self.error = f"Erreur réseau: {str(e)}"
            return False
        except Exception as e:
            self.error = f"Erreur: {str(e)}"
            return False

    def _parse_version(self, tag):
        """Convert git tag (v0.1.2) to version string (0.1.2)"""
        if tag.startswith('v'):
            return tag[1:]
        return tag

    def _compare_versions(self, current, latest):
        """Compare versions using semantic versioning"""
        try:
            return version.parse(latest) > version.parse(current)
        except:
            return False

    def get_latest_version(self):
        """Returns the latest version string"""
        if self.latest_release:
            tag = self.latest_release.get("tag_name", "")
            return self._parse_version(tag)
        return None

    def get_download_url(self, platform="windows"):
        """Get download URL for specified platform (windows or linux)"""
        if not self.latest_release:
            return None

        assets = self.latest_release.get("assets", [])

        for asset in assets:
            filename = asset.get("name", "").lower()
            url = asset.get("browser_download_url", "")

            if platform == "windows" and filename.endswith(".exe"):
                return url
            elif platform == "linux" and filename.endswith(".flatpak"):
                return url

        return None

    def get_release_notes(self):
        """Returns release notes for latest version"""
        if self.latest_release:
            return self.latest_release.get("body", "No release notes")
        return None


def check_for_updates_sync():
    """Synchronous update check (blocking but simple)"""
    checker = UpdateChecker()
    checker.check()
    return checker
