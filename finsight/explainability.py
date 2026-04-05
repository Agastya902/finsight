def summarize_stock_performance(ticker: str, ann_ret: float, ann_vol: float, max_dd: float, bench_ret: float = None) -> str:
    """Generates an institutional, premium plain English summary for a single stock."""
    perf_desc = "yielded robust positive growth" if ann_ret > 0 else "experienced net depreciation in value"
    
    summary = f"Over the selected horizon, <b>{ticker}</b> {perf_desc}, generating an annualized return of <b>{ann_ret*100:.2f}%</b>. "
    
    if bench_ret is not None:
        if ann_ret > bench_ret:
            summary += f"This marks a significant outperformance relative to the benchmark index, which netted <b>{bench_ret*100:.2f}%</b> annualized. "
        else:
            summary += f"The asset lagged behind the broader benchmark index, which yielded <b>{bench_ret*100:.2f}%</b> annualized over the same period. "
            
    summary += f"This return profile was achieved alongside an annualized volatility of <b>{ann_vol*100:.2f}%</b> and a maximum drawdown depth of <b>{max_dd*100:.2f}%</b>. Investors should balance these specific volatility tolerances when considering capital allocation."
    return summary

def summarize_strategy_comparison(strat_ret: float, buy_hold_ret: float, strat_dd: float, buy_hold_dd: float) -> str:
    """Generates an institutional summary comparing an algorithmic strategy against buy & hold."""
    summary = []
    
    if strat_ret > buy_hold_ret:
        summary.append(f"The algorithmic alternative strategy <b>outperformed</b> traditional buy-and-hold dynamics on an absolute return basis ({strat_ret*100:.2f}% vs {buy_hold_ret*100:.2f}%).")
    else:
        summary.append(f"Over the selected time horizon, adhering to a <b>pure buy-and-hold allocation proved optimal</b> regarding total returns ({buy_hold_ret*100:.2f}% vs {strat_ret*100:.2f}%).")
        
    if strat_dd > buy_hold_dd:  # max_dd is usually negative, so > implies it represents less loss.
        summary.append("Importantly, the algorithmic strategy successfully neutralized tail-end risks, reducing maximum drawdown and enforcing <b>better downside protection</b>.")
    else:
        summary.append("However, the algorithmic strategy experienced deeper transient drawdowns, suggesting an elevated risk delta during capital troughs.")
        
    return " ".join(summary)

def summarize_optimization(tickers: list, weights: list, opt_ret: float, bench_ret: float, opt_vol: float, opt_type: str) -> str:
    """Generates an institutional summary of the MPT optimization results."""
    summary = f"Implementing a strict <b>'{opt_type}'</b> mandate, the model distributed aggregate capital across the {len(tickers)} specified securities. "
    
    # Identify largest holding
    max_w = max(weights)
    max_idx = weights.index(max_w)
    max_ticker = tickers[max_idx]
    
    summary += f"The algorithm assigned the highest capital concentration to <b>{max_ticker}</b> at an exact weight of <b>{max_w*100:.1f}%</b>. "
    
    if max_w > 0.4:
        summary += "Notice that this optimization drives significant portfolio concentration; clients must acknowledge potential exposure to single-asset idiosyncratic risk. "
        
    summary += f"Statistically, this construction expects a compound annualized growth rate of <b>{opt_ret*100:.2f}%</b> against a forward volatility profile of <b>{opt_vol*100:.2f}%</b>."
    
    if bench_ret is not None:
        if opt_ret > bench_ret:
            summary += f" Relative to benchmark dynamics, this weighting structure projects <b>favorable alpha</b> generation."
        else:
            summary += f" Relative to benchmark dynamics, this weighting produces a lower absolute yield but enforces the specified risk constraints."
            
    return summary
