import pymysql

connection = pymysql.connect(host="localhost",
                             user="maya95",
                             password="MSmaya2035!",
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


def execute_sql(sql):
    """execute the sql query"""
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    return result


def create_DATABASE():
    sql = "CREATE DATABASE Tweets"
    try:
        execute_sql(sql)
    except pymysql.err.ProgrammingError as err:
        print(err)
    # sql = "SHOW databases"
    # execute_sql(sql)


def use_DATABASE():
    sql = "USE Tweets"
    execute_sql(sql)


def get_number_of_rows(table):
    sql = f'select count(*) from {table}'
    result = execute_sql(sql)
    return result[0]['count(*)']


def create_table_tweets():
    sql = f"""CREATE TABLE Tweets(
             tweet_id INT PRIMARY KEY,
             NAME_OF_PUBLISHER VARCHAR(30),
             ReplyCount VARCHAR(10),
             RetweetCount VARCHAR(10),
             LikeCount VARCHAR(10),
             DATES VARCHAR(30),
             NUMBER_OF_IMAGES INT,
             search_term VARCHAR(30)
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)
    # sql = "SHOW TABLES"
    # execute_sql(sql)


def update_table_tweets(records, search_term, number_of_rows):
    index = 0
    for row in records:
        sql = f'select count(*) from Tweets where DATES = "{row[7]}" AND NAME_OF_PUBLISHER= {row[0]}'
        result = execute_sql(sql)
        if result[0]['count(*)'] != 0:
            continue
        ezer_row4 = row[4]
        if ezer_row4 == '':
            ezer_row4 = 0
        ezer_row5 = row[5]
        if ezer_row5 == '':
            ezer_row5 = 0
        ezer_row6 = row[6]
        if ezer_row6 == '':
            ezer_row6 = 0
        sql = "INSERT INTO Tweets VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql,
                       ((number_of_rows + index), row[0], ezer_row4, ezer_row5, ezer_row6, row[7], row[8], search_term))
        index = index + 1
    connection.commit()


def create_table_users():
    sql = f"""CREATE TABLE Users(
             user_id INT PRIMARY KEY,
             NAME_OF_PUBLISHER VARCHAR(30),
             Number_of_Following VARCHAR(10),
             Number_of_Followers VARCHAR(10)
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)


def update_table_users(records, number_of_rows):
    index = 0
    for row in records:
        sql = f'select count(*) from Users where NAME_OF_PUBLISHER = "{row[0]}"'
        result = execute_sql(sql)
        if result[0]['count(*)'] != 0:
            continue
        sql = "INSERT INTO Users VALUES (%s, %s, %s, %s)"
        cursor.execute(sql,
                       (number_of_rows + index, row[0], row[1], row[2]))
        index = index + 1
    connection.commit()

# def create_table_hashtag():
#     sql = f"""CREATE TABLE Hashtag(
#              id INT PRIMARY KEY,
#              tweet_id INT
#     )"""
#     try:
#         execute_sql(sql)
#     except pymysql.err.OperationalError as err:
#         print(err)

# def create_table_hashtag():
#     sql = f"""CREATE TABLE hashtag(
#              id INT PRIMARY KEY,
#              NAME VARCHAR(30)
#     )"""
#     try:
#         execute_sql(sql)
#     except pymysql.err.OperationalError as err:
#         print(err)
#
#
# def update_table_hashtag(records, number_of_rows):
#     for index, row in enumerate(records):
#         sql = "INSERT INTO Tweets VALUES (%s, %s)"
#         cursor.execute(sql,
#                        (number_of_rows + index, row[0]))
#     connection.commit()
