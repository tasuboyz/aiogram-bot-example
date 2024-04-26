import sqlite3
import config
from datetime import datetime

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('database.db')

        #table
        self.USER_INFO = 'USER_INFO'

        #columns
        self.user_id = "user_id"
        self.username = "username"      
    pass
        
    def create_table(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.USER_INFO} ({self.user_id} INTEGER PRIMARY KEY, {self.username} TEXT)''')
        self.conn.commit()

    def insert_user_data(self, user_id, username):
        self.c.execute(f"INSERT OR REPLACE INTO {self.user_info} ({self.user_id}, {self.username}) VALUES (?, ?)", (user_id, username))
        self.conn.commit()

    def delate_user(self, user_ids):
        for user_id in user_ids:
            self.c.execute(f"DELETE FROM {self.user_info} WHERE {self.user_id} = ?", (user_id,)) 
        self.conn.commit()          
    
    def get_user_data(self, user_id):
        self.c.execute(f'''SELECT {self.user_id} FROM {self.user_info} WHERE {self.user_id} = ?''', (user_id,))
        result = self.c.fetchone()
        self.conn.commit()
        return result[0] if result else (None)
