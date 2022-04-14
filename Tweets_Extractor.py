from selenium.webdriver.common.by import By
from time import sleep
import csv


class Tweets_extractor:
    """
    Create a Tweets' extractor object that can be called after creating a Chrome driver object to extract
    and store in a table as many tweets as one wants, from the result's page of a specific term research on Twitter
    """

    def __init__(self, search_term, quantity_of_tweets, path_csvfile):
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
        self.path_csv_file = path_csvfile
        self.quantity_of_tweets = quantity_of_tweets

        self.quantity_of_scrapers_tweets = 0

        self.list_of_publishers_links = set()
        self.list_hashtags = set()
        self.list_pages_links = set()

        self.records = []

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

    def _save_tweet_data_to_csv(self, mode='w'):
        """
        create csv file with all the records
        """
        header = ['NAMES OF PUBLISHERS', 'LINK OF PUBLISHERS', 'HASHTAGS_USERS TAGGED_LINKS',
                  'ReplyCount_RetweetCount_LikeCount',
                  'DATES', 'NUMBER OF IMAGES', 'NUMBER OF VIDEOS', 'NUMBER OF EMOJIS', 'REPLY']
        with open(self.path_csv_file, mode=mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in self.records:
                writer.writerow(row)

    def return_attribute(self, attribute):
        """
        return attribute
        """
        return getattr(self, attribute)

    @staticmethod
    def _extract_publisher_name(driver):
        """
        Returns the names of the tweet publisher
        """
        publisher = driver.find_elements(By.CLASS_NAME,
                                         "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0".replace(' ', '.'))
        return publisher[0].text

    def _extract_publisher_link(self, driver):
        """
        Returns a list of the names of the different tweet publishers
        """
        publisher_link = driver.find_elements(By.CLASS_NAME,
                                              "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs "
                                              "r-1ny4l3l".replace(' ', '.'))
        self.list_of_publishers_links.add(publisher_link[0].get_attribute('href'))
        return publisher_link[0].get_attribute('href')

    def _extract_hashtags_users_tagged_links(self, driver):
        """"
        Returns 3 lists containing for each tweet the different hashtags (self.list_hashtags),
        the users tagged (self.list_users_tagged),  and the links (self.list_links)
        """
        hashtag_list = driver.find_elements(By.CLASS_NAME,
                                            "css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr "
                                            "r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0".replace(' ', '.'))
        list_hashtags = []
        list_users_tagged = []
        list_links = []
        for element in hashtag_list:
            if '#' in element.text[0]:
                list_hashtags.append(element.text)
                self.list_hashtags.add(element.text)
                continue
            if '@' in element.text[0]:
                list_users_tagged.append(element.text)
                self.list_of_publishers_links.add(element.get_attribute('href'))
                continue
            list_links.append(element.get_attribute('href'))
            self.list_pages_links.add(element.get_attribute('href'))
        return [list_hashtags, list_users_tagged, list_links]

        #         NUMBERS OF REPLIES, RETWEETS AND LIKES

    @staticmethod
    def _extract_num_replies_retweets_likes(driver):
        """"
        Returns a list containing 3 numbers: Num of replies, retweets and likes
        """
        number_info = driver.find_elements(By.CLASS_NAME,
                                           "css-1dbjc4n r-1ta3fxp r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws".replace(' ',
                                                                                                                   '.'))
        numbers_list = number_info[0].find_elements(By.CLASS_NAME,
                                                    "css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp "
                                                    "r-1e081e0 r-qvutc0".replace(' ', '.'))
        return [numbers_list[0].text, numbers_list[1].text, numbers_list[2].text]

        #      DATES

    @staticmethod
    def _extract_dates(driver):
        """
        Returns a list of the exact dates the tweets extracted where posted at.
        """
        times = driver.find_elements(By.TAG_NAME, 'time')
        time = times[0].get_attribute('datetime')
        time = time.replace('T', ' ')
        return time.replace('Z', '')

    @staticmethod
    def _extract_num_images(driver):
        """
        Returns a list giving the number of images present in every tweet.
        """
        list_tweet = driver.find_elements(By.CLASS_NAME,
                                          "css-1dbjc4n r-1ets6dv r-1867qdf r-1phboty r-rs99b7 r-1ny4l3l r-1udh08x "
                                          "r-o7ynqc r-6416eg".replace(' ', '.'))
        num_images_for_tweet = 0
        if len(list_tweet) > 0:
            num_images_for_tweet = len(list_tweet[0].find_elements(By.TAG_NAME, "img"))
        return num_images_for_tweet

    @staticmethod
    def _extract_num_emojis(driver):
        """
        Returns the number of emojis present in every tweet.
        """
        text_tweet = driver.find_elements(By.CLASS_NAME,
                                          "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo "
                                          "r-bnwqim r-qvutc0".replace(' ', '.'))
        list_tweet = text_tweet[0].find_elements(By.CLASS_NAME,
                                                 "r-4qtqp9 r-dflpy8 r-sjv1od r-zw8f10 r-10akycc r-h9hxbl".replace(
                                                     ' ', '.'))
        return len(list_tweet)

    @staticmethod
    def _extract_num_videos(driver):
        """
        Returns number of videos present in the tweet.
        """
        list_tweet = driver.find_elements(By.TAG_NAME, "video")
        return len(list_tweet)

    @staticmethod
    def _extract_bool_reply(driver):
        """
        Returns true if this reply tweet.
        """
        bool_reply = driver.find_elements(By.CLASS_NAME,
                                          "css-1dbjc4n r-4qtqp9 r-zl2h9q".replace(' ', '.'))
        if len(bool_reply) > 0:
            return True
        return False

    def _extract_tweets(self, driver):
        """
        Returns a list of tweets.
        """
        list_tweets = driver.find_elements(By.CLASS_NAME,
                                           "css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu".replace(' ', '.'))
        self.quantity_of_scrapers_tweets = self.quantity_of_scrapers_tweets + len(list_tweets)
        for tweet in list_tweets:
            row = [self._extract_publisher_name(tweet), self._extract_publisher_link(tweet),
                   self._extract_hashtags_users_tagged_links(tweet), self._extract_num_replies_retweets_likes(tweet),
                   self._extract_dates(tweet), self._extract_num_images(tweet), self._extract_num_videos(tweet),
                   self._extract_num_emojis(tweet), self._extract_bool_reply(tweet)]
            self.records.append(row)

    def extract_all(self, driver):

        """
        Creates and Stores a csv file which contains all the features extracted from the webpage, the file is located in
        the path given by the user when creating the TweetsExtractor object
        """

        last_position = None
        end_of_scroll_region = False
        while not end_of_scroll_region:
            self._extract_tweets(driver)
            last_position, end_of_scroll_region = self._scroll_down_page(driver, last_position)
            if int(self.quantity_of_tweets) < int(self.quantity_of_scrapers_tweets):
                break

        self._save_tweet_data_to_csv()
        return self.records