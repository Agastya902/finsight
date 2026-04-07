import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

COLORS = {
    "background": "#0A0E17",
    "panel": "#111827",
    "border": "#1F2937",
    "primary": "#3B82F6",
    "secondary": "#C5A572",
    "success": "#10B981",
    "danger": "#EF4444",
    "text": "#F9FAFB",
    "muted_text": "#9CA3AF"
}

def inject_premium_css():
    """Injects the complete FinSight product shell CSS."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0A0E17 !important;
        color: #F9FAFB !important;
        letter-spacing: -0.01em;
    }
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px;
    }

    /* ── Fixed App Shell (Sidebar) ── */
    section[data-testid="stSidebar"] {
        background-color: #0A0E17 !important;
        border-right: 1px solid #1F2937 !important;
        min-width: 260px !important;
        max-width: 260px !important;
        width: 260px !important;
    }
    /* Hide the collapse button so it never looks collapsible */
    button[data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* ── Navigation: Hide only the radio dot, keep labels visible ── */
    [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 2px !important;
    }
    /* Hide only the small circular radio input dot */
    [data-testid="stSidebar"] [role="radiogroup"] input[type="radio"] {
        display: none !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] [data-testid="stMarkdown"] {
        /* keep labels visible */
    }
    /* Style each radio option as a full-width nav item */
    [data-testid="stSidebar"] [role="radiogroup"] label {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        padding: 11px 16px !important;
        margin: 1px 0 !important;
        border-radius: 6px;
        cursor: pointer;
        color: #9CA3AF;
        font-size: 0.88rem;
        font-weight: 400;
        transition: background-color 0.15s ease, color 0.15s ease;
        border-left: 2px solid transparent;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background-color: rgba(255,255,255,0.04);
        color: #E5E7EB;
    }
    /* Active nav item */
    [data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] label {
        background-color: rgba(59, 130, 246, 0.08) !important;
        color: #3B82F6 !important;
        font-weight: 500 !important;
        border-left: 2px solid #3B82F6 !important;
        border-radius: 0 6px 6px 0;
    }
    /* Clean up baseweb radio wrapper */
    [data-testid="stSidebar"] [data-baseweb="radio"] {
        margin-bottom: 0 !important;
        background: transparent !important;
    }

    /* ── Metric Cards ── */
    .metric-card {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 6px;
        padding: 18px 20px;
        margin-bottom: 14px;
    }
    .metric-card:hover {
        border-color: #374151;
    }
    .metric-title {
        font-size: 0.7rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 500;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 600;
        color: #F9FAFB;
    }

    /* ── Insight Callout ── */
    .insight-box {
        background-color: rgba(17, 24, 39, 0.6);
        border: 1px solid #1F2937;
        border-left: 3px solid #3B82F6;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 0.9rem;
        color: #D1D5DB;
        line-height: 1.55;
        border-radius: 4px;
    }
    .insight-label {
        color: #6B7280;
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    /* ── Hero ── */
    .hero-container {
        padding: 12px 0 28px 0;
        border-bottom: 1px solid #1F2937;
        margin-bottom: 28px;
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #F9FAFB;
        margin-bottom: 8px;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #9CA3AF;
        font-weight: 400;
        line-height: 1.5;
        max-width: 720px;
    }

    /* ── Typography ── */
    h1, h2, h3, h4 {
        font-family: 'Inter', -apple-system, sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: -0.01em !important;
    }

    /* ── Buttons ── */
    .stDownloadButton button, .stButton > button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        border: 1px solid #374151 !important;
        background-color: #111827 !important;
        color: #D1D5DB !important;
        transition: all 0.15s ease;
    }
    .stDownloadButton button:hover, .stButton > button:hover {
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
    }

    /* ── Data Editor ── */
    [data-testid="stDataFrame"] {
        border-radius: 6px !important;
        border: 1px solid #1F2937 !important;
    }

    /* ── Selectbox / Input Overrides ── */
    [data-baseweb="select"] > div {
        background-color: #111827 !important;
        border-color: #1F2937 !important;
    }

    /* ── Floating Copilot Button ── */
    @keyframes copilot-pulse {
        0%   { box-shadow: 0 2px 12px rgba(0,0,0,0.4), 0 0 0 0 rgba(59,130,246,0.35); }
        70%  { box-shadow: 0 2px 12px rgba(0,0,0,0.4), 0 0 0 8px rgba(59,130,246,0); }
        100% { box-shadow: 0 2px 12px rgba(0,0,0,0.4), 0 0 0 0 rgba(59,130,246,0); }
    }
    [data-testid="stPopover"] {
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 999999 !important;
    }
    [data-testid="stPopover"] > button {
        background-color: #3B82F6 !important;
        color: #FFF !important;
        border-radius: 50% !important;
        width: 54px !important;
        height: 54px !important;
        min-height: 54px !important;
        border: none !important;
        animation: copilot-pulse 2.5s infinite;
        transition: transform 0.15s ease, background-color 0.15s ease !important;
        padding: 0 !important;
    }
    [data-testid="stPopover"] > button:hover {
        transform: scale(1.08) !important;
        background-color: #2563EB !important;
    }
    [data-testid="stPopover"] > button p {
        font-size: 1.3rem;
        margin: 0;
        line-height: 1;
    }

    /* ── Copilot Panel ── */
    [data-testid="stPopoverBody"] {
        background-color: #0F1219 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 10px;
        box-shadow: 0 12px 40px -8px rgba(0,0,0,0.6);
    }
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 8px 0 !important;
        border: none !important;
        box-shadow: none !important;
    }
    [data-testid="chatAvatarIcon-user"] {
        background-color: #3B82F6 !important;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #1F2937 !important;
    }

    /* ── Divider ── */
    hr {
        border-top: 1px solid #1F2937 !important;
        margin: 1.2rem 0;
    }

    /* ── Scrolling Ticker Tape ── */
    @keyframes ticker-scroll {
        0%   { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .ticker-tape-wrap {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 99999;
        height: 32px;
        background: rgba(10, 14, 23, 0.85);
        border-bottom: 1px solid #1F2937;
        overflow: hidden;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    .ticker-tape-track {
        display: flex;
        align-items: center;
        height: 100%;
        white-space: nowrap;
        animation: ticker-scroll 45s linear infinite;
        will-change: transform;
    }
    .ticker-tape-track:hover {
        animation-play-state: paused;
    }
    .ticker-item {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 20px;
        font-size: 0.7rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.02em;
    }
    .ticker-item .tk-sym {
        color: #6B7280;
        font-weight: 500;
    }
    .ticker-item .tk-price {
        color: #9CA3AF;
        font-weight: 400;
    }
    .ticker-item .tk-chg-up {
        color: #10B981;
        font-weight: 500;
    }
    .ticker-item .tk-chg-dn {
        color: #EF4444;
        font-weight: 500;
    }
    .ticker-sep {
        color: #1F2937;
        padding: 0 4px;
        font-size: 0.5rem;
    }
    /* Push page content below the fixed tape */
    .block-container {
        padding-top: 2.8rem !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_ticker_tape(tape_data: dict):
    """Renders a scrolling stock-exchange-style ticker tape fixed at the top of the viewport.
    tape_data: dict of {ticker_symbol: (latest_price, change_pct)}
    """
    if not tape_data:
        return

    items_html = ""
    for sym, (price, chg) in tape_data.items():
        arrow = "▲" if chg >= 0 else "▼"
        chg_class = "tk-chg-up" if chg >= 0 else "tk-chg-dn"
        items_html += f'<span class="ticker-item"><span class="tk-sym">{sym}</span><span class="tk-price">${price:,.2f}</span><span class="{chg_class}">{arrow}{abs(chg):.2f}%</span></span><span class="ticker-sep">·</span>'

    # Duplicate the strip so the loop is seamless
    full_html = f"""
    <div class="ticker-tape-wrap">
        <div class="ticker-tape-track">
            {items_html}
            {items_html}
        </div>
    </div>
    """
    st.markdown(full_html, unsafe_allow_html=True)

# ── Reusable UI Components ──

def render_metric_card(title: str, value: str, subtext: str = None):
    sub_html = f"<div style='font-size:0.75rem;color:#6B7280;margin-top:6px'>{subtext}</div>" if subtext else ""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)

def render_insight_box(content: str):
    st.markdown(f"""
        <div class="insight-box">
            <div class="insight-label">Analyst Note</div>
            {content}
        </div>
    """, unsafe_allow_html=True)

# ── Plotly Layouts ──

def apply_default_layout(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(family="Inter, sans-serif", size=14, color="#F9FAFB")),
        title_x=0.01, title_y=0.97,
        font=dict(family="Inter, sans-serif", size=11, color="#9CA3AF"),
        margin=dict(l=16, r=16, t=42, b=16),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#111827", font_size=11, font_family="Inter", bordercolor="#1F2937")
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#1F2937", zeroline=False, showline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#1F2937", zeroline=True, zerolinecolor="#1F2937", zerolinewidth=1, showline=False)
    return fig

def plot_timeseries(data, column, title, color="#3B82F6"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index, y=data[column], mode='lines', name=column,
        line=dict(color=color, width=1.5),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.02,)}" if color.startswith('#') else None
    ))
    return apply_default_layout(fig, title)

def plot_efficient_frontier(frontier_data: dict, opt_vol: float, opt_ret: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=frontier_data['volatility'], y=frontier_data['returns'], mode='markers',
        marker=dict(color=frontier_data['sharpe'], colorscale='Tealgrn', showscale=True, size=4, opacity=0.35, colorbar=dict(title='Sharpe', len=0.6)),
        name='Simulated', hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=[opt_vol], y=[opt_ret], mode='markers',
        marker=dict(color='#C5A572', size=12, symbol='star'),
        name='Optimal'
    ))
    fig = apply_default_layout(fig, "Efficient Frontier")
    fig.update_layout(hovermode='closest')
    fig.update_xaxes(title="Volatility")
    fig.update_yaxes(title="Expected Return")
    return fig

def plot_correlation_heatmap(prices) -> go.Figure:
    corr = prices.pct_change().dropna().corr()
    fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="Tealgrn", origin="lower")
    fig = apply_default_layout(fig, "Correlation Matrix")
    fig.update_layout(coloraxis_showscale=False)
    return fig

def plot_risk_gauge(max_dd: float) -> go.Figure:
    dd_val = abs(max_dd) * 100
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=dd_val,
        number={"suffix": "%", "font": {"color": "#F9FAFB", "size": 28}},
        title={'text': "Max Drawdown", 'font': {'size': 12, "color": "#6B7280"}},
        gauge={
            'axis': {'range': [0, 50], 'tickwidth': 1, 'tickcolor': "#1F2937"},
            'bar': {'color': "#3B82F6"},
            'bgcolor': "rgba(0,0,0,0)", 'borderwidth': 0,
            'steps': [
                {'range': [0, 15], 'color': "rgba(16,185,129,0.08)"},
                {'range': [15, 30], 'color': "rgba(197,165,114,0.08)"},
                {'range': [30, 100], 'color': "rgba(239,68,68,0.08)"}],
        }
    ))
    fig.update_layout(font=dict(family="Inter"), margin=dict(l=16, r=16, t=24, b=12), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=220)
    return fig
