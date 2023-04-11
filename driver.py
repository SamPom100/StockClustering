from database import *
from scraper import *
import queue

database = DataBase()
scraper = RobinScraper()

def main():
    job_queue = queue.Queue()
    job_queue.put('WAL')

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


if __name__ == "__main__":
    main()
