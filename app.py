import json
from flask import request, render_template, Flask
from libs.crawler.yahoo_crawler import YahooCrawler
from mongo_datatables import DataTables
from pymongo import MongoClient
import pprint
app = Flask(__name__, template_folder='templates')

#ODBU,LIW, BMGU

# tickers = ['A17U', 'C38U']

tickers = ['AJBU', 'AU8U', 'BTOU', 'BWCU', 'M44U', 'M1GU', 'TS0U', 'J69U', 'K71U', 'BUOU', 'K2LU', 'A17U', 'CRPU', 'SK6U', 'HMN', 'ME8U', 'UD1U', 'O5RU',
           'C2PU', 'OXMU', 'Q5T', 'ACV', 'T82U', 'AW9U', 'N2IU', 'P40U', 'RW0U', 'SV3U', 'XZL', 'J91U', 'MXNU', 'J85', 'JYEU', 'D5IU', 'CNNU', 'CMOU', 'C61U', 'C38U']


@app.route('/')
def index():
    client = MongoClient('localhost', 27017)
    db = client['REIT']
    collection = db['reit_info']
    result = collection.find().sort([('timestamp', -1)]).limit(1)[0]
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4433)
