import configparser
import re
import time

import win32api
from selenium import webdriver


def use_transfer_code(transfer_code):
    yes_button = driver.find_element_by_css_selector("app-corona-vaccination > div:nth-child(2) > div > div > label:nth-child(1) > span")
    yes_button.click()

    transfer_code_splitted = transfer_code.split("-")

    first_input = driver.find_element_by_css_selector("app-corona-vaccination-yes > form > div:nth-child(1) > label > app-ets-input-code > div > div:nth-child(1) > label > input")
    second_input = driver.find_element_by_css_selector("app-corona-vaccination-yes > form > div:nth-child(1) > label > app-ets-input-code > div > div:nth-child(3) > label > input")
    third_input = driver.find_element_by_css_selector("app-corona-vaccination-yes > form > div:nth-child(1) > label > app-ets-input-code > div > div:nth-child(5) > label > input")
    search_button = driver.find_element_by_css_selector("app-corona-vaccination-yes > form > div:nth-child(2) > button")

    first_input.send_keys(transfer_code_splitted[0])
    second_input.send_keys(transfer_code_splitted[1])
    third_input.send_keys(transfer_code_splitted[2])
    search_button.click()

def request_transfer_code():
    no_button = driver.find_element_by_css_selector("app-corona-vaccination > div:nth-child(2) > div > div > label:nth-child(2) > span")
    no_button.click()

parser = configparser.ConfigParser()
parser.read('config.ini')

post_codes = parser.get('impfbot', 'post_codes').split(',')
transfer_codes = parser.get('impfbot', 'transfer_codes').split(',')
i = 0
appointment_found = False

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()

while not appointment_found:
    post_code = post_codes[i]
    transfer_code = transfer_codes[i]
    driver.get("https://005-iz.impfterminservice.de/impftermine/service?plz={}".format(post_code))

    while "Virtueller Warteraum" in driver.page_source:
        time.sleep(1)

    if re.match(r"^[0-0a-fA-F]{4}-[0-0a-fA-F]{4}-[0-0a-fA-F]{4}$", transfer_code):
        use_transfer_code(transfer_code)
    else:
        request_transfer_code()

    while "Bitte warten, wir suchen verfügbare Termine in Ihrer Region." in driver.page_source:
        time.sleep(1)

    if "Es wurden keine freien Termine in Ihrer Region gefunden." not in driver.page_source or "Onlinebuchung für Ihre Corona-Schutzimpfung" in driver.page_source:
        win32api.MessageBox(0, 'Es wurde ein freier Termin in {} gefunden!'.format(post_code), 'Freier Impftermin')
        appointment_found = True

    i = (i + 1) % len(post_codes)
