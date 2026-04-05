import re

def generate_response(query: str, current_state: dict) -> str:
    """
    Parses a user query and returns a clean, direct, SaaS product assistant response.
    Relies on heuristics mapped against the active Streamlit session state.
    """
    q = query.lower().strip()
    
    asset = current_state.get('asset', 'the selected asset')
    bench = current_state.get('benchmark', 'the benchmark')
    horizon = current_state.get('horizon', 'the selected timeline')
    sharpe = current_state.get('sharpe', 'the Sharpe ratio')
    ann_ret = current_state.get('ann_ret', 'the calculated return')
    max_dd = current_state.get('max_dd', 'the maximum drawdown')

    if any(k in q for k in ["explain my sharpe", "what is sharpe", "sharpe ratio"]):
        return f"**Sharpe Ratio Breakdown:** Your current configuration yields a Sharpe of **{sharpe}**. This metric evaluates your return per unit of risk. A ratio above 1.0 means you are adequately compensated for the volatility you incur, while a ratio below 1.0 suggests the risk might outweigh the historical rewards."

    if any(k in q for k in ["why is my portfolio risky", "risk", "risky", "drawdown"]):
        return f"**Risk Assessment:** The current setup indicates a maximum historical loss (drawdown) of **{max_dd}**. High drawdowns typically occur when assets move highly correlated during macroeconomic stress. To reduce this, consider allocating capital to historically non-correlated assets via the Builder tab."

    if "compare" in q and "vs" in q:
        return f"**Asset Comparison:** When comparing {asset} directly against {bench} over {horizon}, the goal is to isolate relative performance ('alpha'). If the asset's cumulative trajectory consistently outperforms the benchmark's baseline trend, it suggests strong fundamental execution."

    if any(k in q for k in ["explain this chart", "chart", "graph"]):
        return f"**Chart Analysis:** The current timeseries tracks absolute pricing behavior over {horizon}. The moving average overlays (like the 50-day and 200-day SMAs) help strip away daily noise to reveal the longer-term structural trend. Crossovers between these averages often act as basic entry/exit momentum signals."

    if any(k in q for k in ["diversification", "diversify"]):
        return "**Diversification Strategy:** True diversification means mapping assets that don't fall at the same time. Access the Portfolio Builder natively, mix cross-sector assets (e.g. Technology + Utilities + Consumer Staples), and click 'Execute' to let the optimizer construct an efficient frontier allocation based on minimizing overlapping risk."

    if any(k in q for k in ["build diversified", "diversified portfolio"]):
        return "To build a diversified allocation, navigate to the **Portfolio Builder** tab. Input 3-5 distinct sector leaders, then use the 'Max Sharpe' or 'Min Volatility' algorithms to calculate the exact optimal capital weights without having to guess manually."

    if any(k in q for k in ["explain this dashboard", "explain dashboard", "page"]):
        return f"**Page Overview:** This dashboard calculates the underlying risk/reward paradigm for {asset} against {bench}. It outputs trailing compound yields (**{ann_ret}**), adjusts that yield for volatility (**{sharpe} Sharpe**), and displays exactly how far the capital could drop at its worst (**{max_dd} Drawdown**)."

    if "hello" in q or "hi" in q:
        return f"Hi! I'm FinSight Copilot. I'm currently tracking the state for {asset}. How can I help you analyze the data today?"

    return "I am currently focused on core analytics (Sharpe, Returns, Volatility, optimization arrays). For best results, select an asset in the dashboard and ask me to evaluate its drawdown, benchmark variance, or chart logic."
