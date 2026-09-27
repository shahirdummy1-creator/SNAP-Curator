# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('C:\\Users\\User\\.VIRTUALENVS\\DJANGO_PROJECT-7L90E9FR\\Lib\\site-packages\\streamlit', 'streamlit'),
        ('C:\\Users\\User\\.VIRTUALENVS\\DJANGO_PROJECT-7L90E9FR\\Lib\\site-packages\\pandas', 'pandas'),
        ('C:\\Users\\User\\.VIRTUALENVS\\DJANGO_PROJECT-7L90E9FR\\Lib\\site-packages\\requests', 'requests'),
    ],
    hiddenimports=[
        'streamlit',
        'pandas',
        'numpy',
        'requests',
        'openpyxl',
        'PIL',
        'pytesseract',
    ],
    hookspath=[],
    hooksconfig={},
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
    [],
    exclude_binaries=True,
    name='SNAP-Curator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='SNAP-Curator'
)
