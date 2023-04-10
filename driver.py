from database import *
from scraper import Scraper
import queue

database = DataBase()
scraper = Scraper()

job_queue = queue.Queue()
job_queue.put('MSFT')

while not job_queue.empty():
    ticker = job_queue.get()
    print(ticker)
    db_result = database.get_stock(ticker)
    if db_result is None:
        similar_tickers = scraper.get_similar_tickers(ticker)
        for similar_ticker in similar_tickers:
            job_queue.put(similar_ticker)
        database.add_stock(ticker, database.list_to_string(similar_tickers))
    else:
        for stock in database.new_stocks():
            job_queue.put(stock)
