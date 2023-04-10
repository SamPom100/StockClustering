from database import DataBase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service




class Scraper:
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

