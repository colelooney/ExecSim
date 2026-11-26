from execsim.engine.order import Order, Limit, Side, OrderType
import pytest

def make_order(id_number,shares=100):
    return Order(id_number,Side.BUY,OrderType.LIMIT,shares,
                 entry_time=0,event_time=0,price=100)

### helpers
def walk_forward(level):
    ids = []
    order = level.head_order
    while order is not None:
        ids.append(order.id_number)
        order = order.next_order
    return ids

def walk_backward(level):
    ids = []
    order = level.tail_order
    while order is not None:
        ids.append(order.id_number)
        order = order.prev_order
    return ids

def make_level(*share_counts):
    level = Limit(limit_price=100)
    orders = [make_order(i + 1, s) for i, s in enumerate(share_counts)]
    for o in orders:
        level.append(o)
    return level, orders



def test_append_to_empty_level():
    level, (a,) = make_level(100)

    assert level.head_order is a
    assert level.tail_order is a
    assert level.order_count == 1
    assert level.total_volume == 100
    assert a.parent_limit is level
    assert a.prev_order is None and a.next_order is None

def test_append_second_order_to_level():
    level, (a, b) = make_level(100, 200)

    assert level.head_order is a
    assert level.tail_order is b
    assert level.order_count == 2
    assert level.total_volume == 300
    assert b.parent_limit is level
    assert b.prev_order is a and a.next_order is b


def test_three_appends_to_empty_level():
    level, (a, b, c) = make_level(100, 200, 300)

    assert walk_forward(level)  == [1,2,3]
    assert walk_backward(level) == [3,2,1]
    assert level.order_count == 3
    assert level.total_volume == 600

def test_remove_only_order_from_level():
    level, (a,) = make_level(100)

    level.remove(a)

    assert level.head_order is None
    assert level.tail_order is None
    assert level.order_count == 0
    assert level.total_volume == 0
    assert a.prev_order is None
    assert a.next_order is None
    assert a.parent_limit is None
    assert walk_forward(level)  == []
    assert walk_backward(level) == []


def test_remove_head_order_from_level_of_three():
    level, (a, b, c) = make_level(100, 200, 300)

    level.remove(a)

    assert level.head_order is b
    assert level.tail_order is c
    assert level.order_count == 2
    assert level.total_volume == 500
    assert b.prev_order is None
    assert a.prev_order is None
    assert a.next_order is None
    assert a.parent_limit is None
    assert walk_forward(level)  == [2,3]
    assert walk_backward(level) == [3,2]

def test_remove_middle_order_from_level_of_three():
    level, (a, b, c) = make_level(100, 200, 300)

    level.remove(b)

    assert level.head_order is a
    assert level.tail_order is c
    assert level.order_count == 2
    assert level.total_volume == 400
    assert c.prev_order is a
    assert a.next_order is c
    assert b.prev_order is None
    assert b.next_order is None
    assert b.parent_limit is None
    assert walk_forward(level)  == [1,3]
    assert walk_backward(level) == [3,1]

def test_remove_tail_order_from_level_of_three():
    level, (a, b, c) = make_level(100, 200, 300)

    level.remove(c)

    assert level.head_order is a
    assert level.tail_order is b
    assert level.order_count == 2
    assert level.total_volume == 300
    assert b.next_order is None
    assert c.prev_order is None
    assert c.next_order is None
    assert c.parent_limit is None
    assert walk_forward(level)  == [1,2]
    assert walk_backward(level) == [2,1]

def test_remove_then_append_middle_order():
    level, (a, b, c) = make_level(100, 200, 300)

    level.remove(b)
    level.append(b)

    assert level.tail_order is b
    assert b.prev_order is c
    assert b.next_order is None
    assert c.next_order is b
    assert c.prev_order is a
    assert level.order_count == 3
    assert level.total_volume == 600
    assert walk_forward(level)  == [1,3,2]
    assert walk_backward(level) == [2,3,1]

def test_remove_two_head_orders():
    level, (a, b, c) = make_level(100, 200, 300)

    level.remove(a)
    level.remove(b)

    assert level.tail_order is c
    assert level.head_order is c
    assert c.prev_order is None
    assert c.next_order is None
    assert level.order_count == 1
    assert level.total_volume == 300
    assert walk_forward(level)  == [3]
    assert walk_backward(level) == [3]

def test_partial_reduce_quantity():
    level, (a, b, c) = make_level(100, 200, 300)
    level.reduce(a,10)

    assert level.order_count == 3
    assert level.total_volume == 590
    assert walk_forward(level)  == [1,2,3]
    assert walk_backward(level) == [3,2,1]
    assert a.shares == 90
    assert a.original_shares == 100

def test_reduce_by_more_than_available_raises_value_error():
    level, (a, b, c) = make_level(100, 200, 300)
    with pytest.raises(ValueError) as excinfo:
        level.reduce(a,200)
    assert a.shares == 100
    assert level.total_volume == 600


def test_reduce_by_exactly_number_of_available_shares_does_not_remove():
    level, (a, b, c) = make_level(100, 200, 300)
    level.reduce(b,200)

    assert walk_forward(level)  == [1,2,3]
    assert walk_backward(level) == [3,2,1]
    assert b.shares == 0
    assert a.next_order is b
    assert b.prev_order is a
    assert level.order_count == 3
    assert level.total_volume == 400

def test_reduce_an_order_not_in_this_limit_raises_error():
    level, (a,b,c) = make_level(100,200,300)
    level2, (d,) = make_level(400)
    with pytest.raises(ValueError):
        level.reduce(d,400)
    assert walk_forward(level)  == [1,2,3]
    assert walk_backward(level) == [3,2,1]
    assert walk_forward(level2)  == [1]
    assert walk_backward(level2) == [1]
    assert d.shares == 400
    assert level2.order_count == 1
    assert level.order_count == 3
    assert level2.total_volume == 400
    assert level.total_volume == 600

def test_reduce_an_already_removed_order():
    level, (a, b, c) = make_level(100, 200, 300)
    level.remove(a)
    with pytest.raises(ValueError):
        level.reduce(a,100)
    assert walk_forward(level) == [2,3]
    assert walk_backward(level) == [3,2]
    assert level.order_count == 2
    assert level.total_volume == 500
    assert a.parent_limit is None
    assert a.next_order is None
    assert a.prev_order is None

def test_reduce_by_non_negative_value():
    level, (a, b, c) = make_level(100, 200, 300)
    with pytest.raises(ValueError):
        level.reduce(a,0)
    with pytest.raises(ValueError):
        level.reduce(b,-10)
    assert a.shares == 100
    assert b.shares == 200
    assert level.total_volume == 600
    assert level.order_count == 3