import argparse
import zerorpc

from stock import *
from notification import *

class ChaldeaStockObservatoryCore(object):

    @staticmethod
    def get_realtime_stock(symbol):

        ret, output = Stock.get_realtime_stock(symbol)
        if ret == ERR_SUCCESS:
            return output
        else:
            return None

    @staticmethod
    def get_stock(symbol):

        ret, output = Stock.get_stock(symbol)
        if ret == ERR_SUCCESS:
            return output
        else:
            return None

    @staticmethod
    def scan_notification(notification_setting):

        ret, notification_status = Notification.do_scan(notification_setting)
        if ret == ERR_SUCCESS:
            return notification_status
        else:
            return None

    @staticmethod
    def test(cmd):
        return cmd


if __name__ == "__main__":
    #print(ChaldeaStockObservatoryCore.get_stock('T'))
    #notification_setting = {"data": [{"edit": [
    #                    {"args": {"BuyP": "2", "StartDate": "20190718"}, "name": "TBV", "type": "TrailingStop"}],
    #           "enable": True, "symbol": "SLM"}]}
    #print(ChaldeaStockObservatoryCore.scan_notification(notification_setting))
    parser = argparse.ArgumentParser()
    parser.add_argument("-port", dest="port")
    args = parser.parse_args()
    if args.port:
        s = zerorpc.Server(ChaldeaStockObservatoryCore())
        s.bind("tcp://0.0.0.0:" + args.port)
        s.run()
    else:
        print('Need assign port.')



