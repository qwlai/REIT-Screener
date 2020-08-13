import pandas as pd 
import math

data = pd.read_csv("reit.csv") 

class KeyRatioScraper():
    def __init__(self, dict_of_reits):
        self.dict_of_reits = dict_of_reits

    def set_key_ratios(self):
        for ticker in self.dict_of_reits:
            row = data.loc[data['Ticker'] == ticker[:-3]]
            self.dict_of_reits[ticker]['nav'] = row['NAV'].values[0]
            self.dict_of_reits[ticker]['gearing_ratio'] = row['Gearing'].values[0]
            price = self.dict_of_reits[ticker]['price']
            self.dict_of_reits[ticker]['pnav'] = round(price / float(row['NAV'].values[0]), 2)
            if not math.isnan(float(row['WALEGRI'].values[0])):
                self.dict_of_reits[ticker]['wale_gri'] = row['WALEGRI'].values[0]
            if not math.isnan(float(row['WALENLA'].values[0])):
                self.dict_of_reits[ticker]['wale_nla'] = row['WALENLA'].values[0]
            if not math.isnan(float(row['Interest'].values[0])):
                self.dict_of_reits[ticker]['interest_ratio'] = row['Interest'].values[0]
