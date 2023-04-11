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
                stock_ticker TEXT NOT NULL,
                similar_stocks TEXT NOT NULL,
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
        except:
            pass
    
    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_stock(self, ticker, simple_name, tags):
        self.execute(f"INSERT INTO Stocks VALUES ('{ticker}', '{simple_name}', '{self.encode_list(tags)}')")
    
    def add_similar(self, ticker, similar):
        self.execute(f"INSERT INTO Similar VALUES ('{ticker}', '{self.encode_list(similar)}')")
    
    def get_similar(self, ticker):
        return self.decode_list(self.fetch(f"SELECT similar_stocks FROM Similar WHERE stock_ticker='{ticker}'")[0][0])

    def get_indexed_stock_tickers(self):
        return [x[0] for x in self.fetch("SELECT stock_ticker FROM Stocks")]

    def get_indexed_similar_tickers(self):
        return [x[0] for x in self.fetch("SELECT stock_ticker FROM Similar")]

    def get_new_jobs(self):
        seen = self.get_indexed_stock_tickers()
        similar = self.get_indexed_similar_tickers()
        return [x for x in seen if x not in similar]