from execsim.engine.order import Order, Limit, Side, OrderType

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



def test_append_to_empty_level():
    level = Limit(limit_price=100)
    a = make_order(id_number=1,shares=100)

    level.append(a)

    assert level.head_order is a
    assert level.tail_order is a
    assert level.order_count == 1
    assert level.total_volume == 100
    assert a.parent_limit is level
    assert a.prev_order is None and a.next_order is None

def test_append_second_order_to_level():
    level = Limit(limit_price=100)
    a = make_order(id_number=1,shares=100)

    level.append(a)

    b = make_order(id_number=2,shares=200)

    level.append(b)

    assert level.head_order is a
    assert level.tail_order is b
    assert level.order_count == 2
    assert level.total_volume == 300
    assert b.parent_limit is level
    assert b.prev_order is a and a.next_order is b


def test_three_appends_to_empty_level():
    level = Limit(limit_price=100)

    a = make_order(id_number=1,shares=100)
    level.append(a)

    b = make_order(id_number=2,shares=200)
    level.append(b)

    c = make_order(id_number=3,shares=300)
    level.append(c)

    assert walk_forward(level)  == [1,2,3]
    assert walk_backward(level) == [3,2,1]
    assert level.order_count == 3
    assert level.total_volume == 600

def test_remove_only_order_from_level():
    level = Limit(limit_price=100)
    a = make_order(id_number=1,shares=100)
    level.append(a)

    level.remove(a)

    assert level.head_order is None
    assert level.tail_order is None
    assert level.order_count == 0
    assert level.total_volume == 0

def test_remove_head_order_from_level_of_three():
    level = Limit(limit_price=100)
    a = make_order(id_number=1,shares=100)
    level.append(a)
    b = make_order(id_number=2,shares=200)
    level.append(b)
    c = make_order(id_number=3,shares=300)
    level.append(c)

    level.remove(a)

    assert level.head_order is b
    assert level.tail_order is c
    assert level.order_count == 2
    assert level.total_volume == 500
    assert b.prev_order is None
    assert a.prev_order is None
    assert a.next_order is None
    assert a.parent_limit is None

def test_remove_middle_order_from_level_of_three():
    level = Limit(limit_price=100)
    a = make_order(id_number=1,shares=100)
    level.append(a)
    b = make_order(id_number=2,shares=200)
    level.append(b)
    c = make_order(id_number=3,shares=300)
    level.append(c)

    level.remove(b)

    assert level.head_order is a
    assert level.tail_order is c
    assert level.order_count == 2
    assert level.total_volume == 400
    assert c.prev_order is a
    assert a.next_order is b
    assert b.prev_order is None
    assert b.next_order is None
    assert b.parent_limit is None

def test_remove_tail_order_from_level_of_three():
    level = Limit(limit_price=100)
    a = make_order(id_number=1,shares=100)
    level.append(a)
    b = make_order(id_number=2,shares=200)
    level.append(b)
    c = make_order(id_number=3,shares=300)
    level.append(c)

    level.remove(c)

    assert level.head_order is a
    assert level.tail_order is b
    assert level.order_count == 2
    assert level.total_volume == 300
    assert b.next_order is None
    assert c.prev_order is None
    assert c.next_order is None
    assert c.parent_limit is None

def test_remove_then_append_middle_order():
    level = Limit(limit_price=100)
    a = make_order(id_number=1,shares=100)
    level.append(a)
    b = make_order(id_number=2,shares=200)
    level.append(b)
    c = make_order(id_number=3,shares=300)
    level.append(c)

    level.remove(b)
    level.append(b)

    assert level.tail_order is b
    assert b.prev_order is c
    assert b.next_order is None
    assert c.next_order is b
    assert c.prev_order is a
    assert level.order_count == 3
    assert level.total_volume == 600