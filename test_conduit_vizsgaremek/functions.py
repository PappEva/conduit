from selenium.webdriver.common.by import By
import time
import csv

def loginx(browser):
    menu_login_btn = browser.find_element(By.LINK_TEXT, 'Sign in')
    menu_login_btn.click()
    time.sleep(1)

    email_input = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
    password_input = browser.find_element(By.XPATH, '//input[@type="password"]')
    sign_in_btn = browser.find_element(By.XPATH, '//button[contains(text(), "Sign in")]')

    email_input.send_keys('testuser4@gmail.com')
    password_input.send_keys('Testuser1password')
    sign_in_btn.click()
    time.sleep(3)

# TC_05 Több oldalas lista bejárása

# TC_06 Új adat bevitel

# TC_07 Ismételt és sorozatos adatbevitel adatforrásból

# TC_08 Meglévő adat módosítás

# TC_09 Adat vagy adatok törlése

# TC_10 Adatok lementése felületről

# TC_11 Kijelentkezés
