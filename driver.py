from database import *
from scraper import *
import queue

database = DataBase()
scraper = RobinScraper()

def main():
    job_queue = queue.Queue()
    job_queue.put('AAPL')

    while not job_queue.empty():
        ticker = job_queue.get()
        result = scraper.get_similar_tickers(ticker)
        print(result)






if __name__ == "__main__":
    main()


