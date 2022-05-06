import requests
# Connecting to MySQL Using Connector/Python

import mysql.connector
from mysql.connector import errorcode

from setting import password


def main():
    try:
      cnx = mysql.connector.connect(user='root', password=password, host='127.0.0.1')
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)

    cursor = cnx.cursor()



    # Creating Tables Using Connector/Python

    # create table

    DB_NAME = 'pchome_airfryer'

    TABLES = {}
    TABLES['airfryer'] = (
        "CREATE TABLE `airfryer` ("
        # "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(50) NOT NULL,"
        "  `price` int NOT NULL,"
        "  `originprice` int NOT NULL,"
        "  PRIMARY KEY (`name`)"
        ") ENGINE=InnoDB")

    # create database

    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    # Inserting Data Using Connector/Python

    add_airfryer = ("INSERT IGNORE INTO airfryer "
                   "(name, price, originprice) "
                   "VALUES (%s, %s, %s)")

    for i in range(1, 62):
        url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E6%B0%A3%E7%82%B8%E9%8D%8B&page={}&sort=sale/dc'.format(i)
        print(i)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            data = r.json()
            rows = data['prods']
            for row in rows:
                if len(row['name']) >= 50:
                    row['name'] = row['name'][:50]
                data_airfryer = (row['name'], row['price'], row['originPrice'])
                cursor.execute(add_airfryer, data_airfryer)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

if __name__ == '__main__':
    main()