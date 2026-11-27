from execsim.engine.order import Side
from execsim.engine.book import BookSide
from helpers import make_order, walk_forward, walk_backward
import pytest

def test_add_two_prices_and_check_best_price_at_both_sides():
    bids = BookSide(side=Side.BUY)
    asks = BookSide(side=Side.SELL)
    a = make_order(1,side=Side.BUY,shares=100,price=100)
    b = make_order(2,side=Side.BUY,shares=100,price=200)
    bids.add(a)
    bids.add(b)
    c = make_order(3,side=Side.SELL,shares=100,price=100)
    d = make_order(4,side=Side.SELL,shares=100,price=200)
    asks.add(c)
    asks.add(d)

    assert bids.best_price() == 200
    assert asks.best_price() == 100

def test_add_three_orders_and_cancel():
    bids = BookSide(side=Side.BUY)
    a = make_order(1,side=Side.BUY,shares=100,price=100)
    b = make_order(2,side=Side.BUY,shares=100,price=100)
    c = make_order(3,side=Side.BUY,shares=100,price=100)
    for order in (a,b,c):
        bids.add(order)
    bids.cancel(2) # order number of b
    level = bids.levels[100]
    assert walk_forward(level) == [1,3]
    assert walk_backward(level) == [3,1]

def test_cancel_only_order_at_best_price():
    bids = BookSide(side=Side.BUY)
    a = make_order(1,side=Side.BUY,shares=100,price=100)
    bids.add(a)
    bids.cancel(1)

    assert bids.best_price() == None
    assert 100 not in bids.levels

def test_cancel_order_at_best_price():
    bids = BookSide(side=Side.BUY)
    a = make_order(1,side=Side.BUY,shares=100,price=100)
    b = make_order(2,side=Side.BUY,shares=100,price=50)
    bids.add(a)
    bids.add(b)
    bids.cancel(1)

    assert bids.best_price() == 50
    assert 100 not in bids.levels
    assert 50 in bids.levels

def test_readd_price_after_level_deleted():
    bids = BookSide(side=Side.BUY)
    a = make_order(1,side=Side.BUY,shares=100,price=100)
    bids.add(a)
    bids.cancel(1)
    bids.add(a)
    bids.cancel(1)
    assert bids.best_price() is None

def test_unknown_id_on_cancel_raises_value_error():
    bids = BookSide(side=Side.BUY)
    a = make_order(1,side=Side.BUY,shares=100,price=100)
    bids.add(a)
    with pytest.raises(ValueError):
        bids.cancel(2)
    assert 100 in bids
    assert bids.best_price() == 100

def test_duplicate_id_on_add_raises_value_error():
    bids = BookSide(side=Side.BUY)
    a = make_order(1,side=Side.BUY,shares=100,price=100)
    b = make_order(1,side=Side.BUY,shares=100,price=100)
    bids.add(a)
    with pytest.raises(ValueError):
        bids.add(b)
    assert bids.levels[100].order_count == 1
    assert bids.levels[100].total_volume == 100

def test_add_wrong_side_order_raises_value_error():
    bids = BookSide(side=Side.BUY)
    a = make_order(1,side=Side.SELL,shares=100,price=100)
    with pytest.raises(ValueError):
        bids.add(a)
    assert bids.levels == {}
    assert bids.best_price() is None

def test_add_limit_order_with_price_none():
    bids=BookSide(side=Side.BUY)
    a = make_order(1,side=Side.BUY,shares=100,price=None)
    with pytest.raises(ValueError):
        bids.add(a)
    assert bids.levels == {}
    assert bids.best_price() is None