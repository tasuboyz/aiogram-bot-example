import sqlite3
import config
from datetime import datetime

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()      
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
        self.c.execute(f"INSERT OR REPLACE INTO {self.USER_INFO} ({self.user_id}, {self.username}) VALUES (?, ?)", (user_id, username))
        self.conn.commit()

    def delate_user(self, user_ids):
        for user_id in user_ids:
            self.c.execute(f"DELETE FROM {self.USER_INFO} WHERE {self.user_id} = ?", (user_id,)) 
        self.conn.commit()          
    
    def get_user_data(self, user_id):
        self.c.execute(f'''SELECT {self.user_id} FROM {self.USER_INFO} WHERE {self.user_id} = ?''', (user_id,))
        result = self.c.fetchone()
        self.conn.commit()
        return result[0] if result else (None)
    
    def get_all_users(self):
        self.c.execute(f"SELECT {self.user_id} FROM {self.USER_INFO}")
        results = self.c.fetchall()        
        self.conn.commit()
        return results

    def count_users(self):
        self.c.execute(f"SELECT COUNT({self.user_id}) FROM {self.USER_INFO}")
        row_count = self.c.fetchone()[0]
        return row_count   
        
    def delete_ids_from_file(self, filename):
            file = open(filename, "r")
            lines = file.readlines()
            ids_to_delete = []
            for line in lines:
                line = line.strip()
                ids_to_delete.append(int(line))
            file.close()
            sql = f"DELETE FROM {self.USER_INFO} WHERE {self.user_id} IN (%s)" % ",".join("?" * len(ids_to_delete))
            self.c.execute(sql, ids_to_delete)
            count = self.c.rowcount
            self.conn.commit()
            return f"{count} record(s) deleted"