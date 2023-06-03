import os
import tempfile
import time
import configparser

import PySimpleGUI as sg
import wget

config = configparser.ConfigParser()
config.read('config.ini')

LEGACY = config.getboolean('Important Things', 'legacy')
WIN7 = '-win7' if LEGACY else ''

DOWNLOAD_URL = f"https://github.com/EvilDrPurple/AutoInventory/releases/latest/download/AutoInventory-Installer{WIN7}.exe"
INSTALLER_PATH = f"{tempfile.gettempdir()}/AutoInventory-Installer{WIN7}.exe"

THREAD_KEY = '-THREAD-'
DL_START_KEY = '-START DOWNLOAD-'
DL_END_KEY = '-END DOWNLOAD-'
IN_START_KEY = '-START INSTALL-'
IN_END_KEY = '-END INSTALL-'
THREAD_EXITING = '-THREAD EXITING-'

def the_thread(window:sg.Window):
    window.write_event_value((THREAD_KEY, DL_START_KEY), 1)
    wget.download(DOWNLOAD_URL, INSTALLER_PATH)
    
    window.write_event_value((THREAD_KEY, DL_END_KEY), 2)
    time.sleep(1)
    
    window.write_event_value((THREAD_KEY, IN_START_KEY), 3)
    os.system(f'"{INSTALLER_PATH}" /SILENT /NOCLOSEAPPLICATIONS /SUPRESSMSGBOXES /NOCANCEL')
    
    window.write_event_value((THREAD_KEY, IN_END_KEY), 4)
    os.remove(INSTALLER_PATH)
    time.sleep(2)

def main():
    sg.theme('DarkPurple4')
    sg.theme_text_color('white')
    FONT = 'Ariel 14'
    STATUS = '-STATUS-' + sg.WRITE_ONLY_KEY
    layout = [  [sg.Text('Please wait while the application updates...', font=FONT)],
                [sg.Multiline('', key=STATUS, size=(50,5))] ]
    
    window = sg.Window('AutoInventory Updater', layout, finalize=True, keep_on_top=True)
    window.start_thread(lambda: the_thread(window), (THREAD_KEY, THREAD_EXITING))
    
    while True:
        event, values = window.read(timeout=10)

        if event == sg.WIN_CLOSED:
            break
 
        if event[0] == THREAD_KEY:
            if event[1] == DL_START_KEY:
                window[STATUS].print('Downloading installer...')
            elif event[1] == DL_END_KEY:
                window[STATUS].print('Downloaded')
            elif event[1] == IN_START_KEY:
                window[STATUS].print('Installing update...')
            elif event[1] == IN_END_KEY:
                window[STATUS].print('Installed successfully!')
            elif event[1] == THREAD_EXITING:
                break

    window.close()

if __name__ == '__main__':
    main()
