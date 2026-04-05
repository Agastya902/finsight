import re

def generate_response(query: str, current_state: dict) -> str:
    """
    Parses a user query and returns a highly institutional, context-aware artificial intelligence response.
    Relies on heuristics mapped against the active Streamlit session state rather than external API limits.
    """
    q = query.lower().strip()
    
    # State bindings
    asset = current_state.get('asset', 'the designated asset')
    bench = current_state.get('benchmark', 'the market benchmark')
    horizon = current_state.get('horizon', 'the selected temporal timeline')
    sharpe = current_state.get('sharpe', 'the computed Sharpe coefficient')
    ann_ret = current_state.get('ann_ret', 'the calculated yield')
    vol = current_state.get('vol', 'the asset volatility')
    max_dd = current_state.get('max_dd', 'the maximum drawdown')

    # Core Explanations
    if any(k in q for k in ["explain my sharpe", "what is sharpe", "sharpe ratio"]):
        return f"**Sharpe Ratio Profile:** Your current configuration yields a Sharpe of **{sharpe}**. The Sharpe ratio mathematically penalizes returns for excess volatility. A ratio above 1.0 generally signifies institutional-alpha generation via superior risk-adjusted yields, whereas sub-1.0 suggests the returns do not adequately compensate for the embedded volatility exposure tracking {horizon}."

    if any(k in q for k in ["why is my portfolio risky", "risk", "risky", "drawdown"]):
        return f"**Systematic Risk Topology:** The current architecture reveals an annualized volatility of **{vol}** alongside a maximum trough depth of **{max_dd}**. High volatility typically originates from either idiosyncratic single-stock exposure or broader macroeconomic beta factors. To mitigate this {max_dd} drawdown impact, institutional managers implement severe diversification or non-correlated hedging layers."

    if "compare" in q and "vs" in q:
        return f"**Comparative Alpha Generation:** In evaluating {asset} against {bench} strictly across {horizon}, the divergence in cumulative returns and correlation matrices dictates relative performance. Typically, assets consistently bridging the gap above their normalized benchmark line indicate superior fundamental execution or strong sector tailwinds."

    if any(k in q for k in ["explain this chart", "chart", "graph"]):
        return f"**Visual Telemetry Analysis:** The displayed metric topologies indicate performance clustering across {horizon}. Downward deviations signify transient capital depreciation, whereas the smoothing moving averages (SMAs) isolate the noise to reveal macroeconomic trajectories. Toggling these SMAs provides rigorous trendline boundaries for entry and exit protocols."

    if any(k in q for k in ["diversification", "diversify"]):
        return "**Capital Allocation Strategy:** Institutional scaling requires minimizing inter-asset correlation. To augment the resilience of your current construct, transition to the Portfolio Builder tab, inject non-correlated macro components (such as utility identifiers or government treasury proxies), and execute an optimization constraint to solve for Maximum Sharpe on the frontier."

    if any(k in q for k in ["build diversified", "diversified portfolio"]):
        return "Navigate to the **Portfolio Builder** tab. Input an array of distinct sector leaders (e.g., AAPL for Tech, JNJ for Healthcare, XOM for Energy). Execute the 'Maximum Sharpe' mathematical priority to effortlessly synthesize a robustly diversified exposure matrix."

    if "hello" in q or "hi" in q:
        return "Greetings. I am FinSight AI, your institutional quantitative copilot. I am actively tracking your configurations across {asset} boundaries. How may I assist your analysis?"

    # Fallback response
    return "Analyst Request Acknowledged. While your specific parameter falls outside my immediate heuristic boundary, I advise cross-referencing your query with our core quantitative metrics: Evaluate your Sharpe Ratio for risk-adjusted performance or transition to the Optimization tab to simulate the Markowitz efficient baseline natively."
