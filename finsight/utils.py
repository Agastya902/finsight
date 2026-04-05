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
    css = f"""
    <style>
    /* Global Typography & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"]  {{
        font-family: 'Inter', -apple-system, sans-serif !important;
        background-color: {COLORS['background']} !important;
        color: {COLORS['text']} !important;
        letter-spacing: -0.01em;
    }}
    
    /* Clean up main padding */
    .block-container {{
        padding-top: 2rem !important;
        max-width: 1400px;
    }}
    
    /* Refined Metric Cards (No flashy neon, just elegant elevation) */
    .metric-card {{
        background-color: {COLORS['panel']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
        transition: transform 0.15s ease-in-out, border-color 0.15s ease-in-out;
        margin-bottom: 1.5rem;
    }}
    .metric-card:hover {{
        border-color: #374151;
        transform: translateY(-1px);
    }}
    .metric-title {{
        font-size: 0.8rem;
        color: {COLORS['muted_text']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
        margin-bottom: 8px;
    }}
    .metric-value {{
        font-size: 1.85rem;
        font-weight: 600;
        color: {COLORS['text']};
        margin-bottom: 0px;
    }}
    
    /* Elegant Insight / Callout Boxes */
    .insight-box {{
        background-color: #111827;
        border-left: 3px solid {COLORS['secondary']};
        padding: 20px 24px;
        margin: 24px 0;
        font-size: 1.05rem;
        color: #E5E7EB;
        line-height: 1.6;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }}
    .insight-label {{
        color: {COLORS['secondary']};
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }}
    
    /* Sophisticated Hero Section */
    .hero-container {{
        text-align: left;
        padding: 48px 0px 32px 0px;
        border-bottom: 1px solid {COLORS['border']};
        margin-bottom: 40px;
    }}
    .hero-title {{
        font-size: 2.8rem;
        font-weight: 600;
        color: {COLORS['text']};
        margin-bottom: 16px;
    }}
    .hero-subtitle {{
        font-size: 1.2rem;
        color: {COLORS['muted_text']};
        font-weight: 300;
        line-height: 1.6;
        max-width: 800px;
    }}
    
    /* Streamlit Sidebar Polish */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['panel']} !important;
        border-right: 1px solid {COLORS['border']};
    }}
    [data-testid="stSidebarNav"] {{
        display: none;
    }}
    
    /* Elegant standard headings */
    h1, h2, h3, h4 {{
        font-family: 'Inter', -apple-system, sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: -0.02em !important;
    }}
    
    /* Custom divider */
    hr {{
        border-top: 1px solid {COLORS['border']} !important;
        margin: 2rem 0;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtext: str = None):
    """Utility to render a highly polished HTML metric card."""
    sub_html = f"<div style='font-size: 0.8rem; color: {COLORS['muted_text']}; margin-top: 8px;'>{subtext}</div>" if subtext else ""
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
            <div class="insight-label">Analyst Commentary</div>
            {content}
        </div>
    """, unsafe_allow_html=True)

def apply_default_layout(fig: go.Figure, title: str = "") -> go.Figure:
    """Applies a sophisticated, minimalist layout to Plotly figures."""
    fig.update_layout(
        title=dict(text=title, font=dict(family="Inter, sans-serif", size=16, color=COLORS['text'])),
        title_x=0.01,
        title_y=0.95,
        font=dict(family="Inter, sans-serif", size=12, color=COLORS['muted_text']),
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
            bgcolor=COLORS['panel'],
            font_size=12,
            font_family="Inter",
            bordercolor=COLORS['border']
        )
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS['border'],
        zeroline=False,
        showline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS['border'],
        zeroline=True,
        zerolinecolor=COLORS['border'],
        zerolinewidth=1,
        showline=False
    )
    
    return fig

def plot_timeseries(data, column, title, color="primary"):
    """Helper to create an elegant timeseries line chart."""
    hex_color = COLORS.get(color, color) if color in COLORS else color 
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[column],
        mode='lines',
        name=column,
        line=dict(color=hex_color, width=1.5),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.02,)}" if hex_color.startswith('#') else None
    ))
    return apply_default_layout(fig, title)
