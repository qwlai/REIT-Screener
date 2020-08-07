import requests
from lxml import html
import re

class DividendsCrawler():
    def __init__(self, ticker):
        self.ticker = ticker

    def get_dividend_yield_ttm(self):
        response = requests.get('https://www.dividends.sg/view/' + self.ticker[:-3])
        tree = html.fromstring(response.text)
        ttm_yield = tree.xpath("/html/body/div/div[2]/div/div/div[1]/text()[6]")[0]
        ttm_yield = re.search(r"\d{1,5}\.\d{0,2}", ttm_yield)

        if ttm_yield:
            return ttm_yield.group(0)
        else:
            return "0.00"