import PyInstaller.__main__

DIR = 'E:\AutoInventory'

PyInstaller.__main__.run([
    f'{DIR}\\autoinventory.py',
    '--onefile',
    '--windowed',
    '-nAutoInventory',
    f'-i{DIR}\\Images\\pizza_hut_logo.ico'
])
