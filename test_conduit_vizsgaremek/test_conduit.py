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

class TestConduit(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = 'http://localhost:1667/#/'
        self.browser.get(URL)
        self.browser.maximize_window()
        time.sleep(2)

    def teardown_method(self):
        self.browser.quit()

# TC_01 Adatkezelési nyilatkozat használata
    def test_cookie(self):
        accept_cookie_btn = self.browser.find_element(By.XPATH,
                                                      '//button [@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        accept_cookie_btn.click()
        # cookie_accept = self.browser.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")
        # assert cookie_accept["value"] == "accept"
        time.sleep(2)

        # try to find cookie panel
        assert len(self.browser.find_elements(By.ID, 'cookie-policy-panel')) == 0

# TC_02 Regisztráció tesztelése
#     def test_register(self):
#         register_btn = self.browser.find_element(By.LINK_TEXT, 'Sign up')
#         register_btn.click()
#         time.sleep(2)
#         assert self.browser.current_url == 'http://localhost:1667/#/register'
#
#         username_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
#         email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
#         password_input = self.browser.find_element(By.XPATH, '//input[@type="password"]')
#         sign_up_btn = self.browser.find_element(By.XPATH, '//button[contains(text(), "Sign up")]')
#
#         username_input.send_keys('Testuser4')
#         email_input.send_keys('testuser4@gmail.com')
#         password_input.send_keys('Testuser1password')
#         sign_up_btn.click()
#         time.sleep(2)
#
#         registration_popup_title = self.browser.find_element(By.XPATH, '//div[@class="swal-title"]')
#         registration_popup_msg = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]')
#         assert registration_popup_title.text == "Welcome!"
#         assert registration_popup_msg.text == "Your registration was successful!"
#
# # TC_03 Bejelentkezés tesztelése
#     def test_login(self):
#         login_btn = self.browser.find_element(By.LINK_TEXT, 'Sign in')
#         login_btn.click()
#         time.sleep(2)
#         assert self.browser.current_url == 'http://localhost:1667/#/register'
#
#         # username_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
#         email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
#         password_input = self.browser.find_element(By.XPATH, '//input[@type="password"]')
#         sign_up_btn = self.browser.find_element(By.XPATH, '//button[contains(text(), "Sign up")]')
#
#         email_input.send_keys('testuser4@gmail.com')
#         password_input.send_keys('Testuser1password')
#         sign_up_btn.click()
#         time.sleep(2)
#
#         registration_popup_title = self.browser.find_element(By.XPATH, '//div[@class="swal-title"]')
#         registration_popup_msg = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]')

    def test_login(self):
        login_btn = self.browser.find_element(By.LINK_TEXT, 'Sign in')
        login_btn.click()
        time.sleep(1)
        assert self.browser.current_url == 'http://localhost:1667/#/login'

        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@type="password"]')
        sign_in_btn = self.browser.find_element(By.XPATH, '//button[contains(text(), "Sign in")]')

        email_input.send_keys('testuser4@gmail.com')
        password_input.send_keys('Testuser1password')
        sign_in_btn.click()
        time.sleep(5)

        logged_in_user = self.browser.find_element(By.XPATH, '//a [@href="#/@Testuser4/" and @class="nav-link"]')
        assert logged_in_user.text == 'Testuser4'

#
# # TC_04 Adatok listázása
#
# # TC_05 Több oldalas lista bejárása
#
# # TC_06 Új adat bevitel
#
# # TC_07 Ismételt és sorozatos adatbevitel adatforrásból
#
# # TC_08 Meglévő adat módosítás
#
# # TC_09 Adat vagy adatok törlése
#
# # TC_10 Adatok lementése felületről

# TC_11 Kijelentkezés
