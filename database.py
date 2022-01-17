import sqlite3

conn = sqlite3.connect('test_database') 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS users
          ([user_id] INTEGER PRIMARY KEY, 
           [user_name] TEXT,
           [password] TEXT,
           [email] TEXT,
           [address] TEXT)
          ''')

conn.commit()