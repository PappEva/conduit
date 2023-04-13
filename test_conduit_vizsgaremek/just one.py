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

# # TC_03 Bejelentkezés tesztelése
    def test_login(self):
        login_btn = self.browser.find_element(By.LINK_TEXT, 'Sign in')
        login_btn.click()
        time.sleep(2)
        assert self.browser.current_url == 'http://localhost:1667/#/register'

        # username_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@type="password"]')
        sign_in_btn = self.browser.find_element(By.XPATH, '//button[contains(text(), "Sign in")]')

        email_input.send_keys('testuser4@gmail.com')
        password_input.send_keys('Testuser1password')
        sign_in_btn.click()
        time.sleep(2)

        logged_in_user = self.browser.find_element(By.CLASS_NAME, 'nav-link router-link-exact-active active')
        # login_ = self.browser.find_element(By.XPATH, '//div[@class="nav-item"]')
        # registration_popup_msg = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]')
        assert logged_in_user.text == 'Testuser4'
        # assert registration_popup_title.text == "Welcome!"
        # assert registration_popup_msg.text == "Your registration was successful!"