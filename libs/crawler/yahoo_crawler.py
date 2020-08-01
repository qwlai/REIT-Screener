import yfinance as yf
import pprint
import humanize
import requests
from lxml import html
import re


class YahooCrawler():
    def __init__(self, tickers):
        self.tickers = tickers

    def get_tickers_info(self):
        tickers = [ticker + ".SI" for ticker in self.tickers]
        yf_tickers = yf.Tickers(" ".join(tickers)).tickers
        for idx, ticker in enumerate(yf_tickers):
            name = ticker.info['longName']
            industry = ticker.info['industry']
            market_cap = humanize.intword(ticker.info['marketCap'])
            price = ticker.info['regularMarketPrice']
            print(self.get_dividend_yield_ttm(ticker, price, idx))

            day_diff = self.get_day_diff(ticker, price)
            week_diff = self.get_weekly_diff(ticker, price)
            month_diff = self.get_monthly_diff(ticker, price)
            ytd_diff = self.get_ytd_diff(ticker, price)

    def get_day_diff(self, ticker, price):
        return ((price - ticker.info['previousClose']) / ticker.info['previousClose']) * 100

    def get_weekly_diff(self, ticker, price):
        history = ticker.history(period="5d")
        last_week_closing_price = history['Close'].iloc[0]
        return ((price - last_week_closing_price) / last_week_closing_price) * 100

    def get_monthly_diff(self, ticker, price):
        history = ticker.history(period="1mo")
        last_month_closing_price = history['Close'].iloc[0]
        return ((price - last_month_closing_price) / last_month_closing_price) * 100

    def get_ytd_diff(self, ticker, price):
        history = ticker.history(period="ytd")
        ytd_closing_price = history['Close'].iloc[0]
        ytd_diff = ((price - ytd_closing_price) / ytd_closing_price) * 100

    def get_dividend_yield_ttm(self, ticker, price, idx):
        response = requests.get(
            'https://www.dividends.sg/view/' + self.tickers[idx])
        tree = html.fromstring(response.text)
        ttm_yield = tree.xpath(
            "/html/body/div/div[2]/div/div/div[1]/text()[6]")[0]
        ttm_yield = re.search(r"\d{1,5}\.\d{0,2}%", ttm_yield)
        if ttm_yield:
            return ttm_yield.group(0)
        else:
            return "0.00%"
