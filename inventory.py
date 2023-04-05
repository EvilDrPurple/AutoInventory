import pathlib
import time
import config
from openpyxl import load_workbook
from splinter import Browser

browser = Browser()

URL = 'https://fedsso.yum.com/idp/startSSO.ping?PartnerSpId=https://yumph.altametrics.com/'
USER = config.USER
PASS = config.PASS
DATE = '04/02/2023'
FREQ = 'Weekly'

def wait_for_load():
    while browser.find_by_id('loading_layer').visible:
        print("Waiting...")
        time.sleep(0.5)

# Visit portal and log in
browser.visit(URL)
browser.find_by_id('userId').fill(USER)
browser.find_by_id('password').fill(PASS)
browser.find_by_id('submit').click()

# Wait for load
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
browser.find_by_name('DATE_2').fill(DATE)
browser.find_by_value('GO').click()

wait_for_load()

for link in browser.find_by_name('openObject'):
    if link.visible:
        link.click()

wait_for_load()

