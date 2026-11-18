# ExecSim
Independent project to learn more about order books and execution algos for sell-side quant

### Project Build Order

1. Matching Engine: price-time priority, limit/market/cancel orders and L2 snapshots.
2. Order Flow Generator: Poisson Arrivals + Hawkes Processes, potentially adding real data
3. Baseline Algos: TWAP, VWAP, POV, passive/aggresive mix with limit-order placement
4. Implementation shortfall / Almgren-Chriss for risk vs. impact trade-off.
5. RL agent for optimal liquidation
