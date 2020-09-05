from core import *


def test_generator():
    stock_list = ['T', 'COST']
    for stock in stock_list:
        yield get_realtime_stock, stock
        yield get_stock, stock


def get_realtime_stock(symbol):
    result = ChaldeaStockObservatoryCore.get_realtime_stock(symbol)
    assert result is not None
    assert result['symbol'] is not None, result
    assert result['openP'] is not None, result
    assert result['highP'] is not None, result
    assert result['lowP'] is not None, result
    assert result['closeP'] is not None, result
    assert result['volume'] is not None, result
    assert result['changeP'] is not None, result


def get_stock(symbol):
    result = ChaldeaStockObservatoryCore.get_stock(symbol)
    assert result is not None
    assert result['symbol'] is not None, result
    assert result['openP'] is not None, result
    assert result['highP'] is not None, result
    assert result['lowP'] is not None, result
    assert result['closeP'] is not None, result
    assert result['volume'] is not None, result
    assert result['changeP'] is not None, result
    assert result['avg3mP'] is not None, result
    assert result['avg3mV'] is not None, result
    assert result['strikeP1Y'] is not None, result

