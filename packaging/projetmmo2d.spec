# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Projet MMO 2D
Build with: pyinstaller packaging/projetmmo2d.spec
"""

import sys
import os

block_cipher = None

# Dossier racine du projet (un niveau au-dessus de packaging/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(SPEC)))

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'main.py')],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=[
        (os.path.join(PROJECT_ROOT, 'assets'), 'assets'),
        (os.path.join(PROJECT_ROOT, 'data'), 'data'),
        (os.path.join(PROJECT_ROOT, 'settings.json'), '.'),
    ],
    hiddenimports=[
        'requests',
        'packaging',
        'packaging.version',
        'packaging.specifiers',
        'packaging.requirements',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ProjetMMO2D',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(PROJECT_ROOT, 'packaging', 'icons', 'hicolor', '256x256', 'apps', 'io.github.Estemobs.ProjetMMO2D.png'),
)
