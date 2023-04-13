import os, sqlite3, json

def create_database():
    if not os.path.isfile('database.db'):
        os.system('touch database.db')
        sqlite3.connect('database.db', check_same_thread=False).cursor().executescript(
            """CREATE TABLE Stocks (
                stock_ticker TEXT NOT NULL UNIQUE PRIMARY KEY, 
                simple_name TEXT NOT NULL,
                tags TEXT NOT NULL
            );
            CREATE TABLE Similar (
                stock_ticker TEXT NOT NULL UNIQUE,
                similar_stocks TEXT NOT NULL,
                similar_count TEXT NOT NULL,
                FOREIGN KEY (stock_ticker) REFERENCES Stocks (stock_ticker)
            );
            """).close()
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
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(e)
    
    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_stock(self, ticker, simple_name, tags):
        simple_name = simple_name.replace("'", "")
        self.execute(f"INSERT INTO Stocks VALUES ('{ticker}', '{simple_name}', '{self.encode_list(tags)}')")
    
    def add_similar(self, ticker, similar, count=0):
        self.execute(f"INSERT INTO Similar VALUES ('{ticker}', '{self.encode_list(similar)}', {count})")
    
    def get_similar(self, ticker):
        return self.decode_list(self.fetch(f"SELECT similar_stocks FROM Similar WHERE stock_ticker='{ticker}'")[0][0])

    def get_indexed_stock_tickers(self):
        return [x[0] for x in self.fetch("SELECT stock_ticker FROM Stocks")]

    def get_indexed_similar_tickers(self):
        return [x[0] for x in self.fetch("SELECT stock_ticker FROM Similar")]

    def add_stock_count(self, ticker, count):
        self.execute(f"UPDATE Similar SET similar_count={count} WHERE stock_ticker='{ticker}'")

    def get_stock_count(self, ticker):
        return self.fetch(f"SELECT similar_count FROM Similar WHERE stock_ticker='{ticker}'")[0][0]

    def get_similar_all(self, ticker):
        return self.fetch(f"SELECT * FROM Similar WHERE stock_ticker='{ticker}'")

    def get_stock_all(self, ticker):
        return self.fetch(f"SELECT * FROM Stocks WHERE stock_ticker='{ticker}'")

    def get_new_jobs(self):
        similar_list = self.similar_set()
        similar_index = self.get_indexed_similar_tickers()
        return set(similar_list) - set(similar_index)
        
    def similar_set(self):
        returnSet = set()
        for stock in self.get_indexed_similar_tickers():
            for similar_stock in self.get_similar(stock):
                returnSet.add(similar_stock)
        return returnSet

    def similar_score(self, ticker1, ticker2):
        similar1 = self.get_similar(ticker1)
        similar2 = self.get_similar(ticker2)
        list.reverse(similar1)
        list.reverse(similar2)
        try:
            similar1_index = similar1.index(ticker2)+1
        except:
            similar1_index = 0
        try:
            similar2_index = similar2.index(ticker1)+1
        except:
            similar2_index = 0

        return (similar1_index + similar2_index) / 2