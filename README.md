# ExecSim
Independent project to learn more about order books and execution algos for sell-side quant

## Project Build Order

1. Matching Engine: price-time priority, limit/market/cancel orders and L2 snapshots.
2. Order Flow Generator: Poisson Arrivals + Hawkes Processes, potentially adding real data
3. Baseline Algos: TWAP, VWAP, POV, passive/aggresive mix with limit-order placement
4. Implementation shortfall / Almgren-Chriss for risk vs. impact trade-off.
5. RL agent for optimal liquidation

### Matching Engine Notes:
- Three main operations of LOB: add, cancel, and execute. Goal to implement in O(1) time.
- Add: place an order at the end of the list to be executed at a particular limit price
- Cancel: removes an order from anywhere in the book
- Execute: removes an order from the inside of the book
- Each operation keyed off an id number implying hash table will be efficient

### Current Status
- engine.order completed
- engine.book can now add and cancel orders, execution not yet implemented; all in O(1) time

### Next Steps
1. OrderBook: hold both sides of BookSide
2. events.py: define Trade
3. Matching.py: limit order matching
4. Market Orders
5. Check Invariants test

### Background Readings
- [How to Build a Fast Limit Order Book](https://web.archive.org/web/20110219163448/http://howtohft.wordpress.com/2011/02/15/how-to-build-a-fast-limit-order-book/)
