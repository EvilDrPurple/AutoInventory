import os
import sys
import tempfile
import time

import PySimpleGUI as sg
import wget

WIN7 = '-win7' if sys.argv[1] == 'True' else ''

DOWNLOAD_URL = f"https://github.com/EvilDrPurple/AutoInventory/releases/latest/download/AutoInventory-Installer{WIN7}.exe"
INSTALLER_PATH = f"{tempfile.gettempdir()}/AutoInventory-Installer{WIN7}.exe"

THREAD_KEY = '-THREAD-'
DL_START_KEY = '-START DOWNLOAD-'
DL_END_KEY = '-END DOWNLOAD-'
IN_START_KEY = '-START INSTALL-'
IN_END_KEY = '-END INSTALL-'
THREAD_EXITING = '-THREAD EXITING-'

DICT = {
    DL_START_KEY: 'Downloading installer...',
    DL_END_KEY: 'Downloaded',
    IN_START_KEY: 'Installing update...',
    IN_END_KEY: 'Installed successfully!'
}

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
            if event[1] in DICT:
                window[STATUS].print(DICT[event[1]])
            elif event[1] == THREAD_EXITING:
                break

    window.close()

if __name__ == '__main__':
    main()
