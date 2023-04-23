# Imports
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv
import allure
from functions import login_function, cookie_function, data_for_delete_function
from data_for_imports import user_registration, user_login, article, article_for_delete, bio_data_for_modify


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

    # TC_01 Adatkezelési nyilatkozat használata ########################################################################
    @allure.title('Adatkezelési nyilatkozat elfogadása')
    def test_cookie(self):
        # Van cookie panel az oldalon?
        assert len(self.browser.find_elements(By.ID, 'cookie-policy-panel')) != 0

        accept_cookie_btn = self.browser.find_element(By.XPATH,
                                                      '//button [@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        accept_cookie_btn.click()
        time.sleep(2)

        # Eltűnt a cookie panel?
        assert len(self.browser.find_elements(By.ID, 'cookie-policy-panel')) == 0

    # TC_02 Regisztráció tesztelése ####################################################################################
    @allure.title('Regisztráció új felhasználóval')
    def test_registration(self):
        cookie_function(self.browser)

        # Regisztráció gomb keresése és kattintás
        register_btn = self.browser.find_element(By.LINK_TEXT, 'Sign up')
        register_btn.click()
        time.sleep(1)
        assert self.browser.current_url == 'http://localhost:1667/#/register'

        # Tesztadatok beírása a megfelelő helyekre (data_for_imports.py fájlból)
        username_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@type="password"]')
        sign_up_btn = self.browser.find_element(By.XPATH, '//button[contains(text(), "Sign up")]')

        username_input.send_keys(user_registration['username'])
        email_input.send_keys(user_registration['email'])
        password_input.send_keys(user_registration['password'])
        sign_up_btn.click()
        time.sleep(2)

        # Regisztráció után felugró ablak kezelése és tartalmának ellenőrzése
        registration_popup_title = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
        registration_popup_msg = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]')

        assert registration_popup_title.text == "Welcome!"
        assert registration_popup_msg.text == "Your registration was successful!"

        registration_ok_button = self.browser.find_element(By.XPATH,
                                                           '//button[@class="swal-button swal-button--confirm"]')
        registration_ok_button.click()

    # TC_03 Bejelentkezés tesztelése ###################################################################################
    @allure.title('Bejelentkezés regisztrált felhasználóval')
    def test_login(self):
        # cookie_function(self.browser)

        # Bejelentkezés linkre kattintás
        menu_login_btn = self.browser.find_element(By.LINK_TEXT, 'Sign in')
        menu_login_btn.click()
        # time.sleep(1)
        assert self.browser.current_url == 'http://localhost:1667/#/login'

        # Tesztadatok beírása a megfelelő helyekre (data_for_imports.py fájlból)
        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@type="password"]')
        sign_in_btn = self.browser.find_element(By.XPATH, '//button[contains(text(), "Sign in")]')

        email_input.send_keys(user_login['email'])
        password_input.send_keys(user_login['password'])
        sign_in_btn.click()

        # Megjelent a belépés utáni felhasználói felületen a logout link?
        # menu_logout_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Log out')))
        # menu_logout_btn = WebDriverWait(self.browser, 15).until(
        #     EC.presence_of_all_elements_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
        # menu_logout_btn = WebDriverWait(self.browser, 15).until(
        #     EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Log out')))
        # assert menu_logout_btn.is_enabled()
        profile = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/@Testuser4/"]')))
        assert profile.text == "Testuser4"

    # TC_04 Adatok listázása ##########################################################################################
    @allure.title('Adatok listázása')
    def test_datalist(self):
        cookie_function(self.browser)
        login_function(self.browser)

        # Tag adatok listába gyűjtése
        tags = self.browser.find_elements(By.XPATH, '//div[@class="sidebar"]//div[@class="tag-list"]//a')
        popular_tags_list = []
        for tag in tags:
            popular_tags_list.append(tag.text)
        print(popular_tags_list)

        # Lista létrejött és nem üres?
        assert popular_tags_list != 0

    # TC_05 Több oldalas lista bejárása ################################################################################
    @allure.title('Több oldalas lista bejárása')
    def test_list_walkthrough(self):
        cookie_function(self.browser)
        login_function(self.browser)

        # Oldalszám gombok végigkattintása és listába gyűjtés
        page_btns = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="page-link"]')))
        page_num_list = []
        for page_num in page_btns:
            page_num.click()
            time.sleep(1)
            page_num_list.append(page_btns)

        # Oldalszám lista elemszáma megegyezik az aktuális oldalszámmal (string -> int alakítás) és az oldalak számával
        actual_page = self.browser.find_element(By.CSS_SELECTOR, 'li[class="page-item active"]')
        assert len(page_num_list) == int(actual_page.text)
        assert len(page_num_list) == len(page_btns)

    # TC_06 Új adat bevitel - New Article ##############################################################################
    @allure.title('Új adat bevitel, új cikk')
    def test_new_data(self):
        cookie_function(self.browser)
        login_function(self.browser)

        # New article link kattintása
        menu_new_article_link = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
        menu_new_article_link.click()
        # time.sleep(3)

        # Tesztadatok beírása a megfelelő helyekre (data_for_imports.py fájlból)
        article_title_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Article Title"]')))
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

        # New article létrejöttének ellenőrzése
        new_article_title = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

        assert new_article_title.text == (article['title'])
        assert self.browser.current_url == 'http://localhost:1667/#/articles/' + (article['url'])

    # # TC_07 Ismételt és sorozatos adatbevitel adatforrásból ##########################################################
    @allure.title('Ismételt és sorozatos adatbevitel adatforrásból, kommentek')
    def test_repeated_data_from_file(self):
        cookie_function(self.browser)
        login_function(self.browser)
        time.sleep(1)

        # Keresek egy cikket, amihez kommenteket írok
        article_to_comment = self.browser.find_element(By.XPATH, "//h1[contains(text(), 'Lorem ipsum dolor sit amet')]")
        # article_to_comment = WebDriverWait(self.browser, 10).until(
        #     EC.presence_of_all_elements_located((By.XPATH, "//h1[contains(text(), 'Lorem ipsum dolor sit amet')]")))
        article_to_comment.click()
        time.sleep(2)

        comment_box = self.browser.find_element(By.XPATH, '//textarea[@placeholder="Write a comment..."]')

        # Adatforrás megnyitása, beolvasása, és az adatok betöltése
        # with open('comments.csv', 'r') as file:
        with open('test_conduit_vizsgaremek/comments.csv', 'r') as file:
            comment_rows = csv.reader(file, delimiter=',')
            for row in comment_rows:
                comment_box.send_keys(row[0])
                self.browser.find_element(By.XPATH, '//button[@class="btn btn-sm btn-primary"]').click()
                time.sleep(1)

            # Oldalon megjelent kommentek szövegének listába olvasása
            comments_list = self.browser.find_elements(By.XPATH, "//p[@class='card-text']")
            comments_texts = []
            for i in comments_list:
                comments_texts.append(i.text)

            # Elküldött kommentek és az előző lista összehasonlítása
            for row in comment_rows:
                assert row[0] in comments_texts

    # TC_08 Meglévő adat módosítás (user profil bio módosítása) ########################################################
    @allure.title('Meglévő adat módosítás (user profil bio)')
    def test_modify_data(self):
        cookie_function(self.browser)
        login_function(self.browser)

        # User profil oldalon lévő bio szövegének keresése és mentése
        url_user_profile = ('http://localhost:1667/#/@' + (user_login["username"]) + '/')
        self.browser.get(url_user_profile)
        menu_settings_link = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Settings')))
        user_bio_text_before = self.browser.find_element(By.TAG_NAME, 'p').text

        # Settings oldal betöltése
        menu_settings_link.click()
        # time.sleep(3)
        print(self.browser.current_url)

        # "Short bio about you" adat módosítása
        short_bio_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Short bio about you"]')))
        short_bio_input.clear()
        short_bio_input.send_keys(bio_data_for_modify['text'])
        update_settings_btn = self.browser.find_element(By.XPATH,
                                                        '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        update_settings_btn.click()
        time.sleep(4)

        # Popup ablak kezelése
        update_successful_popup = self.browser.find_element(By.XPATH,
                                                            '//button[@class="swal-button swal-button--confirm"]')
        update_successful_popup.click()

        # User profil oldalon lévő bio új szövegének ellenőrzése
        url_user_profile = ('http://localhost:1667/#/@' + (user_login["username"]) + '/')
        self.browser.get(url_user_profile)
        time.sleep(2)
        user_bio_text_after = self.browser.find_element(By.TAG_NAME, 'p').text
        # print(user_bio_text_after)

        assert user_bio_text_before != user_bio_text_after
        assert user_bio_text_after == (bio_data_for_modify['text'])

    # # TC_09 Adat vagy adatok törlése #############################################################################
    @allure.title('Adat törlése, cikk')
    def test_delete_article(self):

        # Bejelentkezés, új bejegyzés létrehozása (data_for_imports.py fájlból)
        cookie_function(self.browser)
        login_function(self.browser)
        data_for_delete_function(self.browser)

        # A törlésre szánt cikk betöltése
        home_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
        home_btn.click()
        time.sleep(2)
        article_title_to_delete = self.browser.find_element(By.XPATH, "//h1[contains(text(), 'Ez a cikk nem kell')]")
        article_title_to_delete.click()
        time.sleep(2)

        # Törlés gombra kattintás
        delete_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-outline-danger btn-sm"]')))
        delete_btn.click()
        time.sleep(1)

        # Eltűnt az oldalról létrehozott, majd törölt cikk?
        home_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
        home_btn.click()
        assert len(self.browser.find_elements(By.PARTIAL_LINK_TEXT, f'{article_for_delete["title"]}')) == 0

    # TC_10 Adatok lementése felületről ############################################################################
    @allure.title('Adatok lementése felületről, tag lista')
    def test_collect_data(self):
        cookie_function(self.browser)
        login_function(self.browser)

        # Tag adatok begyűjtése listába
        tags_on_page = self.browser.find_elements(By.XPATH, '//div[@class="sidebar"]//div[@class="tag-list"]//a')
        popular_tags_list = []
        for tag in tags_on_page:
            popular_tags_list.append(tag.text)
        assert popular_tags_list != 0
        time.sleep(2)

        # Lista fájlba mentése, soronként egy tag
        with open('collected_tag_list.csv', 'w') as csvfile:
            # with open('/test_conduit_vizsgaremek/collected_tag_list.csv', 'w') as csvfile:
            for row in popular_tags_list:
                csvfile.write(row + "\n")

        # Létrejött fájl tartalmának visszaolvasása listába (soremelés törléssel)
        list_from_file = []
        with open('collected_tag_list.csv', 'r') as saved_content:
            # with open('/test_conduit_vizsgaremek/collected_tag_list.csv', 'r') as saved_content:
            for row in saved_content:
                list_from_file.append(row.rstrip())
        # print(list_from_file)

        # Fájlból visszaolvasott lista és az oldalról eredetileg begyűjtött lista összehasonlítása ellenőrzésként
        assert list_from_file == popular_tags_list

    # TC_11 Kijelentkezés ##############################################################################################
    @allure.title('Kijelentkezés')
    def test_logout(self):
        cookie_function(self.browser)
        login_function(self.browser)

        # Kilépés gomb azonosítása és kattintás
        menu_logout_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Log out')))
        menu_logout_btn.click()
        time.sleep(2)

        # Megjelent újra a login gomb?
        menu_login_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Sign in')))

        assert menu_login_btn.is_enabled()
