import PyInstaller.__main__

PyInstaller.__main__.run([
    'autoinventory.py',
    '--onefile',
    '-nAutoInventory',
    '-ipizza_hut_logo.ico'
])
