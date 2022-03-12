from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv
import chromedriver_autoinstaller


class User_extractor:

    def __init__(self, list_of_publishers_links, driver):
        """
        """
        self.list_of_publishers_links = list_of_publishers_links
        self.list_of_Publishers = []
        self.list_of_Following = []
        self.list_of_Followers = []
        self.user_extractor(driver)

    def user_extractor(self, driver):
        for user_link in self.list_of_publishers_links:
            driver.get(user_link)
            driver.implicitly_wait(10)
            user_info = driver.find_elements(By.CLASS_NAME,
                                             "css-901oao css-16my406 r-18jsvk2 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0".replace(
                                                 ' ', '.'))
            try:
                self.list_of_Publishers.append(user_info[0].text)
                self.list_of_Following.append(user_info[1].text)
                self.list_of_Followers.append(user_info[2].text)
            except IndexError:
                print(f"This link, {user_link} is not accessible")
