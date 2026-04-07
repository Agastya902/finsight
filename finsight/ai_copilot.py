"""
Fin — FinSight's AI Analyst
Context-aware heuristic response engine.
"""

def generate_response(query: str, context: dict) -> str:
    """Generates a clean, friendly, analyst-grade response based on current dashboard state."""
    q = query.lower().strip()

    asset = context.get('asset', 'the selected asset')
    bench = context.get('benchmark', 'the benchmark')
    horizon = context.get('horizon', 'the selected period')
    sharpe = context.get('sharpe', None)
    ann_ret = context.get('ann_ret', None)
    vol = context.get('vol', None)
    max_dd = context.get('max_dd', None)

    # ── Sharpe ──
    if any(k in q for k in ["sharpe", "sharpe ratio", "risk adjusted"]):
        if sharpe:
            s = float(sharpe) if sharpe != 'N/A' else None
            if s is not None:
                quality = "strong" if s > 1.0 else "moderate" if s > 0.5 else "weak"
                return (f"Your current Sharpe ratio is **{sharpe}**, which indicates **{quality}** "
                        f"risk-adjusted performance.\n\n"
                        f"In simple terms: for every unit of risk you're taking, you're earning "
                        f"{'more' if s > 1 else 'less'} than 1 unit of return. "
                        f"{'This is a solid result — the strategy is being compensated well for its volatility.' if s > 1 else 'Consider whether the returns justify the risk you are exposed to.'}")
        return "The Sharpe ratio measures return per unit of risk. A ratio above 1.0 is generally considered good — it means you're being adequately compensated for the volatility."

    # ── Risk / Drawdown ──
    if any(k in q for k in ["risk", "risky", "drawdown", "loss", "downside"]):
        if max_dd and max_dd != 'N/A':
            return (f"The maximum drawdown is **{max_dd}**, which represents the largest peak-to-trough "
                    f"decline in the selected period.\n\n"
                    f"Think of it as the worst-case scenario: if you had invested at the peak, this is "
                    f"how much you could have lost before recovery. To reduce drawdown risk, consider "
                    f"diversifying across uncorrelated assets in the Portfolio Builder.")
        return "Drawdown measures the largest drop from a peak. It's a key indicator of downside risk — the lower, the better."

    # ── Compare / Benchmark ──
    if any(k in q for k in ["compare", "benchmark", "vs", "versus", "relative"]):
        if ann_ret and bench:
            return (f"Comparing **{asset}** against **{bench}** over {horizon}:\n\n"
                    f"- **{asset}** returned {ann_ret} annualized\n"
                    f"- Volatility: {vol or 'N/A'}\n\n"
                    f"If the asset consistently outperforms the benchmark on a risk-adjusted basis, "
                    f"it suggests genuine alpha generation rather than just market beta.")
        return f"To compare assets, make sure both an asset and benchmark are selected on the Equity Intelligence page."

    # ── Chart / Trend ──
    if any(k in q for k in ["chart", "graph", "trend", "moving average", "sma"]):
        return (f"The chart shows **{asset}**'s price history over {horizon}. "
                f"The moving average overlays help identify trends:\n\n"
                f"- **50-day SMA**: Short-term momentum. When price crosses above it, that's often bullish.\n"
                f"- **200-day SMA**: Long-term trend. A 'golden cross' (50d crossing above 200d) is a classic buy signal.\n\n"
                f"These are simple technical indicators — they work best as confirmation tools, not standalone signals.")

    # ── Diversification ──
    if any(k in q for k in ["diversif", "concentrate", "spread", "allocat"]):
        return ("Diversification reduces risk by combining assets that don't move in lockstep. "
                "Head to the **Portfolio Builder** to:\n\n"
                "1. Select 3-5 assets across different sectors\n"
                "2. Use **Max Sharpe** to find the best risk-return balance\n"
                "3. Use **Min Volatility** to minimize overall portfolio risk\n\n"
                "The correlation heatmap (in Detailed mode) shows you which assets move together.")

    # ── Explain page / dashboard ──
    if any(k in q for k in ["explain", "page", "dashboard", "what am i looking", "overview", "summary"]):
        parts = [f"You're currently analyzing **{asset}**"]
        if ann_ret: parts.append(f"with an annualized return of **{ann_ret}**")
        if sharpe and sharpe != 'N/A': parts.append(f"a Sharpe ratio of **{sharpe}**")
        if max_dd and max_dd != 'N/A': parts.append(f"and a max drawdown of **{max_dd}**")
        summary = ", ".join(parts) + "."
        return summary + "\n\nThe metrics above measure historical performance. Use them to understand risk-return tradeoffs, not to predict the future."

    # ── Strategy / Backtest ──
    if any(k in q for k in ["strategy", "backtest", "moving average", "crossover", "algorithm"]):
        return (f"The strategy backtest compares a **moving average crossover** system against passive buy-and-hold.\n\n"
                f"How it works: when the fast MA crosses above the slow MA, the algorithm buys. When it crosses below, it sells.\n\n"
                f"Key question to ask: did the strategy generate better **risk-adjusted** returns? "
                f"A strategy that returns slightly less but avoids major drawdowns can be more valuable than one that simply rides the market.")

    # ── Portfolio ──
    if any(k in q for k in ["portfolio", "optimize", "weight", "efficient frontier"]):
        return ("The Portfolio Builder lets you construct multi-asset allocations and optimize them using Modern Portfolio Theory.\n\n"
                "- **Max Sharpe**: Finds the weights that maximize return per unit of risk\n"
                "- **Min Volatility**: Finds the least risky combination\n\n"
                "The efficient frontier chart shows all possible portfolios — the star marks your optimal one.")

    # ── Greeting ──
    if any(k in q for k in ["hello", "hi", "hey", "help"]):
        return (f"Hey! I'm **Fin**, your AI analyst. I can see you're looking at **{asset}**.\n\n"
                f"Try asking me things like:\n"
                f"- \"Is my Sharpe ratio good?\"\n"
                f"- \"What does the drawdown mean?\"\n"
                f"- \"How do I diversify?\"\n"
                f"- \"Explain this chart\"")

    # ── Fallback ──
    return (f"I'm currently tracking **{asset}** with {ann_ret or 'N/A'} return and {max_dd or 'N/A'} drawdown.\n\n"
            f"Try asking me to explain a specific metric (Sharpe, drawdown, volatility), compare against the benchmark, or suggest portfolio improvements.")
