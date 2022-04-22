from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from Config import *


def create_webdriver_instance():
    """
    returns a Webdriver object which will navigate through the webpages and extract the data we want
    """
    options = Options()
    options.headless = False  # hide GUI
    options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
    options.add_argument("start-maximized")

    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome(options=options)
    return driver


def initialize_driver(search_term):
    """
    initialize the wanted page by the self._create_webdriver_instance() method to generate the webdriver
    """
    driver = create_webdriver_instance()
    driver.get(URL + search_term)
    driver.implicitly_wait(10)

    return driver