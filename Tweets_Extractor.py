from selenium.webdriver.chrome.service import Service
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
import csv


class Tweets_extractor:
    def __init__(self, Search_term, PATH):
        self.search_term = Search_term
        self.PATH = PATH

        self.list_of_publishers = []
        self.list_hashtags = []
        self.list_users_tagged = []
        self.list_links = []
        self.list_number_reply = []
        self.list_number_retweet = []
        self.list_number_Like = []
        self.list_times = []
        self.list_images = []

    def _scroll_down_page(self, driver, last_position, num_seconds_to_load=0.5, scroll_attempt=0, max_attempts=5):
        """The function will try to scroll down the page and will check the current
        and last positions as an indicator. If the current and last positions are the same after `max_attempts`
        the assumption is that the end of the scroll region has been reached and the `end_of_scroll_region`
        flag will be returned as `True`"""
        end_of_scroll_region = False
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(num_seconds_to_load)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if curr_position == last_position:
            if scroll_attempt < max_attempts:
                end_of_scroll_region = True
            else:
                self._scroll_down_page(last_position, curr_position, scroll_attempt + 1)
        last_position = curr_position
        return last_position, end_of_scroll_region

    def _save_tweet_data_to_csv(self, records, filepath, mode='a+'):
        header = ['User', 'Handle', 'PostDate', 'TweetText', 'ReplyCount', 'RetweetCount', 'LikeCount']
        with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if mode == 'w':
                writer.writerow(header)
            if records:
                writer.writerow(records)

    def _create_webdriver_instance(self, PATH):
        options = Options()
        options.headless = True  # hide GUI
        options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
        options.add_argument("start-maximized")
        s = Service(PATH)

        driver = webdriver.Chrome(service=s)

        return driver

    def _change_page_sort(self, tab_name, driver):
        """Options for this program are `Latest` and `Top`"""
        tab = driver.find_element_by_link_text(tab_name)
        tab.click()

    def _collect_all_tweets_from_current_view(self, driver, lookback_limit=25):
        """The page is continously loaded, so as you scroll down the number of tweets returned by this function will
         continue to grow. To limit the risk of 're-processing' the same tweet over and over again, you can set the
         `lookback_limit` to only process the last `x` number of tweets extracted from the page in each iteration.
         You may need to play around with this number to get something that works for you. I've set the default
         based on my computer settings and internet speed, etc..."""
        page_cards = driver.find_elements(By.CLASS_NAME,
                                          "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l".replace(
                                              ' ', '.'))
        if len(page_cards) <= lookback_limit:
            return page_cards
        else:
            return page_cards[-lookback_limit:]

    def Return_attribute(self, attribute):
        return self.attribute

        ####     NAMES OF PUBLISHERS

    def _Extract_Names(self, driver):
        Publishers = driver.find_elements(By.CLASS_NAME,
                                          "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l".replace(
                                              ' ', '.'))

        for i in range(len(Publishers)):
            self.list_of_publishers.append(Publishers[i].text[:Publishers[i].text.index('\n')])
        return self.list_of_publishers

        ####       HASHTAGS, USERS TAGGED, LINKS

    def _Extract_hashtags_userstagged_links(self, driver):

        text_info = driver.find_elements(By.CLASS_NAME,
                                         "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0".replace(
                                             ' ', '.'))
        for i in range(len(text_info)):
            hashtag_list = text_info[i].find_elements(By.CLASS_NAME,
                                                      "css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0".replace(
                                                          ' ', '.'))
            list_ezer_hashtag = []
            list_ezer_pages = []
            list_ezer_links = []
            for element in hashtag_list:
                if '#' in element.text:
                    list_ezer_hashtag.append(element.text)
                    break
                if '@' in element.text:
                    list_ezer_pages(element.text)
                    break
                list_ezer_links.append(element.text)
            # print(list_ezer)
            self.list_hashtags.append(list_ezer_hashtag)
            self.list_users_tagged.append(list_ezer_pages)
            self.list_links.append(list_ezer_links)

            ####         NUMBERS OF REPLIES, RETWEETS AND LIKES

    def _Extract_NumReplies_retweets_likes(self, driver):

        number_info = driver.find_elements(By.CLASS_NAME,
                                           "css-1dbjc4n r-1ta3fxp r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws".replace(' ',
                                                                                                                   '.'))

        for i in range(len(number_info)):
            numbers_list = number_info[i].find_elements(By.CLASS_NAME,
                                                        "css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0".replace(
                                                            ' ', '.'))
            self.list_number_reply.append(numbers_list[0].text)
            self.list_number_retweet.append(numbers_list[1].text)
            self.list_number_Like.append(numbers_list[2].text)

        driver.quit()

        ####      DATES

    def _Extract_Dates(self, driver):

        TIMES = driver.find_elements(By.TAG_NAME, 'time')
        list_times = []
        for item in TIMES:
            time = item.get_attribute('datetime')
            time = time.replace('T', ' ')
            self.list_times.append(time.replace('Z', ' '))
        driver.quit()

        ####           NUMBER OF IMAGES

    def _Extract_Num_images(self, driver):

        list_tweet = driver.find_elements(By.CLASS_NAME,
                                          "css-1dbjc4n r-1ets6dv r-1867qdf r-1phboty r-rs99b7 r-1ny4l3l r-1udh08x r-o7ynqc r-6416eg".replace(
                                              ' ', '.'))

        for i in list_tweet:
            images_for_tweet = i.find_elements(By.TAG_NAME, "img")
            self.list_images.append(len(images_for_tweet))

        driver.quit()

    def Extract_ALL(self, filepath):
        """
        Returns a csv file which contains all the features extracted from the webpage
        """
        driver = self._create_webdriver_instance(self.PATH)
        driver.get('https://twitter.com/search?q=' + self.search_term)
        self._save_tweet_data_to_csv(None, filepath, 'w')  # create file for saving records
        last_position = None
        end_of_scroll_region = False
        unique_tweets = set()
        while not end_of_scroll_region:
            self._Extract_Names(driver)
            self._Extract_hashtags_userstagged_links(driver)
            self._Extract_NumReplies_retweets_likes(driver)
            self._Extract_Dates(driver)
            self._Extract_Num_images(driver)
            last_position, end_of_scroll_region = self._scroll_down_page(driver, last_position)

        rows = zip(self.list_of_publishers, self.list_hashtags, self.list_users_tagged, self.list_links,
                   self.list_number_reply, self.list_number_retweet, self.list_number_Like, self.list_times,
                   self.list_images)

        with open("file.csv", "w") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

        driver.quit()




