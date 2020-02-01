import sqlite3
class DBManager(object):
    '''this class makes connection to root folder's database '''
    def __init__(self):
        self.connection = None
        self.cursor = None
    def make_connection(self, url)->None:
        self.connection = sqlite3.connect(url)
        self.cursor = self.connection.cursor()
    def disconnect(self)->None:
        if self.connection:
            self.connection.commit()
            self.connection.close()
    def get_selection(self)->list:
        return self.cursor.fetchall()
