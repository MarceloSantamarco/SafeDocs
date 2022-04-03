import base64
from Crypto.PublicKey import RSA
from src.address import Address
from src.application_helper import create_connection

class Session:

    def __init__(self, email, password):

        conn = create_connection()
        user = self.find_user(email, conn)

        if user is None:
            raise ValueError
        elif base64.b64decode(user[2]) != bytes(password, 'utf-8'):
            raise ValueError
        else:
            self.name= user[1]
            self.email = user[3]
            self.address = user[4]

    def find_user(self, email, conn):
        c = conn.cursor()
        sql = f""" SELECT * FROM USERS WHERE EMAIL = '{email}' """
        cursor = c.execute(sql)
        return cursor.fetchone()