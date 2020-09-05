import json
import pandas as pd
import time
import datetime

from stock import *


class Notification(object):

    @staticmethod
    def do_scan(notification_setting):

        ret = ERR_SUCCESS
        notification_status = {'data': []}

        for stock in notification_setting['data']:

            if not stock['enable']:
                continue

            ret, data = Stock.get_notification_data(stock['symbol'])

            if ret != ERR_SUCCESS:
                continue

            stock_status = {}

            # pass data
            stock_status['symbol'] = data['symbol']
            stock_status['openP'] = data['openP']
            stock_status['highP'] = data['highP']
            stock_status['lowP'] = data['lowP']
            stock_status['closeP'] = data['closeP']
            stock_status['volume'] = data['volume']
            stock_status['changeP'] = data['changeP']

            # do scan
            stock_status['messages'] = []

            for scan in stock['edit']:
                Notification.ScanFuncDict[scan["type"]](stock_status, data['data_3mo'], scan)

            # push to data
            notification_status['data'].append(stock_status)

        return ret, notification_status

    # scan methods
    @staticmethod
    def ArrivalPrice(stock_status, data_3mo, scan):

        price = float(stock_status['closeP'])
        if ('GreaterThan' in scan['args'] and price > float(scan['args']['GreaterThan'])) or \
            ('LessThan' in scan['args'] and price < float(scan['args']['LessThan'])):
            stock_status['messages'].append({'name': scan['name'], 'trigger': True})

        return

    @staticmethod
    def TrailingStop(stock_status, data_3mo, scan):

        price_now = float(stock_status['closeP'])
        quote = data_3mo['quote']
        start_date = time.mktime(datetime.datetime.strptime(scan['args']['StartDate'], "%Y%m%d").timetuple())

        max_p = 0
        min_p = 1000000.0
        trigger = False
        for i, v in enumerate(data_3mo['timestamp']):
            if v >= start_date:
                max_p = max(max_p, quote[0]['high'][i])
                min_p = min(min_p, quote[0]['low'][i])

                if ('SellAmt' in scan['args'] and price_now <= max_p - float(scan['args']['SellAmt'])) or \
                    ('SellP' in scan['args'] and (max_p - price_now) / max_p >= float(scan['args']['SellP'])/100) or \
                    ('BuyAmt' in scan['args'] and price_now >= min_p + float(scan['args']['BuyAmt'])) or \
                    ('BuyP' in scan['args'] and (price_now - min_p) / min_p >= float(scan['args']['BuyP']) / 100):
                    trigger = True
                    break
        if trigger:
            stock_status['messages'].append({'name': scan['name'], 'trigger': True})

        return

    @staticmethod
    def MA(stock_status, scan):
        pass

    ScanFuncDict = {
        'ArrivalPrice': ArrivalPrice.__get__(object),
        'TrailingStop': TrailingStop.__get__(object),
        'MA': MA.__get__(object)
    }
