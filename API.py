from Config import *
from main import *
import configparser
import requests

config = configparser.RawConfigParser()
config.read(filenames=TOKEN_LOCATION)
BEARER_TOKEN = config.get('Default', 'BEARER_TOKEN')


def create_url(user):
    """
    """
    usernames = "usernames="
    usernames += user[1:].lstrip("_")
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, USER_FIELDS)
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
    if response.status_code != 200:
        logging.error(f"cant get the api info from this url user {url}")
        return 0
    logging.info(f"the api info extract successful from this url user{url}")
    return response.json()


def users_updater(list_of_usernames):
    rows = []
    for user in list_of_usernames:
        url = create_url(user)
        json_response = connect_to_endpoint(url)
        if json_response == 0 or 'data' not in json_response:
            rows.append([None] * 6)
            continue
        user_info = json_response['data'][0]
        keys = sorted(user_info.keys())
        user_info_list = []
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
    rows = users_updater(record)
    for row in rows:
        if None in row:
            continue
        sql = "UPDATE Users SET created_at=%s, description=%s, listed_count=%s, tweet_count=%s, verified=%s where " \
              "TAG_OF_PUBLISHER=%s"
        cursors.execute(sql,
                        (row[0][:10], row[1], row[4], row[5], row[7], '@'+row[6]))
    connection.commit()


def get_list_usernames_from_table(cursors):
    query = "SELECT tag_of_publisher from Users"
    cursors.execute(query)
    result = cursors.fetchall()
    output_list = []
    for name_dict in result:
        output_list.append(name_dict['tag_of_publisher'])
    return output_list
