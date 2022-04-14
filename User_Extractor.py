from selenium.webdriver.common.by import By


class User_extractor:

    def __init__(self, list_of_publishers_links):
        """
        """
        self.list_of_publishers_links = list_of_publishers_links
        self.records = []

    def user_extract(self, driver):
        for user_link in self.list_of_publishers_links:
            driver.get(user_link)
            driver.implicitly_wait(10)
            user_info = driver.find_elements(By.CLASS_NAME,
                                             "css-901oao css-16my406 r-18jsvk2 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0"
                                             .replace(' ', '.'))
            user_tag = driver.find_elements(By.CLASS_NAME,
                                            "css-901oao css-bfa6kz r-14j79pv r-18u37iz r-37j5jr r-a023e6 r-16dba41 "
                                            "r-rjixqe r-bcqeeo r-qvutc0 ".replace(' ', '.'))
            row = []
            try:
                row.append(user_info[0].text)
                row.append(user_tag[0].text)
                row.append(user_info[1].text)
                row.append(user_info[2].text)
            except IndexError:
                print(f"This link, {user_link} is not accessible")

            self.records.append(row)

        return self.records