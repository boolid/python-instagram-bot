from selenium_web.web_driver import create_browser
from instagram.instagram import Instagram
import logging

logging.basicConfig(level=logging.DEBUG)
browser = create_browser()

instagram = Instagram("username", "password", browser)
instagram.login()