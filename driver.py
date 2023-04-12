from database import *
from scraper import *
import queue

database = DataBase()
scraper = RobinScraper()

def main():
    job_queue = queue.Queue()
    job_queue.put('AAPL')

    while True:
        if job_queue.empty():
            new_jobs = database.get_new_jobs()   
            if len(new_jobs) == 0:
                break
            for job in new_jobs:
                job_queue.put(job)
                
        ticker = job_queue.get()
        print("Searching: ", ticker)
        index = database.get_indexed_similar_tickers()
        if ticker not in index:
            tickerId = scraper.get_ticker_id(ticker)
            similar_tickers = scraper.get_similar_tickers_populate(tickerId, database)
            database.add_similar(ticker, similar_tickers)
            print("Added: ", ticker)
        else:
            print("Seen: ", ticker)

def calc_sizes():
    stock_dict = {}
    for stock in database.get_indexed_similar_tickers():
        for similar_stock in database.get_similar(stock):
            if similar_stock not in stock_dict:
                stock_dict[similar_stock] = 1
            else:
                stock_dict[similar_stock] += 1
    for stock in stock_dict:
        database.add_stock_count(stock, stock_dict[stock])

def add_straggler(ticker):
    tickerId = scraper.get_ticker_id(ticker)
    similar_tickers = scraper.get_similar_tickers_populate(tickerId, database)

    tickerId2 = scraper.get_ticker_id(similar_tickers[0])
    similar_tickers2 = scraper.get_similar_tickers_populate(tickerId2, database)

if __name__ == "__main__":
    main()
