from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from data_for_imports import user_login, article_for_delete


def cookie_function(browser):
    accept_cookie_btn = browser.find_element(By.XPATH,
                                             '//button [@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    accept_cookie_btn.click()
    time.sleep(3)


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
    time.sleep(3)
    menu_logout_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Log out')))
    assert menu_logout_btn.is_enabled()


def data_for_delete_function(browser):
    menu_new_article_link = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
    menu_new_article_link.click()

    article_title_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Article Title"]')))
    article_about_input = browser.find_element(By.XPATH, '//input[@placeholder="What\'s this article about?"]')
    article_text_input = browser.find_element(By.XPATH,
                                              '//textarea[@placeholder="Write your article (in markdown)"]')
    article_tags_input = browser.find_element(By.CSS_SELECTOR, 'input.ti-new-tag-input')
    publish_article_btn = browser.find_element(By.XPATH, '//button[@type="submit"]')

    article_title_input.send_keys(article_for_delete['title'])
    article_about_input.send_keys(article_for_delete['about'])
    article_text_input.send_keys(article_for_delete['text'])
    article_tags_input.send_keys(article_for_delete['tags'])
    publish_article_btn.click()
    time.sleep(2)
