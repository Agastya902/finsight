import plotly.graph_objects as go
import plotly.express as px

# FinSight Theme Colors
COLORS = {
    "primary": "#1E88E5",      # Blue
    "secondary": "#43A047",    # Green
    "benchmark": "#757575",    # Grey
    "danger": "#E53935",       # Red
    "warning": "#FB8C00",      # Orange
    "background": "rgba(0,0,0,0)",
    "text": "#E0E0E0",
}

def apply_default_layout(fig: go.Figure, title: str = "") -> go.Figure:
    """Applies a clean, modern, and professional layout to Plotly figures."""
    fig.update_layout(
        title=title,
        title_x=0.0,  # Left align title
        font=dict(family="Inter, sans-serif", size=13),
        margin=dict(l=40, r=20, t=50, b=40),
        plot_bgcolor=COLORS["background"],
        paper_bgcolor=COLORS["background"],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified"
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128, 128, 128, 0.2)",
        zeroline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128, 128, 128, 0.2)",
        zeroline=True,
        zerolinecolor="rgba(128, 128, 128, 0.5)",
        zerolinewidth=1
    )
    
    return fig

def plot_timeseries(data, column, title, color="primary"):
    """Helper to create a simple aesthetic timeseries line chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[column],
        mode='lines',
        name=column,
        line=dict(color=COLORS.get(color, COLORS["primary"]), width=2)
    ))
    return apply_default_layout(fig, title)
