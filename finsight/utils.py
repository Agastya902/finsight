import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Institutional FinSight Premium Colors (Sophisticated, Non-Flashy)
COLORS = {
    "background": "#0A0E17",      # Deep institutional navy/black
    "panel": "#111827",           # Clean dark slate for cards
    "border": "#1F2937",          # Very subtle border
    "primary": "#3B82F6",         # Trustworthy institutional blue
    "secondary": "#C5A572",       # Muted wealth management gold
    "success": "#10B981",         # Clear, non-neon emerald
    "danger": "#EF4444",          # Clear, non-neon red
    "text": "#F9FAFB",            # Bright crisp white
    "muted_text": "#9CA3AF"       # Professional slate grey
}

def inject_premium_css():
    """Injects sophisticated, heavily refined CSS for a credible SaaS aesthetic."""
    css = """
    <style>
    /* Global Typography & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', -apple-system, sans-serif !important;
        background-color: #0A0E17 !important;
        color: #F9FAFB !important;
        letter-spacing: -0.01em;
    }
    
    /* Clean up main padding */
    .block-container {
        padding-top: 1.5rem !important;
        max-width: 1400px;
    }
    
    /* Refined Metric Cards (No flashy neon, just elegant elevation) */
    .metric-card {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 6px;
        padding: 20px;
        transition: transform 0.15s ease-in-out, border-color 0.15s ease-in-out;
        margin-bottom: 1.5rem;
    }
    .metric-card:hover {
        border-color: #374151;
        transform: translateY(-1px);
    }
    .metric-title {
        font-size: 0.75rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 600;
        color: #F9FAFB;
        margin-bottom: 0px;
    }
    
    /* Elegant Insight / Callout Boxes */
    .insight-box {
        background-color: rgba(17, 24, 39, 0.5);
        border: 1px solid #1F2937;
        border-left: 3px solid #3B82F6;
        padding: 18px 24px;
        margin: 16px 0;
        font-size: 0.95rem;
        color: #D1D5DB;
        line-height: 1.5;
        border-radius: 4px;
    }
    .insight-label {
        color: #3B82F6;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    
    /* Sophisticated Hero Section */
    .hero-container {
        text-align: left;
        padding: 24px 0px 32px 0px;
        border-bottom: 1px solid #1F2937;
        margin-bottom: 30px;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 600;
        color: #F9FAFB;
        margin-bottom: 12px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #9CA3AF;
        font-weight: 400;
        line-height: 1.5;
        max-width: 800px;
    }
    
    /* ------------------------------------- */
    /* SIDEBAR NAVIGATION REDESIGN           */
    /* ------------------------------------- */
    section[data-testid="stSidebar"] {
        background-color: #0A0E17 !important;
        border-right: 1px solid #1F2937 !important;
        padding-top: 1rem !important;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Ruthlessly destroy Streamlit Radio Buttons to format as generic buttons */
    /* Hide the actual radio circle entirely */
    [data-testid="stSidebar"] [role="radiogroup"] div[role="radio"] {
        display: none !important;
    }
    /* Expand label blocks to look like proper sidebar menu items */
    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding: 12px 16px;
        margin-bottom: 4px;
        background-color: transparent;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: block;
        width: 100%;
        color: #9CA3AF;
    }
    /* Subtle hover effect */
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.03);
        color: #F9FAFB;
    }
    /* Active Link state wrapper */
    [data-testid="stSidebar"] [data-baseweb="radio"] {
        margin-bottom: 0px !important;
        background: transparent !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] label {
        background-color: rgba(59, 130, 246, 0.1) !important;
        color: #3B82F6 !important;
        border-left: 2px solid #3B82F6 !important;
        font-weight: 500 !important;
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
    }
    
    /* Elegant headings */
    h1, h2, h3, h4 {
        font-family: 'Inter', -apple-system, sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: -0.01em !important;
    }
    
    /* Button Overrides */
    .stDownloadButton button, .stButton button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        border: 1px solid #374151 !important;
        background-color: #111827 !important;
        color: #E5E7EB !important;
        transition: all 0.2s ease;
    }
    .stDownloadButton button:hover, .stButton button:hover {
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 6px !important;
        border: 1px solid #1F2937 !important;
    }
    
    /* ------------------------------------- */
    /* FIN-SIGHT AI FLOATING WIDGET CSS      */
    /* ------------------------------------- */
    @keyframes pulse-shadow {
        0% { box-shadow: 0 4px 15px rgba(0,0,0,0.5), 0 0 0 0 rgba(59, 130, 246, 0.4); }
        70% { box-shadow: 0 4px 15px rgba(0,0,0,0.5), 0 0 0 10px rgba(59, 130, 246, 0); }
        100% { box-shadow: 0 4px 15px rgba(0,0,0,0.5), 0 0 0 0 rgba(59, 130, 246, 0); }
    }
    [data-testid="stPopover"] {
        position: fixed !important;
        bottom: 30px !important;
        right: 30px !important;
        z-index: 999999 !important;
    }
    [data-testid="stPopover"] > button {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        transition: transform 0.2s ease !important;
        animation: pulse-shadow 2.5s infinite;
    }
    [data-testid="stPopover"] > button:hover {
        transform: scale(1.05) !important;
        background-color: #2563EB !important;
    }
    [data-testid="stPopover"] > button p {
        font-size: 1.5rem;
        margin: 0;
        padding: 0;
    }
    
    /* Inside the chat bubble popover body - lock background */
    [data-testid="stPopoverBody"] {
        background-color: #0A0E17 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    
    /* Chat Message bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 10px 0 !important;
        border: none !important;
    }
    [data-testid="chatAvatarIcon-user"] {
        background-color: #3B82F6 !important;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #1F2937 !important;
    }
    
    /* Quick Prompts standard buttons */
    .stButton button[kind="secondary"] {
        border-radius: 20px !important;
        border: 1px solid #374151 !important;
        color: #9CA3AF !important;
        background-color: transparent !important;
        padding: 4px 12px !important;
        font-size: 0.8rem !important;
    }
    .stButton button[kind="secondary"]:hover {
        color: #3B82F6 !important;
        border-color: #3B82F6 !important;
        background-color: rgba(59, 130, 246, 0.05) !important;
    }

    hr {
        border-top: 1px solid #1F2937 !important;
        margin: 1.5rem 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtext: str = None):
    """Utility to render a highly polished HTML metric card."""
    sub_html = f"<div style='font-size: 0.8rem; color: #9CA3AF; margin-top: 8px;'>{subtext}</div>" if subtext else ""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)

def render_insight_box(content: str):
    """Utility to render a premium institutional client-facing insight box."""
    st.markdown(f"""
        <div class="insight-box">
            <div class="insight-label">Analyst Commentary / Note</div>
            {content}
        </div>
    """, unsafe_allow_html=True)

def apply_default_layout(fig: go.Figure, title: str = "") -> go.Figure:
    """Applies a sophisticated, minimalist layout to Plotly figures."""
    fig.update_layout(
        title=dict(text=title, font=dict(family="Inter, sans-serif", size=16, color="#F9FAFB")),
        title_x=0.01,
        title_y=0.95,
        font=dict(family="Inter, sans-serif", size=12, color="#9CA3AF"),
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11)
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#111827",
            font_size=12,
            font_family="Inter",
            bordercolor="#1F2937"
        )
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#1F2937",
        zeroline=False,
        showline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#1F2937",
        zeroline=True,
        zerolinecolor="#1F2937",
        zerolinewidth=1,
        showline=False
    )
    
    return fig

def plot_timeseries(data, column, title, color="#3B82F6"):
    """Helper to create an elegant timeseries line chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[column],
        mode='lines',
        name=column,
        line=dict(color=color, width=1.5),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.02,)}" if color.startswith('#') else None
    ))
    return apply_default_layout(fig, title)

def plot_efficient_frontier(frontier_data: dict, opt_vol: float, opt_ret: float) -> go.Figure:
    """Renders an institutional efficient frontier scatter plot."""
    fig = go.Figure()
    
    # 5000 randomized portfolios
    fig.add_trace(go.Scatter(
        x=frontier_data['volatility'], 
        y=frontier_data['returns'], 
        mode='markers',
        marker=dict(
            color=frontier_data['sharpe'],
            colorscale='Tealgrn',
            showscale=True,
            size=5,
            opacity=0.4,
            colorbar=dict(title='Sharpe')
        ),
        name='Simulated Portfolios',
        hoverinfo='skip'
    ))
    
    # The optimal portfolio
    fig.add_trace(go.Scatter(
        x=[opt_vol], 
        y=[opt_ret], 
        mode='markers',
        marker=dict(color='#C5A572', size=14, symbol='star'),
        name='Optimized Target'
    ))
    
    fig = apply_default_layout(fig, "Markowitz Efficient Frontier Array")
    fig.update_layout(hovermode='closest')
    fig.update_xaxes(title="Annualized Volatility (Risk)")
    fig.update_yaxes(title="Expected Annual Return (Yield)")
    return fig

def plot_correlation_heatmap(prices) -> go.Figure:
    """Generates a premium asset correlation matrix heatmap."""
    corr = prices.pct_change().dropna().corr()
    fig = px.imshow(
        corr, 
        text_auto=".2f", 
        aspect="auto",
        color_continuous_scale="Tealgrn",
        origin="lower"
    )
    fig = apply_default_layout(fig, "Asset Correlation Topography")
    fig.update_layout(coloraxis_showscale=False)
    return fig

def plot_risk_gauge(max_dd: float) -> go.Figure:
    """Builds a gauge chart for historical drawdown risk assessment."""
    dd_val = abs(max_dd) * 100
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = dd_val,
        number = {"suffix": "%", "font": {"color": "#F9FAFB"}},
        title = {'text': "Maximum Protocol Risk", 'font': {'size': 14, "color": "#9CA3AF"}},
        gauge = {
            'axis': {'range': [0, 40], 'tickwidth': 1, 'tickcolor': "#1F2937"},
            'bar': {'color': "#3B82F6"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 15], 'color': "rgba(16, 185, 129, 0.1)"},
                {'range': [15, 25], 'color': "rgba(197, 165, 114, 0.1)"},
                {'range': [25, 100], 'color': "rgba(239, 68, 68, 0.1)"}],
        }
    ))
    fig.update_layout(
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=250
    )
    return fig
