from Tweets_Extractor import *
from User_Extractor import *
from build_database import *
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
        records = tweets.Extract_ALL(driver)
        # tweets._Extract_Names_and_links(driver)
        create_DATABASE()
        use_DATABASE()
        create_table_tweets()
        # create_table_hashtag()
        number_of_rows = get_number_of_rows('Tweets')
        update_table_tweets(records, search_term, number_of_rows)
        users = User_extractor(tweets.list_of_publishers_links)
        records = users.user_extract(driver)
        create_table_users()
        number_of_rows = get_number_of_rows('Users')
        update_table_users(records, number_of_rows)
        # tweets._Extract_hashtags_userstagged_links(driver)
        # pages_info = User_extractor(tweets.list_pages_links, driver)
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

