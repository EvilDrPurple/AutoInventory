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
UNITS = {'EACH': {'DISK', 'EACH'},
        'BTL': 'BOTTLE',
        'GAL': 'GALLON'}
WEB_SERVICE = 'firefox'

if WEB_SERVICE == 'chrome':
    CHROME_SERVICE = ChromeService(ChromeDriverManager().install())
    browser = Browser('chrome', service=CHROME_SERVICE)
else:
    browser = Browser()

wb = load_workbook(filename = f"{PATH}/{FILE}")
sheet = wb.active

log = open(f"{PATH}/log.txt", 'a')
log.truncate(0)
log.write("Log start\n\n")

def wait_for_load():
    while browser.find_by_id('loading_layer').visible:
        time.sleep(0.5)

def find_and_click(items, search_type, search_text = ''):
    for item in items:
        if search_type == 'text' and item.text == search_text or search_type == 'visible' and item.visible:
            item.click()
            break

class Item:
    def __str__(self):
        return f"{self.itemCode : <12}{self.itemDesc : <30}{self.itemCount} {self.itemUnit}"

    def parse_row(self, row):
        for cell in row:
            match cell.column_letter:
                case "A":
                    if not cell.value: return False
                    self.itemCode = cell.value.strip()
                case "B":
                    self.itemDesc = cell.value.strip()
                case "C":
                    self.itemUnit = cell.value.strip()
                    self.itemUnit = UNITS[self.itemUnit] if self.itemUnit in UNITS else self.itemUnit
                case "H":
                    if not cell.value: return False
                    self.itemCount = cell.value

        return True
    
    def enter_data(self):
        browser.find_by_id('INV_ACC_DETAIL_tbl_filter').find_by_tag('input').fill(self.itemCode)

        for td in browser.find_by_id('INV_ACC_DETAIL_tbl').find_by_tag('td'):
            if td.text and td.text in self.itemUnit:
                prev.find_by_tag('input').fill(self.itemCount)
                return True
            prev = td

        return False

if __name__ == '__main__':
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
    tags = browser.find_by_tag('h3')
    find_and_click(items=tags, search_type='text', search_text='Enterprise Office')

    wait_for_load()

    browser.find_by_text('Shortcuts').click()
    tags = browser.find_by_css('.style3')
    find_and_click(items=tags, search_type='text', search_text='Inventory')

    wait_for_load()

    # Find correct inventory sheet
    browser.find_by_css('.controls').click()
    links = browser.find_by_tag('li').links.find_by_text(FREQ)
    find_and_click(items=links, search_type='visible')
    browser.find_by_name('DATE_2').fill(DATE)
    browser.find_by_name('DATE_3').fill(DATE)
    browser.find_by_value('GO').click()

    wait_for_load()

    links = browser.find_by_name('openObject')
    find_and_click(items=links, search_type='visible')

    wait_for_load()

    # Cycle through spreadsheet and enter data
    for row in sheet.iter_rows(min_row=6, max_row=115, min_col=0, max_col=8):
        item = Item()
        if not item.parse_row(row): continue
      
        logText = f"ADDED: {item}\n" if item.enter_data() else f"\nERROR: {item}  WAS NOT FOUND\n\n"
        log.write(logText)

    log.write("\nLog closed")
    log.close()