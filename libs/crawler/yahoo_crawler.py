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
        dict_of_reits = self.get_asset_info()
        self.set_reit_info(dict_of_reits)

    def get_asset_info(self):
        yq_tickers = yq.Ticker(" ".join(self.yahoo_tickers))
        profiles = yq_tickers.asset_profile
        quotes = yq_tickers.quotes

        dict_of_reits = {}

        for idx, t in enumerate(self.yahoo_tickers):
            t_dict = {}
            key = t
            t_dict[key] = dict()

            t_dict[key]['industry'] = profiles[t]['industry'].replace("REIT—", "")
            t_dict[key]['website'] = profiles[t]['website']

            t_dict[key]['name'] = quotes[idx]['longName']
            t_dict[key]['market_cap'] = humanize.intword(
                quotes[idx]['marketCap'])
            t_dict[key]['price'] = quotes[idx]['regularMarketPrice']
            t_dict[key]['price_to_book'] = round(quotes[idx]['priceToBook'], 2)

            dict_of_reits.update(t_dict)
        return dict_of_reits

    def set_reit_info(self, dict_of_reits):
        for symbol in dict_of_reits:
            ticker = yq.Ticker(symbol)
            self.set_price_changes(symbol, ticker, dict_of_reits)
            self.set_dividend_yield_ttm(symbol, dict_of_reits)
            self.set_stock_distribution(symbol, ticker, dict_of_reits)
            self.set_ffo(symbol, ticker, dict_of_reits)

    def set_price_changes(self, symbol, ticker, dict_of_reits):
        current_price = dict_of_reits[symbol]['price']
        dict_of_reits[symbol]['day_change'] = self.get_daily_changes(
            ticker, current_price)
        dict_of_reits[symbol]['week_change'] = self.get_weekly_changes(
            ticker, current_price)
        dict_of_reits[symbol]['month_change'] = self.get_monthly_changes(
            ticker, current_price)
        dict_of_reits[symbol]['ytd_change'] = self.get_ytd_changes(
            ticker, current_price)

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

    def set_dividend_yield_ttm(self, symbol, dict_of_reits):
        response = requests.get('https://www.dividends.sg/view/' + symbol[:-3])
        tree = html.fromstring(response.text)
        ttm_yield = tree.xpath("/html/body/div/div[2]/div/div/div[1]/text()[6]")[0]
        ttm_yield = re.search(r"\d{1,5}\.\d{0,2}", ttm_yield)

        if ttm_yield:
            dict_of_reits[symbol]['dividend_yield'] = ttm_yield.group(0)
        else:
            dict_of_reits[symbol]['dividend_yield'] = "0.00"

    def set_stock_distribution(self, symbol, ticker, dict_of_reits):
        if not ticker.fund_ownership.empty:
            top_5_institutional_holders = ticker.fund_ownership.iloc[:5]
            cols = ['maxAge', 'reportDate', 'position', 'value']
            top_5_institutional_holders = top_5_institutional_holders.drop(cols, axis=1).to_dict('records')
            for i in top_5_institutional_holders:
                i['pctHeld'] = round(i['pctHeld'] * 100, 2)
            dict_of_reits[symbol]['institutional_holders'] = top_5_institutional_holders
        dict_of_reits[symbol]['insiders_held_percentage'] = round(ticker.major_holders[symbol]['insidersPercentHeld'] * 100, 2)
        dict_of_reits[symbol]['institutional_held_percentage'] = round(ticker.major_holders[symbol]['institutionsPercentHeld'] * 100, 2)

    def set_ffo(self, symbol, ticker, dict_of_reits):
        if 'unavailable' not in ticker.income_statement():
            df = ticker.income_statement().iloc[-2:]
            last_fy = df.iloc[0]
            ttm = df.iloc[1]

            last_fy_ffo = round(df.iloc[0]['OperatingIncome'] / df.iloc[0]['GrossProfit'] * 100, 2)
            dict_of_reits[symbol]['last_fy_ffo'] = last_fy_ffo

            ttm_ffo = round(df.iloc[1]['OperatingIncome'] / df.iloc[1]['GrossProfit'] * 100, 2)
            dict_of_reits[symbol]['ttm_ffo'] = ttm_ffo
