import requests
import configparser
from build_database import *
from Config import *

config = configparser.RawConfigParser()
config.read(filenames=TOKEN_LOCATION)
BEARER_TOKEN = config.get('Default', 'BEARER_TOKEN')


def create_url(list_of_usernames):
    """

    """
    usernames = "usernames="
    for user in list_of_usernames:
        usernames += user[1:]
        if user != list_of_usernames[-1]:
            usernames += ","
    user_fields = "user.fields=description,created_at,public_metrics,verified"
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def users_updater(list_of_usernames):
    url = create_url(list_of_usernames)
    json_response = connect_to_endpoint(url)
    rows = []
    for user_info in json_response['data']:
        keys = sorted(user_info.keys())
        user_info_list = [list_of_usernames[json_response['data'].index(user_info)]]
        for key in keys:
            if key == 'public_metrics':
                sub_dict = user_info[key]
                for sub_key in ['listed_count', 'tweet_count']:
                    user_info_list.append(sub_dict[sub_key])
            else:
                user_info_list.append(user_info[key])
        rows.append(user_info_list)
    return rows


def add_columns(cursors):
    try:
        query_update = "ALTER TABLE Users ADD created_at DATE, ADD description VARCHAR(200), ADD listed_count INT, " \
                       "ADD tweet_count INT, ADD verified BOOL"
        cursors.execute(query_update)
    except pymysql.err.OperationalError as err:
        print(err)


def fill_new_columns(record, cursors):
    for row in users_updater(record):
        sql = "UPDATE users SET created_at=%s, description=%s, listed_count=%s, tweet_count=%s, verified=%s where " \
              "TAG_OF_PUBLISHER=%s"
        cursors.execute(sql,
                        (row[1][:-4], row[2], row[5], row[6], row[8], row[0]))
        print((row[1], row[2], row[5], row[6], row[8], row[0]))
    connection.commit()


def get_list_usernames_from_table(cursors):
    query = "SELECT tag_of_publisher from Users"
    # result = cursors.execute(query)
    cursor.execute(query)
    result = cursor.fetchall()
    output_list = []
    for name_dict in result:
        output_list.append(name_dict['tag_of_publisher'])
    return output_list
