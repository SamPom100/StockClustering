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

    def get_similar_tickers(self, ticker):
        tickerId = self.r.stocks.id_for_stock(ticker)
        res = self.r.helper.request_get('https://dora.robinhood.com/instruments/similar/'+tickerId+'/')['similar']
        return [x['symbol'] for x in res]

