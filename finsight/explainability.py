def summarize_stock_performance(ticker: str, ann_ret: float, ann_vol: float, max_dd: float, bench_ret: float = None) -> str:
    """Generates institutional investment research commentary for single equities."""
    summary = f"<b>Research Note — {ticker}</b><br><br>"
    summary += f"Over the observed investment horizon, <b>{ticker}</b> generated an annualized yield of <b>{ann_ret*100:.2f}%</b>, "
    
    if bench_ret is not None:
        if ann_ret > bench_ret:
            summary += f"representing definitive alpha generation against the designated benchmark (+{(ann_ret - bench_ret)*100:.2f}% relative outperformance). "
        else:
            summary += f"which trailed the broader benchmark aggregate by {abs(bench_ret - ann_ret)*100:.2f}%. "
            
    summary += f"<br><br>The asset's risk topology exhibits an annualized volatility profile of <b>{ann_vol*100:.2f}%</b> and a maximum historical drawdown vector of <b>{max_dd*100:.2f}%</b>. Institutional managers must strictly evaluate these idiosyncratic downside risks when sizing systematic exposures."
    return summary

def summarize_strategy_comparison(strat_ret: float, buy_hold_ret: float, strat_dd: float, buy_hold_dd: float) -> str:
    """Generates institutional commentary comparing an algorithmic overlay to passive holding."""
    summary = "<b>Quantitative Output Assessment</b><br><br>"
    
    if strat_ret > buy_hold_ret:
        summary += f"The systematic overlay <b>materially outperformed</b> the passive accumulation strategy on an absolute basis, returning a CAGR of {strat_ret*100:.2f}% vs the passive benchmark yield of {buy_hold_ret*100:.2f}%. "
    else:
        summary += f"Empirical backtesting indicates that the <b>passive buy-and-hold methodology dominates</b> the algorithmic overlay on absolute yields ({buy_hold_ret*100:.2f}% vs {strat_ret*100:.2f}%). "
        
    summary += "<br><br>"
    
    if strat_dd > buy_hold_dd:  # max_dd is usually negative, so > implies closer to zero (less loss).
        summary += f"However, the fundamental merit of the systemic approach resides in its risk mitigation footprint. The model significantly truncated tail risk, capping maximum drawdowns at {strat_dd*100:.2f}% (compared to a baseline exposure of {buy_hold_dd*100:.2f}%), signaling institutional-grade downside protection."
    else:
        summary += f"Furthermore, the signal-driven strategy experienced amplified downside beta dynamics, forcing deeper transient drawdowns ({strat_dd*100:.2f}% vs {buy_hold_dd*100:.2f}%) compared to raw asset ownership."
        
    return summary

def summarize_optimization(tickers: list, weights: list, opt_ret: float, bench_ret: float, opt_vol: float, opt_type: str) -> str:
    """Generates institutional commentary on the exact portfolio allocations and implied efficient frontiers."""
    summary = f"<b>Portfolio Architecture Statement</b><br><br>"
    summary += f"The specified mandate ('{opt_type}') resolves to a non-linear optimal capital distribution traversing {len(tickers)} discrete securities. "
    
    max_w = max(weights)
    max_idx = weights.index(max_w)
    max_ticker = tickers[max_idx]
    
    summary += f"Optimization algorithms dictate an apex allocation of <b>{max_w*100:.1f}% toward {max_ticker}</b>. "
    
    if max_w > 0.4:
        summary += "Due to the rigorous parameters applied, the resulting allocation displays severe concentration metrics. Institutional portfolios should monitor correlation collapse scenarios regarding this dense specific-asset exposure. "
        
    summary += f"<br><br>Statistically, the combined topology forecasts an expected annualized rate of return mapping to <b>{opt_ret*100:.2f}%</b> set against a deterministic volatility profile of <b>{opt_vol*100:.2f}%</b>."
            
    return summary
