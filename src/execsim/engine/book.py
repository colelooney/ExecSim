from execsim.engine.order import Order, Side, OrderType, Limit
import heapq

class BookSide:
    """
    Methods:
    add(order): add an order to the order book
    cancel(order_id): look up an order an remove 
    best_price() pop prices no longer in levels then return top
    best_level(): limit at its best price
    """
    def __init__(self,side):
        self.side = Side(side)
        self.levels = {} # maps price to limit holding the queue
        self.orders = {} # maps order id to its order
        self.heap = [] # find best price quickly
        self.store_sign = -1 if self.side == Side.BUY else 1

    def add(self,order):
        if order.side is not self.side:
            raise ValueError('Order side must match book side')
        if order.id_number in self.orders:
            raise ValueError('Order id number must be unique')
        if order.price is None:
            raise ValueError('Order price must have value')
        if order.price in self.levels:
            self.levels[order.price].append(order)
        else:
            self.levels[order.price] = Limit(order.price)
            self.levels[order.price].append(order)
            heapq.heappush(self.heap,self.store_sign * order.price) # only push new price to heap   
        self.orders[order.id_number] = order

    def cancel(self,order_id):
        if order_id not in self.orders:
            raise ValueError("Order id must be in book")
        order = self.orders[order_id]
        self.levels[order.price].remove(order)
        del self.orders[order_id]
        if self.levels[order.price].order_count == 0:
            del self.levels[order.price]

    def best_price(self):
        while self.heap != [] and self.store_sign * self.heap[0] not in self.levels:
            heapq.heappop(self.heap)
        if self.heap == []:
            return None
        return self.store_sign*self.heap[0]