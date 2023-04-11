import os, sqlite3, json

def create_database():
    if not os.path.isfile('database.db'):
        os.system('touch database.db')
        sqlite3.connect('database.db', check_same_thread=False).cursor().executescript(
            """CREATE TABLE Stocks (
                stock_ticker TEXT NOT NULL UNIQUE PRIMARY KEY, 
                simple_name TEXT NOT NULL,
                tags TEXT NOT NULL,
                similar_tickers TEXT NOT NULL
            );""").close()
        print("DATABASE CREATED")

class DataBase:
    def encode_list(self, list):
        return json.dumps(list)

    def decode_list(self, string):
        return json.loads(string)
        
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

    def add_stock(self, stock_ticker, simple_name, tags, similar_tickers):
        print("Added: ", stock_ticker)
        self.execute(f"INSERT INTO Stocks VALUES ('{stock_ticker}', '{simple_name}', '{tags}', '{self.encode_list(similar_tickers)}')")

    def get_similar_tickers(self, stock_ticker):
        tmp = self.fetch(f"SELECT similar_tickers FROM Stocks WHERE stock_ticker='{stock_ticker}'")
        return None if len(tmp) == 0 else self.decode_list(tmp[0][0])

    def seen_stocks(self):
        return set([x[0] for x in self.fetch("SELECT stock_ticker FROM Stocks")])

    def new_stocks(self):
        seen_stocks = self.seen_stocks()
        similar_stocks = set()
        for stock in seen_stocks:
            similar_stocks.update(self.get_similar_tickers(stock))
        return similar_stocks - seen_stocks