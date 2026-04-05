def summarize_stock_performance(ticker: str, ann_ret: float, ann_vol: float, max_dd: float, bench_ret: float = None) -> str:
    """Generates plain English summary for a single stock."""
    perf_word = "positive" if ann_ret > 0 else "negative"
    summary = f"{ticker} has had a {perf_word} annualized return of {ann_ret*100:.1f}%."
    
    if bench_ret is not None:
        if ann_ret > bench_ret:
            summary += f" It has outperformed the benchmark, which returned {bench_ret*100:.1f}% annualized."
        else:
            summary += f" It has underperformed the benchmark, which returned {bench_ret*100:.1f}% annualized."
            
    summary += f" Its annualized volatility was {ann_vol*100:.1f}%, taking on a maximum drawdown of {max_dd*100:.1f}%."
    return summary

def summarize_strategy_comparison(strat_ret: float, buy_hold_ret: float, strat_dd: float, buy_hold_dd: float) -> str:
    """Generates a summary comparing a strategy against buy & hold."""
    summary = []
    
    if strat_ret > buy_hold_ret:
        summary.append(f"The alternative strategy outperformed Buy and Hold on a total return basis ({strat_ret*100:.1f}% vs {buy_hold_ret*100:.1f}%).")
    else:
        summary.append(f"Over the selected time frame, Buy and Hold outperformed the alternative strategy on total return ({buy_hold_ret*100:.1f}% vs {strat_ret*100:.1f}%).")
        
    if strat_dd > buy_hold_dd:  # max_dd is negative, so > means closer to 0, which means smaller drawdown
        summary.append("The strategy successfully reduced the maximum drawdown, indicating better downside protection.")
    else:
        summary.append("The strategy experienced a deeper maximum drawdown compared to simply holding the asset.")
        
    return " ".join(summary)

def summarize_optimization(tickers: list, weights: list, opt_ret: float, bench_ret: float, opt_vol: float, opt_type: str) -> str:
    """Generates a plain English summary of the portfolio optimization result."""
    summary = f"This '{opt_type}' optimization heavily allocated capital across {len(tickers)} assets. "
    
    # Identify largest holding
    max_w = max(weights)
    max_idx = weights.index(max_w)
    max_ticker = tickers[max_idx]
    
    summary += f"The largest position is {max_ticker} at {max_w*100:.1f}%. "
    if max_w > 0.4:
        summary += "This portfolio is noticeably concentrated, which may increase stock-specific risk. "
        
    summary += f"Expected annualized return is {opt_ret*100:.1f}% at a volatility of {opt_vol*100:.1f}%."
    
    if bench_ret is not None:
        if opt_ret > bench_ret:
            summary += f" Compared with the benchmark, this portfolio has a higher expected return."
        else:
            summary += f" Compared with the benchmark, this portfolio has a lower expected return."
            
    return summary
