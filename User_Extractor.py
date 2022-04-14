from selenium.webdriver.common.by import By
import logging


class User_extractor:

    def __init__(self, list_of_publishers_links):
        """
        """
        self.list_of_publishers_links = list_of_publishers_links
        self.records = []

    def user_extract(self, driver):
        for user_link in self.list_of_publishers_links:
            try:
                driver.get(user_link)
                driver.implicitly_wait(10)
                user_info = driver.find_elements(By.CLASS_NAME,
                                                 "css-901oao css-16my406 r-18jsvk2 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0"
                                                 .replace(' ', '.'))
                if len(user_info) == 0:
                    logging.error(f"the scraping of time of the user_info failed")
                else:
                    logging.info(f"the scraping of time of the user_info succeed")
                user_tag = driver.find_elements(By.CLASS_NAME,
                                                "css-901oao css-bfa6kz r-14j79pv r-18u37iz r-37j5jr r-a023e6 "
                                                "r-16dba41 r-rjixqe r-bcqeeo r-qvutc0".replace(' ', '.'))
                if len(user_tag) == 0:
                    logging.error(f"the scraping of time of the user_tag failed")
                else:
                    logging.info(f"the scraping of time of the user_tag succeed")
                row = [user_info[0].text, user_tag[0].text, user_info[1].text, user_info[2].text]
                self.records.append(row)
            except IndexError:
                logging.error(f"the scraping of {user_link} is not accessible")
                print(f"This link, {user_link} is not accessible")

        return self.records
