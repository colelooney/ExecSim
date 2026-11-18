from enum import Enum

class Order:
    def __init__(self, id_number, side, order_type, shares, entry_time, event_time, price = None, next_order = None, prev_order=None, parent_limit=None):
        self.id_number = id_number
        self.shares = shares
        self.original_shares = shares
        self.side = Side(side)
        self.order_type = OrderType(order_type)
        self.price = price
        self.entry_time = entry_time
        self.event_time = event_time
        self.next_order = next_order
        self.prev_order = prev_order
        self.parent_limit = parent_limit

class Limit: # single limit price
    def __init__(self, limit_price, order_count=0, total_volume=0, head_order=None, tail_order=None):
        self.limit_price = limit_price
        self.order_count = order_count
        self.total_volume = total_volume
        self.head_order = head_order
        self.tail_order = tail_order

class Side(Enum):
    BUY = 1
    SELL = 2

class OrderType(Enum):
    LIMIT = 1
    MARKET = 2
