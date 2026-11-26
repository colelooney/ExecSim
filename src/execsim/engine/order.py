from enum import Enum

class Order:
    def __init__(self, id_number, side, order_type, shares, entry_time, event_time, price = None, next_order = None, prev_order=None, parent_limit=None):
        self.id_number = id_number # type int, unique
        self.shares = shares # type int, remaining quantity
        self.original_shares = shares # type int
        self.side = Side(side) # type: Side
        self.order_type = OrderType(order_type) # type OrderType
        self.price = price # type int|None
        self.entry_time = entry_time # int
        self.event_time = event_time # int
        self.next_order = next_order # type Order | None
        self.prev_order = prev_order # type Order | None
        self.parent_limit = parent_limit # type Limit | None

class Side(Enum):
    BUY = 1
    SELL = 2

class OrderType(Enum):
    LIMIT = 1
    MARKET = 2

class Limit: # single limit price
    def __init__(self, limit_price, order_count=0, total_volume=0, head_order=None, tail_order=None):
        self.limit_price = limit_price # int
        self.order_count = order_count # int
        self.total_volume = total_volume # int
        self.head_order = head_order # front ## Order| None
        self.tail_order = tail_order # back ## Order | None

    def append(self,order):
        # Clear stale orders
        order.next_order = None
        order.prev_order = None
        order.parent_limit = self # parent limit is the limit the order lives in
        if self.tail_order is not None:
            self.tail_order.next_order = order
            order.prev_order = self.tail_order
        else:
            self.head_order = order
        self.tail_order = order
        self.order_count += 1
        self.total_volume += order.shares
