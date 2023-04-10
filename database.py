import os, sqlite3

def create_database():
    if not os.path.isfile('database.db'):
        os.system('touch database.db')
        sqlite3.connect('database.db', check_same_thread=False).cursor().executescript("""CREATE TABLE Stocks (stock_name TEXT NOT NULL UNIQUE PRIMARY KEY, similar_tickers TEXT NOT NULL);""").close()
        print("DATABASE CREATED")

class DataBase:
    def list_to_string(self, list):
        return ', '.join(list)

    def string_to_list(self, string):
        return string.split(', ')
        
    def __init__(self):
        create_database()
        self.connection = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        print("CONNECTED TO DB")

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_stock(self, stock_name, similar_tickers):
        print("Added: "+stock_name)
        self.execute(f"INSERT INTO Stocks VALUES ('{stock_name}', '{similar_tickers}')")

    def get_stock(self, stock_name):
        tmp = self.fetch(f"SELECT similar_tickers FROM Stocks WHERE stock_name='{stock_name}'")
        return None if len(tmp) == 0 else self.string_to_list(tmp[0][0])[1:]

    def seen_stocks(self):
        return set([x[0] for x in self.fetch("SELECT stock_name FROM Stocks")])

    def new_stocks(self):
        seen_stocks = self.seen_stocks()
        similar_stocks = set()
        for stock in seen_stocks:
            similar_stocks.update(self.get_stock(stock))
        return similar_stocks - seen_stocks