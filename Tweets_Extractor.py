from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv
import chromedriver_autoinstaller


class Tweets_extractor:
    """
    Create a Tweets extractor object that can be called after creating a Chrome driver object to extract
    and store in a table as many tweets as one wants, from the result's page of a specific term research on Twitter
    """

    def __init__(self, search_term, quantity_of_tweets, path_CSVfile):
        """
        Our class has 1 attribute the user need to enter: 1) the terms he wants to type in the search bar.
        and two optional attributes:
          1)How many tweets does he want to extract
        and 2) the path of the csv file in which the tweets will be saved

        There are other attributes corresponding to the different features the user can extract for each tweet
         from the page, for example, self.list_hashtags is a list of the hashtags appearing on each tweet:
         example: self.list_hashtags[i] is the list of hashtags present with the i th tweet.
         !!! However, these last attributes are empty until the user fill them with the corresponding methods !
        """
        self.search_term = search_term
        self.path_CSVfile = path_CSVfile
        self.quantity_of_tweets = quantity_of_tweets

        self.list_of_publishers = []
        self.list_of_publishers_links = set()
        self.list_hashtags = []
        self.list_users_tagged = []
        self.list_links = []
        self.list_pages_links = set()
        self.list_number_reply = []
        self.list_number_retweet = []
        self.list_number_Like = []
        self.list_times = []
        self.list_images = []
        self.list_videos = []

    def _scroll_down_page(self, driver, last_position, num_seconds_to_load=0.5, scroll_attempt=0, max_attempts=5):
        """
        The function will try to scroll down the page and will check the current
        and last positions as an indicator. If the current and last positions are the same after `max_attempts`
        the assumption is that the end of the scroll region has been reached and the `end_of_scroll_region`
        flag will be returned as `True`
        """
        end_of_scroll_region = False
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(num_seconds_to_load)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if curr_position == last_position:
            if scroll_attempt >= max_attempts:
                end_of_scroll_region = True
            else:
                self._scroll_down_page(last_position, curr_position, scroll_attempt + 1)
        last_position = curr_position
        return last_position, end_of_scroll_region

    def _save_tweet_data_to_csv(self, records, filepath, mode='w'):
        """
        create csv file with all the records
        """
        header = ['NAMES OF PUBLISHERS', 'HASHTAGS', 'USERS TAGGED', 'LINKS', 'ReplyCount', 'RetweetCount', 'LikeCount',
                  'DATES', 'NUMBER OF IMAGES']
        with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in records:
                writer.writerow(row)

    def _create_webdriver_instance(self):
        """
        returns a Webdriver object which will navigate through the webpages and extract the data we want
        """
        options = Options()
        options.headless = True  # hide GUI
        options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
        options.add_argument("start-maximized")

        chromedriver_autoinstaller.install()

        driver = webdriver.Chrome(options=options)
        return driver

    def initialize_driver(self):
        """
        initialize the wanted page by the self._create_webdriver_instance() method to generate the webdriver
        """
        driver = self._create_webdriver_instance()
        driver.get('https://twitter.com/search?q=' + self.search_term)
        driver.implicitly_wait(10)

        return driver

    def Return_attribute(self, attribute):
        """
        return attribute
        """
        return getattr(self, attribute)

    def _Extract_Names_and_links(self, driver):
        """
        Returns a list of the names of the different tweet publishers
        """
        Publishers = driver.find_elements(By.CLASS_NAME,
                                          "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l".replace(
                                              ' ', '.'))
        for i in range(len(Publishers)):
            self.list_of_publishers_links.add(Publishers[i].get_attribute('href'))
            if '\n' in Publishers[i].text:
                self.list_of_publishers.append(Publishers[i].text[:Publishers[i].text.index('\n')])
            else:
                self.list_of_publishers.append(Publishers[i].text)

    def _Extract_hashtags_userstagged_links(self, driver):
        """"
        Returns 3 lists containing for each tweet the different hashtags (self.list_hashtags),
         the users tagged (self.list_users_tagged),  and the links (self.list_links)
        """
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
                    continue
                if '@' in element.text:
                    list_ezer_pages.append(element.text)
                    self.list_pages_links.add(element.get_attribute('href'))
                    continue
                list_ezer_links.append(element.text)
            self.list_hashtags.append(list_ezer_hashtag)
            self.list_users_tagged.append(list_ezer_pages)
            self.list_links.append(list_ezer_links)

            ####         NUMBERS OF REPLIES, RETWEETS AND LIKES

    def _Extract_NumReplies_retweets_likes(self, driver):
        """"
        Returns a list containing 3 numbers per tweet: Num of replies, retweets and likes
        """
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

        ####      DATES

    def _Extract_Dates(self, driver):
        """
        Returns a list of the exact dates the tweets extracted where posted at.
        """
        TIMES = driver.find_elements(By.TAG_NAME, 'time')
        for item in TIMES:
            time = item.get_attribute('datetime')
            time = time.replace('T', ' ')
            self.list_times.append(time.replace('Z', ' '))

    def _Extract_Num_images(self, driver):
        """
        Returns a list giving the number of images present in every tweet.
        """
        list_tweet = driver.find_elements(By.CLASS_NAME,
                                          "css-1dbjc4n r-1ets6dv r-1867qdf r-1phboty r-rs99b7 r-1ny4l3l r-1udh08x r-o7ynqc r-6416eg".replace(
                                              ' ', '.'))

        for i in list_tweet:
            images_for_tweet = i.find_elements(By.TAG_NAME, "img")
            self.list_images.append(len(images_for_tweet))

    def Extract_ALL(self, driver):

        """
        Creates and Stores a csv file which contains all the features extracted from the webpage, the file is located in
        the path given by the user when creating the TweetsExtractor object
        """

        last_position = None
        end_of_scroll_region = False
        while not end_of_scroll_region:
            self._Extract_Names_and_links(driver)
            self._Extract_hashtags_userstagged_links(driver)
            self._Extract_NumReplies_retweets_likes(driver)
            self._Extract_Dates(driver)
            self._Extract_Num_images(driver)
            last_position, end_of_scroll_region = self._scroll_down_page(driver, last_position)
            if int(self.quantity_of_tweets) < len(self.list_of_publishers):
                break
        records = zip(self.list_of_publishers[:int(self.quantity_of_tweets)],
                      self.list_hashtags[:int(self.quantity_of_tweets)],
                      self.list_users_tagged[:int(self.quantity_of_tweets)],
                      self.list_links[:int(self.quantity_of_tweets)],
                      self.list_number_reply[:int(self.quantity_of_tweets)],
                      self.list_number_retweet[:int(self.quantity_of_tweets)],
                      self.list_number_Like[:int(self.quantity_of_tweets)],
                      self.list_times[:int(self.quantity_of_tweets)],
                      self.list_images[:int(self.quantity_of_tweets)])

        self._save_tweet_data_to_csv(records, self.path_CSVfile)


