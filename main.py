from Tweets_Extractor import *
from User_Extractor import *
import argparse


def main(search_term, quantity_of_tweets, path_csv_file):
    """
    arguments: the term the user wants to type in the search bar, the num of tweets the user wants to extract
     and the path where the csv file will be created.
     Returns the csv file containing the extracted tweets and located in the path as required.
    """
    try:
        tweets = Tweets_extractor(search_term, quantity_of_tweets, path_csv_file)
        driver = tweets.initialize_driver()
        tweets.Extract_ALL(driver)
        # tweets._Extract_Names_and_links(driver)
        user_info = User_extractor(tweets.list_of_publishers_links, driver)
        # tweets._Extract_hashtags_userstagged_links(driver)
        pages_info = User_extractor(tweets.list_pages_links, driver)
        driver.quit()
    except ValueError as va:
        print(f'{va}, Make sure you type an integer as second argument !')
    except PermissionError as Pa:
        print(f'{Pa}, Make sure the path you typed really exists or that you have permission to access it! !')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="the text you want to search in twitter", type=str)
    parser.add_argument("--number_of_tweets", help="optional number of tweets you need", type=int, required=False)
    parser.add_argument("--pathfile", help="the path for csv file", type=int, required=False)
    try:
        args = parser.parse_args()
        if not args.number_of_tweets:
            args.number_of_tweets = 150
        if not args.pathfile:
            args.pathfile = args.term + '.csv'
        main(args.term, args.number_of_tweets, args.pathfile)
    except SystemExit:
        print('Sorry, you need to type at least one arguments! 1) the text you want to search in twitter')

