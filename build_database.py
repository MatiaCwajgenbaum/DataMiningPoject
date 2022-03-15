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

def create_table(search_term):
    sql = f"""CREATE TABLE Tweet_{search_term}(
             tweet_id INT PRIMARY KEY,
             NAMES_OF_PUBLISHERS VARCHAR(30),
             ReplyCount INT,
             RetweetCount INT,
             LikeCount INT,
             DATES DATE,
             NUMBER_OF_IMAGES INT
    )"""
    try:
        execute_sql(sql)
    except pymysql.err.OperationalError as err:
        print(err)
    # sql = "SHOW TABLES"
    # execute_sql(sql)


def update_table(records, search_term):
    for index, row in enumerate(records):
        sql = f"INSERT INTO Tweet_{search_term} VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (index, row[0], row[4], row[5], row[6], row[7], row[8]))
