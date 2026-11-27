from order import Order, Side, OrderType, Limit

class BookSide:
    def __init__(self,side):
        self.side = Side(side)
        self.levels = {} # maps price to limit holding the queue
        self.orders = {} # maps order id to its order
        self.heap = [] # find best price quickly

    def add(self,order):
        if order.price in self.levels:
            self.levels[order.price].append(order)
        else:
            self.levels[order.price] = Limit().append(order)
        self.orders[order.id_number] = order
