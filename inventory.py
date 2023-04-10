import pathlib
import re
import time
from datetime import datetime

import config
from openpyxl import load_workbook
#from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from splinter import Browser
#from webdriver_manager.chrome import ChromeDriverManager

URL = 'https://fedsso.yum.com/idp/startSSO.ping?PartnerSpId=https://yumph.altametrics.com/'
USER = config.USER
PASS = config.PASS
FREQ = 'Weekly'
PATH = pathlib.Path(__file__).parent.resolve().__str__()
FILE = 'march 27-april 2.xlsx'
UNITS = {'EACH': {'DISK', 'EACH'},
        'BTL': 'BOTTLE',
        'GAL': 'GALLON'}
MIN_ROW = 6
MAX_ROW = 115
NEW_INV = True
LEGACY = False
BROWSER_NAME = 'firefox'


def get_date():
    date = input("Enter inventory date (mm/dd/yyyy): ")

    while not re.search('^(1[0-2]|0?[1-9])/(0?[1-9]|[1-2]\d|3[0-1])/\d{4}$', date):
        print('Invalid date')
        date = input("Enter inventory date (mm/dd/yyyy): ")

    return date


def wait_for_load():
    while browser.find_by_id('loading_layer').visible:
        time.sleep(0.5)


def find_and_click(items, search_type, search_text=''):
    for item in items:
        if (
            search_type == 'text' and item.text == search_text
            or search_type == 'visible' and item.visible
        ):
            item.click()
            return True
        
    return False


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
                    self.itemDesc = cell.value.strip().replace('\t', '')
                    # Adjustment for Pepsi gallons
                    self.itemCode = 'V62 Syrup' if self.itemDesc == 'BNB PEPSI 5 GL SYRUP' else self.itemCode
                    self.itemCode = 'V65 Syrup' if self.itemDesc == 'BNB PEPSI 3 GL SYRUP' else self.itemCode
                case "C":
                    self.itemUnit = cell.value.strip()
                    # Adjustment for oregano
                    self.itemUnit = 'CASE' if self.itemCode == '74727' else self.itemUnit
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
    log = open(f"{PATH}/log.txt", 'a')
    log.truncate(0)
    log.write(f"{datetime.now():%A %B %-d, %Y %-I:%M %p}\n")
    log.write('Log start\n\n')

    wb = load_workbook(filename=f"{PATH}/{FILE}", read_only=True)
    sheet = wb.active

    DATE = get_date()

    if LEGACY:
        CHROME_SERVICE = ChromeService(executable_path=f"{PATH}/chromedriver_win32/chromedriver")
        browser = Browser('chrome', service=CHROME_SERVICE)
    else:
        browser = Browser(BROWSER_NAME)

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
    
    if NEW_INV:
        # Add new inventory sheet
        browser.find_by_id('ADD_ACTION').click()
        browser.find_by_css('.selectBox-arrow').last.click()
        links = browser.find_by_tag('li').links.find_by_text(FREQ)
        find_and_click(items=links, search_type='visible')
        browser.fill('DATE_1', DATE)
        browser.find_by_value('Add').click()
    else:
        # Find correct inventory sheet
        browser.find_by_css('.controls').click()
        links = browser.find_by_tag('li').links.find_by_text(FREQ)
        find_and_click(items=links, search_type='visible')
        browser.fill('DATE_2', DATE)
        browser.fill('DATE_3', DATE)
        browser.find_by_value('GO').click()

        wait_for_load()

        links = browser.find_by_name('openObject')
        find_and_click(items=links, search_type='visible')

    wait_for_load()

    # Cycle through spreadsheet and enter data
    for row in sheet.iter_rows(min_row=MIN_ROW, max_row=MAX_ROW, min_col=0, max_col=8):
        item = Item()
        if not item.parse_row(row): continue

        logText = f"ADDED: {item}\n" if item.enter_data() else f"\nERROR: {item}  WAS NOT FOUND\n\n"
        log.write(logText)

    log.write("\nLog closed")
    log.close()