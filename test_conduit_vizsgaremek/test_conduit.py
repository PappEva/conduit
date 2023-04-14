from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

# import csv
from functions import loginx
from data_for_imports import user_login, article


class TestConduit(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
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
        time.sleep(2)

        # try to find cookie panel
        assert len(self.browser.find_elements(By.ID, 'cookie-policy-panel')) == 0

    # TC_02 Regisztráció tesztelése
    def test_registration(self):
        register_btn = self.browser.find_element(By.LINK_TEXT, 'Sign up')
        register_btn.click()
        time.sleep(2)
        assert self.browser.current_url == 'http://localhost:1667/#/register'

        username_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@type="password"]')
        sign_up_btn = self.browser.find_element(By.XPATH, '//button[contains(text(), "Sign up")]')

        username_input.send_keys(user_login['username'])
        email_input.send_keys(user_login['email'])
        password_input.send_keys(user_login['password'])
        sign_up_btn.click()
        time.sleep(2)

        registration_popup_title = self.browser.find_element(By.XPATH, '//div[@class="swal-title"]')
        registration_popup_msg = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]')
        assert registration_popup_title.text == "Welcome!"
        assert registration_popup_msg.text == "Your registration was successful!"

    # TC_03 Bejelentkezés tesztelése OK

    def test_login(self):
        menu_login_btn = self.browser.find_element(By.LINK_TEXT, 'Sign in')
        menu_login_btn.click()
        time.sleep(1)
        assert self.browser.current_url == 'http://localhost:1667/#/login'

        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@type="password"]')
        sign_in_btn = self.browser.find_element(By.XPATH, '//button[contains(text(), "Sign in")]')

        email_input.send_keys(user_login['email'])
        password_input.send_keys(user_login['password'])
        sign_in_btn.click()
        time.sleep(3)

        logged_in_user = self.browser.find_element(By.XPATH, '//a [@href="#/@Testuser4/" and @class="nav-link"]')
        assert logged_in_user.text == 'Testuser4'
        # assert - általánosabb elemre kellene ellenőrizni: log out, settings, your feed v new article

    # TC_04 Adatok listázása OK
    def test_datalist(self):
        loginx(self.browser)

        # adatok listázása
        tags = self.browser.find_elements(By.XPATH, '//div[@class="sidebar"]//div[@class="tag-list"]//a')
        popular_tags_list = []
        for tag in tags:
            popular_tags_list.append(tag.text)
        print(popular_tags_list)
        assert popular_tags_list != 0

    # # TC_05 Több oldalas lista bejárása OK
    def test_list_walkthrough(self):
        loginx(self.browser)

        page_num_list = self.browser.find_elements(By.XPATH, '//li[@class="page-link"]')

        for page_num in page_num_list:
            page_num.click()
            actual_page = self.browser.find_element(By.CSS_SELECTOR, 'li[class="page-item active"]')
            assert page_num.text == actual_page.text

    # # TC_06 Új adat bevitel - New Article
    def test_new_data(self):
        loginx(self.browser)

        menu_new_article_link = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
        menu_new_article_link.click()
        time.sleep(3)

        article_title_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Article Title"]')
        article_about_input = self.browser.find_element(By.XPATH, '//input[@placeholder="What\'s this article about?"]')
        article_text_input = self.browser.find_element(By.XPATH,
                                                       '//textarea[@placeholder="Write your article (in markdown)"]')
        article_tags_input = self.browser.find_element(By.CSS_SELECTOR, 'input.ti-new-tag-input')
        publish_article_btn = self.browser.find_element(By.XPATH, '//button[@type="submit"]')

        article_title_input.send_keys(article['title'])
        article_about_input.send_keys(article['about'])
        article_text_input.send_keys(article['text'])
        article_tags_input.send_keys(article['tags'])
        publish_article_btn.click()

        # article_title_input.send_keys('Tavaszi gyerekdal')
        # article_about_input.send_keys('dalszöveg')
        # article_text_input.send_keys(
        #     'Tavaszi szél vizet áraszt, virágom, virágom. Minden madár társat választ, virágom, virágom.')
        # article_tags_input.send_keys('gyerek', 'dalok')
        # publish_article_btn.click()

        time.sleep(1)
        assert self.browser.current_url == 'http://localhost:1667/#/articles/' + (article['url'])
        # ??? vagy az oldalon kellene keresni valamire

    # # TC_07 Ismételt és sorozatos adatbevitel adatforrásból
    # def test_repeated_data_from_file
    # posztok vagy kommentek
    #
    # # TC_08 Meglévő adat módosítás
    # def test_modify_article(self):

    # # TC_09 Adat vagy adatok törlése
    # def test_delete_article(self):

    # # TC_10 Adatok lementése felületről
    #     def test_save_data_to_file(self):
    # #       loginx(self.browser)
    #
    #         # adatok listázása
    #         tags = self.browser.find_elements(By.XPATH, '//div[@class="sidebar"]//div[@class="tag-list"]//a')
    #         popular_tags_list = []
    #         for tag in tags:
    #             popular_tags_list.append(tag.text)
    #         print(popular_tags_list)
    #         assert popular_tags_list != 0
    #
    #         # adatok fájlba írása
    #

    # TC_11 Kijelentkezés
    def test_logout(self):
        loginx(self.browser)

        # kilépés
        menu_logout_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Log out')))
        menu_logout_btn.click()
        time.sleep(2)

        login_btn = self.browser.find_element(By.LINK_TEXT, 'Sign in')
        assert login_btn.is_enabled()
