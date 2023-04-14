from selenium.webdriver.common.by import By
import time
from data_for_imports import user_login
# import csv


def loginx(browser):
    menu_login_btn = browser.find_element(By.LINK_TEXT, 'Sign in')
    menu_login_btn.click()
    time.sleep(2)

    email_input = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
    password_input = browser.find_element(By.XPATH, '//input[@type="password"]')
    sign_in_btn = browser.find_element(By.XPATH, '//button[contains(text(), "Sign in")]')

    email_input.send_keys(user_login['email'])
    password_input.send_keys(user_login['password'])
    # email_input.send_keys('testuser4@gmail.com')
    # password_input.send_keys('Testuser1password')
    sign_in_btn.click()
    time.sleep(3)

# def new_data_input(browser):
