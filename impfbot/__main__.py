import configparser
import re
import time

import simpleaudio as sa
from selenium import webdriver


def accept_cookies(cookies_accepted):
    if cookies_accepted:
        return True

    time.sleep(1)

    if "Wir verwenden Cookies" in driver.page_source:
        cookie_button = driver.find_element_by_css_selector("app-root > div > div > div > div.row.no-gutters.user-select-none > div.col-10.offset-1.col-md-6.offset-md-0.text-center.text-md-left > div > div:nth-child(2) > a")
        cookie_button.click()

    return True

def use_transfer_code(driver, transfer_code):
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

def request_transfer_code(driver):
    no_button = driver.find_element_by_css_selector("app-corona-vaccination > div:nth-child(2) > div > div > label:nth-child(2) > span")
    no_button.click()

def ring_alarm():
    filename = 'resources/alarm.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

parser = configparser.ConfigParser()
parser.read('resources/config.ini')

post_codes = parser.get('impfbot', 'post_codes').split(',')
transfer_codes = parser.get('impfbot', 'transfer_codes').split(',')
i = 0
appointment_found = False

driver = webdriver.Chrome("resources/chromedriver.exe")
driver.implicitly_wait(30)
driver.maximize_window()

cookies_accepted = False

while not appointment_found:
    post_code = post_codes[i]
    transfer_code = transfer_codes[i]
    driver.get("https://005-iz.impfterminservice.de/impftermine/service?plz={}".format(post_code))
    cookies_accepted = accept_cookies(cookies_accepted)

    while "Virtueller Warteraum" in driver.page_source:
        time.sleep(1)

    if re.match(r"^[0-0a-fA-F]{4}-[0-0a-fA-F]{4}-[0-0a-fA-F]{4}$", transfer_code):
        use_transfer_code(driver, transfer_code)
    else:
        request_transfer_code(driver)

    while "Bitte warten, wir suchen verfügbare Termine in Ihrer Region." in driver.page_source:
        time.sleep(1)

    if "Es wurden keine freien Termine in Ihrer Region gefunden." not in driver.page_source or "Onlinebuchung für Ihre Corona-Schutzimpfung" in driver.page_source:
        ring_alarm()
        appointment_found = True

    i = (i + 1) % len(post_codes)
    time.sleep(10)
