from libs.crawler.yahoo_crawler import YahooCrawler

#ODBU,LIW, BMGU
tickers = ['AJBU', 'AU8U', 'BTOU', 'BWCU', 'M44U', 'M1GU', 'TS0U', 'J69U', 'K71U', 'BUOU', 'K2LU', 'A17U', 'CRPU', 'SK6U', 'HMN', 'ME8U', 'UD1U', 'O5RU',
           'C2PU', 'OXMU', 'Q5T', 'ACV', 'T82U', 'AW9U', 'N2IU', 'P40U', 'RW0U', 'SV3U', 'XZL', 'J91U', 'MXNU', 'J85', 'JYEU', 'D5IU', 'CNNU', 'CMOU', 'C61U', 'C38U']
yq = YahooCrawler(tickers)
yq.get_tickers_info()
