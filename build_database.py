import pymysql
from Config import *
import re
from datetime import datetime

connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


def execute_sql(sql):
    """execute the sql query"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def create_database():
    sql = "CREATE DATABASE " + DATABASE_NAME
    try:
        execute_sql(sql)
    except pymysql.err.ProgrammingError as err:
        print(err)


def use_database():
    sql = "USE " + DATABASE_NAME
    execute_sql(sql)


# create tables

def create_table_tweets(length_varchar):
    sql = f"""CREATE TABLE Tweets(
              tweet_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              name_of_publisher VARCHAR({length_varchar}) NOT NULL,
              reply_count INT NOT NULL,
              retweet_count INT NOT NULL,
              like_count INT NOT NULL,
              dates DATETIME NOT NULL,
              number_of_images INT NOT NULL,
              number_of_videos INT NOT NULL,
              number_of_emojis INT NOT NULL,          
              reply BOOL NOT NULL,
              search_term VARCHAR({length_varchar}) NOT NULL
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)


def create_table_hashtag(length_varchar):
    sql = f"""CREATE TABLE Hashtag(
              hashtag_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              hashtag_name VARCHAR({length_varchar}) NOT NULL 
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)


def create_table_hashtag_tweets():
    """ create table to connect between the Hashtag' table to the Tweets table"""
    sql = f"""CREATE TABLE Hashtag_tweets(
              hashtag_tweet_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              hashtag_id INT NOT NULL,
              tweet_id INT NOT NULL 
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)


def create_table_link(length_varchar):
    sql = f"""CREATE TABLE Links(
              link_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              link VARCHAR({length_varchar}) NOT NULL
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)


def create_table_link_tweets():
    """ create table to connect between the Links' table to the Tweets table"""
    sql = f"""CREATE TABLE Links_tweets(
              link_tweet_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              link_id INT NOT NULL,
              tweet_id INT NOT NULL 
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)


def create_table_users(length_varchar):
    """ create table of users that include users that publish a tweet and users that tagged in tweet"""
    sql = f"""CREATE TABLE Users(
              user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              name_of_publisher VARCHAR({length_varchar}) UNIQUE,
              tag_of_publisher VARCHAR({length_varchar}) UNIQUE,
              number_of_following INT NOT NULL,
              number_of_followers INT NOT NULL
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)


def create_table_users_tagged_tweets():
    """ create table to connect between the Users' table to the Tweets' table for users that tagged in the tweet"""
    sql = f"""CREATE TABLE users_tagged_tweets(
              users_tagged_tweet_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              users_tagged_id INT NOT NULL,
              tweet_id INT NOT NULL 
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)


# helper functions for update

def convert_string_to_number(value):
    """ some features that represent numbers include symbols and letters, this method converts them to numbers"""
    if value == '':
        return 0
    new_value = float(re.sub("[A-Za-z,]", "", value))
    if 'K' in value:
        new_value = new_value * 1000
    if 'M' in value:
        new_value = new_value * 1e6
    return int(new_value)


def get_current_hashtags():
    sql = 'select * from Hashtag'
    result = execute_sql(sql)
    output_list = []
    for name_dict in result:
        output_list.append(name_dict['hashtag_name'])
    return output_list


def get_current_links():
    sql = 'select * from Links'
    result = execute_sql(sql)
    output_list = []
    for name_dict in result:
        output_list.append(name_dict['link'])
    return output_list


# update tables

def update_table_hashtag_tweets(records, hashtags, tweet_id):
    for row in set(records):
        if row.lower() not in list(map(lambda x: x.lower(), hashtags)):  # add only new hashtags to Hashtags table
            sql = 'insert into Hashtag (hashtag_id, hashtag_name) values(%s, %s)'
            cursor.execute(sql, (None, row))
        sql = 'insert into Hashtag_tweets (hashtag_tweet_id, hashtag_id, tweet_id) values(%s, (select hashtag_id ' \
              'from Hashtag where hashtag_name=%s), %s)'
        cursor.execute(sql, (None, row, tweet_id))


def update_table_links_tweets(records, links, tweet_id):
    for row in set(records):
        if row.lower() not in list(map(lambda x: x.lower(), links)):  # add only new links to Links table
            sql = 'insert into Links (link_id, link) values(%s, %s)'
            cursor.execute(sql, (None, row))
        sql = 'insert into Links_tweets (link_tweet_id, link_id, tweet_id) values(%s, (select link_id ' \
              'from Links where link=%s), %s)'
        cursor.execute(sql, (None, row, tweet_id))


def update_table_users(records):
    for row in records:
        row[2] = convert_string_to_number(row[2])
        row[3] = convert_string_to_number(row[3])
        # Add new users or update information on users that already exist
        sql = 'insert into Users (user_id, name_of_publisher,tag_of_publisher, number_of_following,' \
              'number_of_followers) values(%s, %s, %s,%s, %s) on duplicate key update number_of_following=values(' \
              'number_of_following), number_of_followers=values(number_of_followers) '
        cursor.execute(sql,
                       (None, row[0], row[1], row[2], row[3]))
    connection.commit()


def update_table_users_tagged_tweets(records, tweet_id):
    for row in set(records):
        sql = 'insert into users_tagged_tweets (users_tagged_tweet_id, users_tagged_id, tweet_id) values(%s, ' \
              '(select user_id from Users where tag_of_publisher=%s), %s)'
        cursor.execute(sql, (None, row, tweet_id))


def update_table_tweets(records, search_term):
    """ update all the tables according the new records, except the Users' table that update separately"""
    current_hashtags = set(get_current_hashtags())
    current_links = set(get_current_links())
    for row in records:
        # change the ReplyCount, RetweetCount, LikeCount to integers from string
        row[3] = list(map(lambda x: convert_string_to_number(x), row[3]))
        # change DATES to date format
        row[4] = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')
        # check if the tweet exist
        condition = f'dates = "{row[4]}" AND name_of_publisher= "{row[0]}"'
        sql = f'select count(*) from Tweets where {condition}'
        result = execute_sql(sql)
        if result[0]['count(*)'] != 0:  # update tweet information
            sql = f'UPDATE Tweets SET reply_count=%s, retweet_count=%s, like_count=%s where {condition}'
            cursor.execute(sql, (row[3][0], row[3][1], row[3][2]))
        else:  # insert new tweet
            sql = 'insert into Tweets values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql,
                           (None, row[0], row[3][0], row[3][1], row[3][2], row[4], row[5], row[6], row[7], row[8],
                            search_term))
        sql = 'SELECT COUNT(*) FROM Tweets'
        tweet_id = execute_sql(sql)[0]['COUNT(*)']
        update_table_hashtag_tweets(row[2][0], current_hashtags, tweet_id)
        current_hashtags = current_hashtags.union(set(row[2][0]))  # update the hashtags set
        update_table_users_tagged_tweets(row[2][1], tweet_id)
        update_table_links_tweets(row[2][2], current_links, tweet_id)
        current_links = current_links.union(set(row[2][2]))  # update the links set
    connection.commit()
