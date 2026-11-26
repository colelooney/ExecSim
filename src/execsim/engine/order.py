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

    def remove(self,order):
        if order.prev_order is None: # remove head order
            if order.next_order is not None:
                self.head_order = order.next_order
                self.head_order.prev_order = None
            else:
                self.head_order = None # single order case
                self.tail_order = None
        elif order.next_order is None: #remove tail order
            self.tail_order = order.prev_order # single order case already considered above
            self.tail_order.next_order = None
        else: # middle case
            order.prev_order.next_order = order.next_order
            order.next_order.prev_order = order.prev_order
        self.order_count -= 1
        self.total_volume -= order.shares

        order.next_order = None
        order.prev_order = None
        order.parent_limit = None

    def reduce(self,order,qty):
        if order.parent_limit is not self:
            raise ValueError("Order is not in this level")
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        if qty > order.shares:
            raise ValueError("Quantity must not exceed number of shares")
        order.shares -= qty
        self.total_volume -= qty