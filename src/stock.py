import json
import pandas as pd

from common import *
from web import *


class Stock(object):

    @staticmethod
    def get_realtime_stock(symbol):

        output = {'symbol': symbol}

        url = yahoo_api_v8_template.replace('{symbol}', symbol)
        url = url.replace('{interval}', '1d')
        url = url.replace('{range}', '1d')
        ret, res = send_request(url)

        if ret != ERR_SUCCESS:
            return ret

        quote = Stock.__extract_quote(json.loads(res))

        output['open'] = quote['quote'][0]['open'][1]
        output['high'] = quote['quote'][0]['high'][1]
        output['low'] = quote['quote'][0]['low'][1]
        output['close'] = quote['quote'][0]['close'][1]
        output['volume'] = quote['quote'][0]['volume'][1]
        output['changeP'] = (output['close'] - quote['chartPreviousClose']) / quote['chartPreviousClose']

        output['open'] = "{:.2f}".format(output['open'])
        output['high'] = "{:.2f}".format(output['high'])
        output['low'] = "{:.2f}".format(output['low'])
        output['close'] = "{:.2f}".format(output['close'])
        output['volume'] = Stock.__human_format(output['volume'])
        output['changeP'] = "{:.2%}".format(output['changeP'])

        return ret, output

    @staticmethod
    def get_stock(symbol):

        ret1, output = Stock.get_realtime_stock(symbol)
        ret2 = Stock.__get_pv_avg_3mo(symbol, output)
        ret3 = Stock.__get_p_range_1y(symbol, output)

        if ret1 != ERR_SUCCESS or ret2 != ERR_SUCCESS or ret3 != ERR_SUCCESS:
            ret = ERR_GET_STOCK_ERROR
        else:
            ret = ERR_SUCCESS

        output['avg3mP'] = "{:.2f}".format(output['avg3mP'])
        output['avg3mV'] = Stock.__human_format(output['avg3mV'])
        output['strikeP1Y'] = "{0:.2f} - {1:.2f}".format(output['strikeP1Y'][0], output['strikeP1Y'][1])

        return ret, output

    @staticmethod
    def __get_pv_avg_3mo(symbol, output):

        url = yahoo_api_v8_template.replace('{symbol}', symbol)
        url = url.replace('{interval}', '1d')
        url = url.replace('{range}', '3mo')
        ret, res = send_request(url)

        if ret != ERR_SUCCESS:
            return ret

        quote = Stock.__extract_quote(json.loads(res))

        output['avg3mP'] = pd.Series(quote['quote'][0]['close']).mean()
        output['avg3mV'] = pd.Series(quote['quote'][0]['volume']).mean()

        return ERR_SUCCESS

    @staticmethod
    def __get_p_range_1y(symbol, output):

        url = yahoo_api_v8_template.replace('{symbol}', symbol)
        url = url.replace('{interval}', '1d')
        url = url.replace('{range}', '1y')
        ret, res = send_request(url)

        if ret != ERR_SUCCESS:
            return ret

        quote = Stock.__extract_quote(json.loads(res))
        output['strikeP1Y'] = [pd.Series(quote['quote'][0]['low']).min(), pd.Series(quote['quote'][0]['high']).max()]

        return ERR_SUCCESS

    @staticmethod
    def __extract_quote(data):

        output = {}

        output['timestamp'] = data['chart']['result'][0]['timestamp']
        output['quote'] = data['chart']['result'][0]['indicators']['quote']
        output['chartPreviousClose'] = data['chart']['result'][0]['meta']['chartPreviousClose']

        return output

    def __human_format(num):
        num = float('{:.4g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


