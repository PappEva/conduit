from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
import time

# import csv
# from FUNCTIONS import ......
# from ADATOK import .......

# service = Service(executable_path='c:\_automata\install\chromedriver.exe')
service = Service(executable_path=ChromeDriverManager().install())

options = Options()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=service, options=options)

URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()
time.sleep(2)

# TC_01 Adatkezelési nyilatkozat használata

# id=cookie-policy-panel látható?
accept_cookie_btn = browser.find_element(By.XPATH,
                                         '//button [@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
accept_cookie_btn.click()
# id=cookie-policy-panel látható? nem. OK.
# WebDriverWait(browser, 2).until_not(EC.presence_of_element_located((By.ID, 'cookie-policy-panel')))
time.sleep(2)

# TC_02 Regisztráció tesztelése

register_btn = browser.find_element(By.LINK_TEXT, 'Sign up')
register_btn.click()
time.sleep(2)
assert browser.current_url == 'http://localhost:1667/#/register'

username_input = browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
email_input = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
password_input = browser.find_element(By.XPATH, '//input[@type="password"]')
sign_up_btn = browser.find_element(By.XPATH, '//button[contains(text(), "Sign up")]')

username_input.send_keys('Testuser3')
# username_input.send_keys(testuser["username"]) !!! TESZTADAT IMPORT-ra átírni
email_input.send_keys('testuser3@gmail.com')
password_input.send_keys('Testuser1password')
sign_up_btn.click()
time.sleep(2)

registration_popup_title = browser.find_element(By.XPATH, '//div[@class="swal-title"]')
registration_popup_msg = browser.find_element(By.XPATH, '//div[@class="swal-text"]')
assert registration_popup_title.text == "Welcome!"
assert registration_popup_msg.text == "Your registration was successful!"

# TC_03 Bejelentkezés tesztelése
# login_btn = browser.find_element(By.LINK_TEXT, 'Sign in')
# login_btn.click()
# time.sleep(2)
# assert browser.current_url == 'http://localhost:1667/#/login'

# TC_04 Adatok listázása

# TC_05 Több oldalas lista bejárása

# TC_06 Új adat bevitel

# TC_07 Ismételt és sorozatos adatbevitel adatforrásból

# TC_08 Meglévő adat módosítás

# TC_09 Adat vagy adatok törlése

# TC_10 Adatok lementése felületről

# TC_11 Kijelentkezés
