from database import DataBase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import robin_stocks.robinhood as r
import json



class AlphaScraper:
    def __init__(self):
            chromedriver = "/chromedriver"
            option = webdriver.ChromeOptions()
            #option.add_argument("--headless")
            option.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
            s = Service(chromedriver)
            self.browser = webdriver.Chrome(service=s, options=option)
            #self.browser = webdriver.Safari()

    def get_url(self, ticker):
        return 'https://seekingalpha.com/symbol/'+ticker+'/peers/comparison'

    def get_similar_tickers(self, ticker):
        self.browser.get(self.get_url(ticker))
        while(True):
            if '?compare' in self.browser.current_url:
                break
        res = self.browser.current_url
        return res[res.find('?compare=')+9:].split(',')

class RobinScraper:
    def __init__(self):
        loginInfo = json.load(open('login_information.json'))
        login = r.login(loginInfo['email'], loginInfo['password'])
        self.r = r

    def get_ticker_id(self, ticker):
        return self.r.stocks.id_for_stock(ticker)

    def get_similar_tickers(self, tickerId):
        res = self.r.helper.request_get('https://dora.robinhood.com/instruments/similar/'+tickerId+'/')['similar']
        return [x['symbol'] for x in res]

    def get_similar_tickers_populate(self, tickerId, db: DataBase):
        res = self.r.helper.request_get('https://dora.robinhood.com/instruments/similar/'+tickerId+'/')['similar']
        similar_stocks = []
        for stock in res:
            symbol = stock['symbol']
            simple_name = stock['simple_name']
            tags = stock['tags']
            tags = [x['name'] for x in tags]
            similar_stocks.append(symbol)
            db.add_stock(symbol, simple_name, tags)
        return similar_stocks
            

    def get_info(self, tickerId):
        res = self.r.helper.request_get('https://api.robinhood.com/instruments/'+tickerId)
        return res['simple_name'], 

