import sys
import argparse
import zerorpc

from stock import *


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
    def test(cmd):
        return cmd


if __name__ == "__main__":
    #print(ChaldeaStockObservatoryCore.get_stock('T'))
    parser = argparse.ArgumentParser()
    parser.add_argument("-port", dest="port")
    args = parser.parse_args()
    if args.port:
        s = zerorpc.Server(ChaldeaStockObservatoryCore())
        s.bind("tcp://0.0.0.0:" + args.port)
        s.run()
    else:
        print('Need assign port.')



