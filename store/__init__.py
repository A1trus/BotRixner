import sqlite3
import pandas as pd

class MessageStore:
    def __init__(self):
        self.conn = sqlite3.connect('./store.db')

        # Create the table if it doesn't already exist
        if pd.read_sql('SELECT * FROM sqlite_master WHERE tbl_name = "store"', self.conn).shape[0] == 0:
            print('Creating store...')
            cur = self.conn.cursor()
            cur.execute('CREATE TABLE store (key text, value text)')
            self.conn.commit()
        
        self.read_data()
    
    def read_data(self):
        self.data = pd.read_sql('SELECT * FROM store', self.conn)
    
    def includes(self, id, prefix=''):
        return id in self.data.loc[self.data['key'].str.startswith(prefix), 'value'].to_numpy()
    
    def get(self, key):
        s = self.data.loc[self.data['key'] == key, 'value']
        if s.shape[0] != 1:
            return None
        return s.iloc[0]

    def add(self, key, value):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO store VALUES (?, ?)', [key, value])
        self.conn.commit()
        self.read_data()

    def remove(self, key):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM store WHERE key = ?', [key])
        self.conn.commit()
        self.read_data()

# Create a message store for the application.  
# This is what should be referenced outside this module
message_store = MessageStore()