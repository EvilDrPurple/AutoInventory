import PyInstaller.__main__

DIR = 'E:\AutoInventory'

PyInstaller.__main__.run([
    f'{DIR}\\update.py',
    '--onefile',
    '--windowed',
    '-nupdate'
])
