Visitez mon site web : justinallard.ca


Générer le fichier .spec :
Utilisez la commande suivante pour générer le fichier .spec de base:
TERMINAL OU POWERSHELL→→→ pyinstaller --onefile --icon=snake.ico video_xtractor.py

Puis vous devez inclure le dossier ffmpeg à l'intérieur du fichier spec:
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['video_xtractor.py'],
    pathex=['C:\\VotreDossier\\VotreSousDossier\\video_xtractor'],
    binaries=[],
    datas=[('ffmpeg/bin', 'ffmpeg/bin')],
    hiddenimports=['yt_dlp', 'colorama'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='video_xtractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='snake.ico',
)


Pour créer un fichier exécutable de ce projet (construction de l'exécutable), veuillez, dans le terminal du projet, à l'emplacement du programme, écrire la ligne de commande suivante:
TERMINAL OU POWERSHELL→→→ pyinstaller video_xtractor.spec


Le fichier exécutable video_xtractor.exe se trouvera à l'intérieur du dossier dist nouvellement créé.
