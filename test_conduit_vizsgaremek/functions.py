from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from data_for_imports import user_login
# import csv

def cookie_function(browser):
    accept_cookie_btn = browser.find_element(By.XPATH,
                                                  '//button [@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    accept_cookie_btn.click()
    time.sleep(1)


def login_function(browser):
    menu_login_btn = browser.find_element(By.LINK_TEXT, 'Sign in')
    menu_login_btn.click()
    time.sleep(2)

    email_input = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
    password_input = browser.find_element(By.XPATH, '//input[@type="password"]')
    sign_in_btn = browser.find_element(By.XPATH, '//button[contains(text(), "Sign in")]')

    email_input.send_keys(user_login['email'])
    password_input.send_keys(user_login['password'])
    sign_in_btn.click()
    menu_logout_btn = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Log out')))
    assert menu_logout_btn.is_enabled()
    # time.sleep(3)

# def new_data_input(browser):
