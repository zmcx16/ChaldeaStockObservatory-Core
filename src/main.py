import sys
import zerorpc


class ChaldeaStockObservatoryCore(object):

    @staticmethod
    def test(cmd):
        return cmd


if __name__ == "__main__":
    s = zerorpc.Server(ChaldeaStockObservatoryCore())
    s.bind("tcp://0.0.0.0:" + sys.argv[1])
    s.run()