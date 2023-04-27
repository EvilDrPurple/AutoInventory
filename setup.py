import PyInstaller.__main__

PyInstaller.__main__.run([
    'autoinventory.py',
    '--onefile',
    '-n AutoInventory',
    '-ipizza_hut_logo.png'
    #'--add-data=chromedriver.exe;chromedriver.exe'
])
