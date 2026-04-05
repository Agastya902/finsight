def summarize_stock_performance(ticker: str, ann_ret: float, ann_vol: float, max_dd: float, bench_ret: float = None) -> str:
    """Generates clear, concise analyst commentary for single equities."""
    summary = f"**Research Note — {ticker}**\n\n"
    summary += f"Over the selected timeframe, **{ticker}** returned an annualized **{ann_ret*100:.2f}%**. "
    
    if bench_ret is not None:
        if ann_ret > bench_ret:
            summary += f"This outperformed the benchmark by **{(ann_ret - bench_ret)*100:.2f}%** on a relative basis. "
        else:
            summary += f"This underperformed the benchmark by **{abs(bench_ret - ann_ret)*100:.2f}%**. "
            
    summary += f"\n\nThe asset exhibited **{ann_vol*100:.2f}%** annualized volatility and experienced a worst-case drawdown of **{max_dd*100:.2f}%**. Consider this historical downside risk when scaling positions."
    return summary

def summarize_strategy_comparison(strat_ret: float, buy_hold_ret: float, strat_dd: float, buy_hold_dd: float) -> str:
    """Generates concise comparative analysis for the algorithmic strategy."""
    summary = "**Backtest Summary**\n\n"
    
    if strat_ret > buy_hold_ret:
        summary += f"The moving average strategy **outperformed** a passive holding strategy, generating a CAGR of **{strat_ret*100:.2f}%** compared to the baseline **{buy_hold_ret*100:.2f}%**. "
    else:
        summary += f"The passive 'buy and hold' approach **outperformed** the algorithmic overlay in absolute returns (**{buy_hold_ret*100:.2f}%** vs **{strat_ret*100:.2f}%**). "
        
    summary += "\n\n"
    
    if strat_dd > buy_hold_dd:
        summary += f"Importantly, the algorithmic model successfully reduced tail risk, limiting the maximum drawdown to **{strat_dd*100:.2f}%** (better than the baseline **{buy_hold_dd*100:.2f}%** loss)."
    else:
        summary += f"Furthermore, the strategy strategy failed to provide downside protection, resulting in a steeper maximum drawdown (**{strat_dd*100:.2f}%**) than simply holding the underlying asset (**{buy_hold_dd*100:.2f}%**)."
        
    return summary

def summarize_optimization(tickers: list, weights: list, opt_ret: float, bench_ret: float, opt_vol: float, opt_type: str) -> str:
    """Generates clean structural breakdowns of generated portfolios."""
    summary = f"**Portfolio Architecture**\n\n"
    summary += f"Optimizing for '{opt_type}' across {len(tickers)} assets resulted in a distinct concentration. "
    
    max_w = max(weights)
    max_idx = weights.index(max_w)
    max_ticker = tickers[max_idx]
    
    summary += f"The largest allocation is **{max_w*100:.1f}% to {max_ticker}**. "
    
    if max_w > 0.4:
        summary += "This indicates high single-asset concentration. Monitor correlation risks tightly. "
        
    summary += f"\n\nBased on historical variance, this specific allocation targets an annualized return of **{opt_ret*100:.2f}%** against **{opt_vol*100:.2f}%** volatility."
            
    return summary
