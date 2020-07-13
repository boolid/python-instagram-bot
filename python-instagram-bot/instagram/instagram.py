from selenium_web.web_driver import check_element_exist
from selenium import webdriver
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

            login_buttion = self.browser.find_element_by_xpath("//button[@type='submit']")
            self.browser.execute_script("arguments[0].click();", login_buttion)
        else:
            self.browser.save_screenshot("/python-instagram-bot/screenshots/unable_to_login.png")
            raise Exception("Unable to login to website. Please check the screenshot of 'unable_to_login.png'")

        # Waiting for after login
        time.sleep(5)

        if check_element_exist(self.browser, '//button[text()="Not Now"]'):
            self.browser.find_element_by_xpath('//button[text()="Not Now"]').click()

        return True