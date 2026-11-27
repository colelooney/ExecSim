from execsim.engine.order import Order, Side, OrderType, Limit

def make_order(id_number,side=Side.BUY,shares=100,price=100):
    return Order(id_number,side,OrderType.LIMIT,shares,
                 entry_time=0,event_time=0,price=price)

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
    orders = [make_order(i + 1, shares=s) for i, s in enumerate(share_counts)]
    for o in orders:
        level.append(o)
    return level, orders