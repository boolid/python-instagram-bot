from instagram.errors import AuthError, UnknownError, FindError
from selenium import webdriver
from selenium_web.web_driver import check_element_exist
from selenium.webdriver import ActionChains
import urllib
import time
import logging

# Create a custom logger
logger = logging.getLogger(__name__)


class Instagram:
    def __init__(self, username, password, browser: webdriver.Chrome):
        self.username = username
        self.password = password
        self.browser = browser

    def login(self) -> bool:
        self.browser.get("https://www.instagram.com/")

        # Waiting for Login Screen to appear
        time.sleep(5)

        if check_element_exist(self.browser, "input[name='username']", by='css'):
            username_input = self.browser.find_element_by_css_selector("input[name='username']")
            username_input.send_keys(self.username)
            password_input = self.browser.find_element_by_css_selector("input[name='password']")
            password_input.send_keys(self.password)

            login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
            self.browser.execute_script("arguments[0].click();", login_button)

            # Checking login error
            if check_element_exist(self.browser, 'slfErrorAlert', by='id'):
                raise AuthError("Invalid password and username")
        else:
            self.browser.save_screenshot("/python-instagram-bot/screenshots/unable_to_login.png")
            raise UnknownError("Unable to login to website. Please check the screenshot of 'unable_to_login.png'")

        # Waiting for after login
        # TODO: Find better method of doing this because this might not work
        time.sleep(5)

        if check_element_exist(self.browser, '//button[text()="Not Now"]'):
            self.browser.find_element_by_xpath('//button[text()="Not Now"]').click()

        return True

    def logout(self) -> bool:
        profile_attribute = f"""//img[@alt="{self.username}'s profile picture"]"""
        if check_element_exist(self.browser, profile_attribute, by='xpath'):
            profile_element = self.browser.find_element_by_xpath(profile_attribute)
            self.browser.execute_script("arguments[0].click();", profile_element)

            logout_attribute = "//div[contains(text(), 'Log Out')]"
            if check_element_exist(self.browser, logout_attribute, by='xpath'):
                logout_element = self.browser.find_elements_by_xpath(logout_attribute)
                logout_element[0].click()
            else:
                raise FindError("Unable to find log out button after profile click")
        else:
            raise FindError("Unable to find profile on right top corner")
        return True

    def _visit_explore_tags(self, search_value: str) -> bool:
        search_value_with_hash_tag = search_value if search_value[0] == '#' else '#'+search_value
        search_value_without_hash_tag = search_value.replace('#', '') if search_value[0] == '#' else search_value

        # Getting the search bar
        if check_element_exist(self.browser, "input[placeholder='Search']", by='css'):
            search_bar_element = self.browser.find_element_by_css_selector("input[placeholder='Search']")

            # sending keys
            search_bar_element.clear()
            search_bar_element.send_keys(search_value_with_hash_tag)

            # find things
            time.sleep(2)
            if check_element_exist(self.browser, '//a[@href="/explore/tags/'+search_value_without_hash_tag+'/"]', by='xpath'):
                searched_element = self.browser.find_element_by_xpath('//a[@href="/explore/tags/'+search_value_without_hash_tag+'/"]')
                searched_element.click()
            else:
                raise FindError("Unable to find tag from search drop-down")
        else:
            raise FindError("Unable to find search bar")

        return True

    def _scrape_image_from_explore(self):
        """
            Scrapping Images in the explore page.
        """
        images = self.browser.find_elements_by_xpath("//img")

        # TODO: This might be change later on
        # Poping first image as it's a picture for the story view
        images.pop(0)

        i = 0
        for image in images:
            if i > 3:
                return i

            # TODO: Maybe try to save image?
            link_to_image = image.get_attribute('src')
            urllib.request.urlretrieve(link_to_image, f"scrape_image_{i}.jpg")

            link = image.find_element_by_xpath('./../../..')
            i += 1
            if 'https://www.instagram.com' in link.get_attribute('href'):
                # Clicking the image
                ActionChains(self.browser).click(link).perform()

                # Get name of the profile (Is this really important?)


                # Closing the button
                close_button = 'svg[aria-label="Close"]'
                close_button_element = self.browser.find_element_by_css_selector(close_button)
                close_button_element.click()
