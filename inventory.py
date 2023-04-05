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
TYPE = 'Weekly'

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

while browser.find_by_id('loading_layer').visible:
    time.sleep(0.5)
browser.find_by_text('Shortcuts').click()
browser.find_by_text('Inventory').click()

# Find correct inventory sheet