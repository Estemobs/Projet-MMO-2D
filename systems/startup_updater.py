"""
Startup update flow for MMO 2D.
Checks GitHub releases before the game engine is imported so the user
can accept or decline an update from a small dialog.
"""

from __future__ import annotations

import sys

try:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter.scrolledtext import ScrolledText
except Exception:  # pragma: no cover - tkinter is platform dependent
    tk = None
    messagebox = None
    ScrolledText = None

from systems.update_checker import check_for_updates_sync
from systems.update_installer import UpdateInstaller


DIALOG_TITLE = "MMO 2D - Mise à jour"


def check_and_prompt_for_update() -> bool:
    """Check GitHub and show a GUI prompt if a new release exists.

    Returns True when the game should continue launching.
    Returns False when an update was installed successfully and the caller
    should exit.
    """

    checker = check_for_updates_sync()

    if checker.error:
        print(f"⚠️  Mise à jour ignorée: {checker.error}")
        return True

    if not checker.has_update:
        return True

    latest_version = checker.get_latest_version() or "inconnue"
    current_version = checker.current_version
    release_notes = checker.get_release_notes() or "Aucune note de version disponible."

    if not _show_update_dialog(current_version, latest_version, release_notes):
        return True

    installer = UpdateInstaller(checker)
    success, payload = installer.download_update()

    if not success:
        installer.cleanup()
        _show_error_dialog("Téléchargement impossible", str(payload))
        return True

    success, payload = installer.install_update(payload)
    installer.cleanup()

    if success:
        _show_info_dialog(
            "Mise à jour installée",
            "La mise à jour a été installée. Relance le jeu pour appliquer la nouvelle version.",
        )
        return False

    _show_error_dialog("Installation impossible", str(payload))
    return True


def _show_update_dialog(current_version: str, latest_version: str, release_notes: str) -> bool:
    """Display a small modal dialog asking the user to update."""

    if tk is None:
        return _fallback_console_prompt(current_version, latest_version, release_notes)

    try:
        root = tk.Tk()
    except Exception:
        return _fallback_console_prompt(current_version, latest_version, release_notes)

    root.withdraw()
    root.title(DIALOG_TITLE)
    root.resizable(False, False)
    root.attributes("-topmost", True)

    window = tk.Toplevel(root)
    window.title(DIALOG_TITLE)
    window.resizable(False, False)
    window.attributes("-topmost", True)
    window.protocol("WM_DELETE_WINDOW", window.destroy)

    container = tk.Frame(window, padx=16, pady=16)
    container.pack(fill="both", expand=True)

    title_label = tk.Label(
        container,
        text="Une nouvelle version est disponible.",
        font=("TkDefaultFont", 11, "bold"),
    )
    title_label.pack(anchor="w")

    version_label = tk.Label(
        container,
        text=f"Version actuelle: {current_version}   Nouvelle version: {latest_version}",
        pady=8,
    )
    version_label.pack(anchor="w")

    notes_label = tk.Label(container, text="Notes de version:")
    notes_label.pack(anchor="w", pady=(8, 4))

    notes_box = ScrolledText(container, width=68, height=12, wrap="word")
    notes_box.pack(fill="both", expand=True)
    notes_box.insert("1.0", release_notes.strip())
    notes_box.configure(state="disabled")

    result = {"accepted": False}

    def accept_update() -> None:
        result["accepted"] = True
        window.destroy()

    def decline_update() -> None:
        window.destroy()

    buttons = tk.Frame(container, pady=12)
    buttons.pack(fill="x")

    later_button = tk.Button(buttons, text="Plus tard", command=decline_update, width=12)
    later_button.pack(side="right", padx=(8, 0))

    update_button = tk.Button(buttons, text="Mettre à jour", command=accept_update, width=14)
    update_button.pack(side="right")

    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = max((screen_width - width) // 2, 0)
    y = max((screen_height - height) // 2, 0)
    window.geometry(f"+{x}+{y}")
    window.transient(root)
    window.grab_set()
    window.lift()
    window.focus_force()

    root.wait_window(window)
    root.destroy()
    return result["accepted"]


def _fallback_console_prompt(current_version: str, latest_version: str, release_notes: str) -> bool:
    """Fallback prompt when tkinter is not available."""

    if not sys.stdin.isatty():
        print("⚠️  Impossible d'afficher la fenêtre de mise à jour, lancement du jeu.")
        return False

    print()
    print(f"Nouvelle version disponible: {current_version} -> {latest_version}")
    print(release_notes.strip()[:800])
    response = input("Mettre à jour maintenant ? [o/N]: ").strip().lower()
    return response in {"o", "oui", "y", "yes", ""}


def _show_error_dialog(title: str, message: str) -> None:
    if tk is None or messagebox is None:
        print(f"❌ {title}: {message}")
        return

    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message, parent=root)
        root.destroy()
    except Exception:
        print(f"❌ {title}: {message}")


def _show_info_dialog(title: str, message: str) -> None:
    if tk is None or messagebox is None:
        print(f"✅ {title}: {message}")
        return

    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title, message, parent=root)
        root.destroy()
    except Exception:
        print(f"✅ {title}: {message}")
