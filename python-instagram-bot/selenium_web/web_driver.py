from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import logging

# Create a custom logger
logger = logging.getLogger(__name__)

def create_browser() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    return webdriver.Chrome(chrome_options=chrome_options)


def check_element_exist(driver: webdriver.Chrome, path: str, by: str = 'xpath') -> bool:
    try:
        if by == 'xpath':
            driver.find_element_by_xpath(path)
        elif by == 'css':
            driver.find_element_by_css_selector(path)
        else:
            logger.info(f"Unable to check element using '{by}'")
    except NoSuchElementException:
        return False
    return True
