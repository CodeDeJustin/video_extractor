# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(
    ['video_xtractor.py'],
    pathex=['D:\\OneDrive\\SITE_WEB\\video_xtractor'],
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