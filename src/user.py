import base64
from Crypto.PublicKey import RSA
from src.address import Address
import sqlite3

class User:

    def __init__(self, name, email, password):

        address = Address()
        conn = self.create_connection()
        last_id = self.get_max_id(conn)

        self.id = 1 if not last_id else last_id+1
        self.name = name
        self.password = base64.b64encode(password.encode("utf-8"))
        self.email = email
        self.address = address.__dict__['address']

        self.create_user_row(conn)

    def create_user_row(self, conn):
        c = conn.cursor()
        sql = ''' INSERT INTO users (user_id, user_name, password, email, address)
                  VALUES(?,?,?,?,?) '''
        user_params = [self.__dict__[i] for i in list(self.__dict__)]
        print(user_params)
        c.execute(sql, user_params)

        conn.commit()
        conn.close()

    def get_max_id(self, conn):
        c = conn.cursor()

        cursor = c.execute('SELECT MAX(USER_ID) FROM USERS')
        return cursor.fetchone()[0]

    def create_connection(self):
        return sqlite3.connect('test_database') 

