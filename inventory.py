import pathlib
import time
import config
from openpyxl import load_workbook
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

URL = 'https://fedsso.yum.com/idp/startSSO.ping?PartnerSpId=https://yumph.altametrics.com/'
USER = config.USER
PASS = config.PASS
DATE = '04/02/2023'
FREQ = 'Weekly'
PATH = pathlib.Path(__file__).parent.resolve().__str__()
FILE = 'march 27-april 2.xlsx'
DICT = {'EACH': {'DISK', 'EACH'},
        'BTL': 'BOTTLE',
        'GAL': 'GALLON'}
WEB_SERVICE = 'firefox'

if WEB_SERVICE == 'chrome':
    CHROME_SERVICE = ChromeService(ChromeDriverManager().install())
    browser = Browser('chrome', service=CHROME_SERVICE)
else:
    browser = Browser()

wb = load_workbook(filename = PATH + '/' + FILE)
sheet = wb.active

def wait_for_load():
    while browser.find_by_id('loading_layer').visible:
        time.sleep(0.5)

# Visit portal and log in
browser.visit(URL)
browser.driver.maximize_window()
browser.find_by_id('userId').fill(USER)
browser.find_by_id('password').fill(PASS)
browser.find_by_id('submit').click()

# Wait for redirect
while not browser.url.endswith('erslaunch-app'):
    time.sleep(1)

# Navigate to inventory page
for tag in browser.find_by_tag('h3'):
    if tag.text == "Enterprise Office":
        tag.click()
        break

wait_for_load()

browser.find_by_text('Shortcuts').click()
for tag in browser.find_by_css('.style3'):
    if tag.text == "Inventory":
        tag.click()
        break

wait_for_load()

# Find correct inventory sheet
browser.find_by_css('.controls').click()
for link in browser.find_by_tag('li').links.find_by_text(FREQ):
    if link.visible: 
        link.click()
        break
browser.find_by_name('DATE_2').fill(DATE)
browser.find_by_name('DATE_3').fill(DATE)
browser.find_by_value('GO').click()

wait_for_load()

for link in browser.find_by_name('openObject'):
    if link.visible: 
        link.click()
        break

wait_for_load()

log = open('log.txt', 'a')
log.truncate(0)
log.write("Log start\n\n")

# Cycle through spreadsheet and enter data
for row in sheet.iter_rows(min_row=6, max_row=115, min_col=0, max_col=8):
    skip = False
    for cell in row:
        match cell.column_letter:
            case "A":
                if cell.value is None: 
                    skip = True
                    break
                itemCode = cell.value.strip()
            case "B":
                itemDesc = cell.value.strip()
            case "C":
                itemUnit = cell.value.strip()
                itemUnit = DICT[itemUnit] if itemUnit in DICT else itemUnit
            case "H":
                if cell.value is None: 
                    skip = True
                    break
                itemCount = cell.value
    if skip: continue
    
    browser.find_by_id('INV_ACC_DETAIL_tbl_filter').find_by_tag('input').fill(itemCode)
    found = False
    logString = f"{itemCode : <12}{itemDesc : <30}{itemCount} {itemUnit}"
    for td in browser.find_by_id('INV_ACC_DETAIL_tbl').find_by_tag('td'):
        if td.text != "" and td.text in itemUnit:
            prev.find_by_tag('input').fill(itemCount)
            log.write(f"ADDED: {logString}\n")
            found = True
            break
        prev = td
    if not found: log.write(f"\nERROR: {logString}  WAS NOT FOUND\n\n")

log.write("\nLog closed")
log.close()