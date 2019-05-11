import json

from common import *
from web import *


class Stock(object):

    @staticmethod
    def get_realtime_stock(symbol):

        output = {}

        url = yahoo_api_v8_template.replace('{symbol}', symbol)
        url = url.replace('{interval}', '1d')
        url = url.replace('{range}', '1d')
        ret, res = send_request(url)

        if ret != ERR_SUCCESS:
            return ret, None

        data = Stock.__extract_quote(json.loads(res))

        output['open'] = data['quote'][0]['open'][1]
        output['high'] = data['quote'][0]['high'][1]
        output['low'] = data['quote'][0]['low'][1]
        output['close'] = data['quote'][0]['close'][1]
        output['volume'] = data['quote'][0]['volume'][1]
        output['change'] = (output['close'] - data['chartPreviousClose']) / data['chartPreviousClose']

        return ret, output

    @staticmethod
    def __extract_quote(data):

        output = {}
        output['timestamp'] = data['chart']['result'][0]['timestamp']
        output['quote'] = data['chart']['result'][0]['indicators']['quote']
        output['chartPreviousClose'] = data['chart']['result'][0]['meta']['chartPreviousClose']

        return output




