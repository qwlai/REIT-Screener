import yahooquery as yq
import pprint
import humanize
import requests
from lxml import html
import re


class YahooCrawler():
    def __init__(self, reit_tickers):
        self.reit_tickers = reit_tickers
        self.yahoo_tickers = [ticker + ".SI" for ticker in self.reit_tickers]

    def get_tickers_info(self):
        yq_tickers = yq.Ticker(" ".join(self.yahoo_tickers))

        dict_of_reits = self.get_asset_info(yq_tickers)
        self.set_price_changes(dict_of_reits)
        self.set_dividend_yield_ttm(dict_of_reits)

    def get_asset_info(self, yq_tickers):
        profiles = yq_tickers.asset_profile
        prices = yq_tickers.price
        
        dict_of_reits = {}

        for t in self.yahoo_tickers:
            t_dict = {}
            key = t
            t_dict[key] = dict()
            
            t_dict[key]['industry'] = profiles[t]['industry'].replace("REIT—", "")
            t_dict[key]['website'] = profiles[t]['website']
            
            t_dict[key]['name'] = prices[t]['longName']
            t_dict[key]['market_cap'] = humanize.intword(prices[t]['marketCap'])
            t_dict[key]['price'] = prices[t]['regularMarketPrice']
            dict_of_reits.update(t_dict)
        return dict_of_reits
    
    def set_price_changes(self, dict_of_reits):
        for reit in dict_of_reits:
            print(reit)
            current_price = dict_of_reits[reit]['price']
            ticker = yq.Ticker(reit)
            dict_of_reits[reit]['day_change'] = self.get_daily_changes(ticker, current_price)
            dict_of_reits[reit]['week_change'] = self.get_weekly_changes(ticker, current_price)
            dict_of_reits[reit]['month_change'] = self.get_monthly_changes(ticker, current_price)
            dict_of_reits[reit]['ytd_change'] = self.get_ytd_changes(ticker, current_price)   
        
    def get_daily_changes(self, ticker, price):
        day_1 = ticker.history('1d')['open'].iloc[0]
        return round(((price - day_1) / day_1) * 100, 2)
    
    def get_weekly_changes(self, ticker, price):
        day_1 = ticker.history('5d')['open'].iloc[0]
        return round(((price - day_1) / day_1) * 100, 2)
    
    def get_monthly_changes(self, ticker, price):
        day_1 = ticker.history('1mo')['open'].iloc[0]
        return round(((price - day_1) / day_1) * 100, 2)

    def get_ytd_changes(self, ticker, price):
        day_1 = ticker.history()['open'].iloc[0]
        return round(((price - day_1) / day_1) * 100, 2)

    def set_dividend_yield_ttm(self, dict_of_reits):
        for reit in dict_of_reits:
            response = requests.get('https://www.dividends.sg/view/' + reit[:-3])
            tree = html.fromstring(response.text)
            ttm_yield = tree.xpath("/html/body/div/div[2]/div/div/div[1]/text()[6]")[0]
            ttm_yield = re.search(r"\d{1,5}\.\d{0,2}", ttm_yield)
            
            if ttm_yield:
                dict_of_reits[reit]['dividend_yield'] = ttm_yield.group(0)
            else:
                dict_of_reits[reit]['dividend_yield'] = "0.00"

    # def get_stock_distribution(self, ticker):
    #     top_5_institutional_holders = ticker.institutional_holders.iloc[:5]
    #     cols = ['Shares', 'Date Reported', 'Value']
    #     top_5_institutional_holders = top_5_institutional_holders.drop(cols, axis=1).to_dict('records')
    #     return ticker.major_holders[0][0], ticker.major_holders[0][1], ticker.major_holders[0][3], top_5_institutional_holders

    # def get_ffo(self, ticker):
        # print(ticker.financials)
        # print(ticker.balance_sheet)
