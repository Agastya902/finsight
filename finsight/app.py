import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

import data_loader
import metrics
import explainability
import strategies
import optimizer
import utils
import universe
import ai_copilot # Keep for now if any logic depends on it, but we'll use copilot.py
import copilot
import reporting

# ── Page Config ──
st.set_page_config(page_title="FinSight", page_icon="◆", layout="wide", initial_sidebar_state="collapsed")
utils.inject_premium_css()

# ── Session State ──
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [
        {"role": "assistant", "content": "Hi, I'm Fin! I'm your personal AI analyst. I can explain any metric, analyze trends, or help you build a portfolio."}
    ]
if 'ai_context' not in st.session_state:
    st.session_state['ai_context'] = {}
if 'last_report' not in st.session_state:
    st.session_state['last_report'] = None
if 'show_report_preview' not in st.session_state:
    st.session_state['show_report_preview'] = False
if 'active_page' not in st.session_state:
    st.session_state['active_page'] = "overview"
if 'show_chat' not in st.session_state:
    st.session_state['show_chat'] = False

# ── Time Horizon Helpers ──
def get_horizon_dates(horizon: str):
    end = datetime.today()
    deltas = {"1Y": 1, "3Y": 3, "5Y": 5, "10Y": 10, "Max": 30}
    start = end - relativedelta(years=deltas.get(horizon, 5))
    return start.date(), end.date()

def render_horizon_selector(key):
    h = st.radio("Period", ["1Y", "3Y", "5Y", "10Y", "Max", "Custom"],
                 horizontal=True, key=f"{key}_h", label_visibility="collapsed")
    if h == "Custom":
        c1, c2 = st.columns(2)
        s = c1.date_input("From", value=datetime.today().date() - relativedelta(years=5), key=f"{key}_s")
        e = c2.date_input("To", value=datetime.today().date(), key=f"{key}_e")
        return s, e
    return get_horizon_dates(h)

def csv_download(df, filename, label="Export CSV"):
    st.download_button(label=label, data=df.to_csv(index=True).encode('utf-8'),
                       file_name=filename, mime='text/csv')

# ── Actions ──
def trigger_report_generation(state):
    """Triggers report building and stores in session state."""
    with st.spinner("Compiling institutional report..."):
        artifact = reporting.create_report_artifact(state)
        st.session_state['last_report'] = artifact
        st.session_state['show_report_preview'] = True

def display_report_preview():
    """Renders the in-app report preview and download buttons with error fallbacks."""
    if st.session_state['last_report'] and st.session_state['show_report_preview']:
        artifact = st.session_state['last_report']
        
        st.markdown("<hr>", unsafe_allow_html=True)
        with st.expander("📄 View Research Report Preview", expanded=True):
            # Header actions
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**Institutional Report:** {artifact.filename_base}")
            if c2.button("Close Preview", use_container_width=True):
                st.session_state['show_report_preview'] = False
                st.rerun()

            # Status / Error Messaging
            if artifact.pdf_error:
                st.warning(f"⚠️ PDF generation encountered an issue, but your HTML report is ready. (Error: {artifact.pdf_error[:50]}...)")
            
            # Download buttons
            b1, b2, b3 = st.columns(3)
            b1.download_button("Download HTML", data=artifact.html, file_name=f"{artifact.filename_base}.html", mime="text/html", use_container_width=True)
            
            if not artifact.pdf_error:
                b2.download_button("Download PDF", data=artifact.pdf, file_name=f"{artifact.filename_base}.pdf", mime="application/pdf", use_container_width=True)
            else:
                b2.button("PDF Unavailable", disabled=True, use_container_width=True)
                
            b3.download_button("Download CSV", data=artifact.csv, file_name=f"{artifact.filename_base}.csv", mime="text/csv", use_container_width=True)
            
            st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
            
            # Preview Frame
            st.markdown("<div style='background:white; border-radius:8px; overflow:hidden; border: 1px solid #E5E7EB;'>"
                        f"{artifact.html}"
                        "</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── Top Navigation Rail ──
st.markdown("<div class='top-nav-container'>", unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3 = st.columns([1.8, 5, 1.2])

with nav_col1:
    st.markdown("""
    <div style='display:flex; align-items:center; gap:12px; height:100%;'>
        <div style='width:32px; height:32px; border-radius:8px; background:linear-gradient(135deg, #3B82F6, #2563EB); display:flex; align-items:center; justify-content:center; font-size:1rem; color:#fff; font-weight:800; box-shadow:0 4px 12px rgba(59,130,246,0.3);'>F</div>
        <div>
            <div style='font-size:1.15rem; font-weight:700; color:#F9FAFB; letter-spacing:-0.03em; line-height:1;'>FinSight</div>
            <div style='font-size:0.6rem; color:#6B7280; text-transform:uppercase; letter-spacing:0.05em; margin-top:2px; font-weight:600;'>Institutional Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown('<div class="top-nav-tabs">', unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4)
    pages = [
        ("Platform Overview", "overview"),
        ("Equity Intelligence", "equity"),
        ("Algorithmic Validator", "strategy"),
        ("Portfolio Builder", "portfolio")
    ]
    for i, (label, key) in enumerate(pages):
        is_active = st.session_state.active_page == key
        btn_class = "nav-tab-btn nav-tab-active" if is_active else "nav-tab-btn"
        # We use a bit of a hack to apply the custom class via markdown around the button
        # But for now, we'll just use regular buttons and rely on session state
        if [t1, t2, t3, t4][i].button(label, key=f"nav_{key}", use_container_width=True, type="secondary" if not is_active else "primary"):
            st.session_state.active_page = key
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with nav_col3:
    mode = st.selectbox("mode", ["Summary", "Detailed"], label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)
page_key = st.session_state.active_page
# ══════════════════════════════════════════
# GLOBAL TICKER TAPE (all pages)
# ══════════════════════════════════════════
TAPE_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "JPM", "V", "JNJ", "XOM", "WMT", "DIS", "NFLX", "AMD"]
_tape_end = datetime.today().date()
_tape_start = (datetime.today() - relativedelta(days=10)).date()
_tape_prices = data_loader.fetch_stock_data(TAPE_TICKERS, _tape_start, _tape_end)
_tape_dict = {}
if not _tape_prices.empty:
    for tk in TAPE_TICKERS:
        if tk in _tape_prices.columns:
            col = _tape_prices[tk].dropna()
            if len(col) >= 2:
                _tape_dict[tk] = (col.iloc[-1], ((col.iloc[-1] - col.iloc[-2]) / col.iloc[-2]) * 100)
utils.render_ticker_tape(_tape_dict)

# ══════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════

if page_key == "overview":

    # ── Hero ──
    st.markdown("""
    <div class="hero-container">
        <div style="font-size:0.7rem; color:#3B82F6; text-transform:uppercase; letter-spacing:0.1em; font-weight:600; margin-bottom:10px;">Portfolio Intelligence Platform</div>
        <div class="hero-title">Understand your investments.<br>Make smarter decisions.</div>
        <div class="hero-subtitle">
            Analyze any public equity, backtest trading strategies, optimize multi-asset portfolios,
            and get plain-English explanations — all powered by real market data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sparkline data for feature cards ──
    _spark_tickers = ["AAPL", "MSFT", "GOOGL"]
    _spark_start = (datetime.today() - relativedelta(years=1)).date()
    sparkline_data = data_loader.fetch_stock_data(_spark_tickers, _spark_start, datetime.today().date())

    # ── Quick Start Search ──
    st.markdown("<div style='font-size:0.65rem; color:#4B5563; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:8px;'>Quick Start — Search any asset</div>", unsafe_allow_html=True)
    qs_col1, qs_col2 = st.columns([3, 1])
    with qs_col1:
        quick_asset = st.selectbox("Search", options=list(universe.EQUITY_UNIVERSE.keys()), index=0, label_visibility="collapsed", key="qs_search")
    with qs_col2:
        if st.button("Analyze →", use_container_width=True, key="qs_go"):
            st.session_state['quick_ticker'] = universe.extract_ticker(quick_asset, universe.EQUITY_UNIVERSE)
            st.info(f"Navigate to **Equity Intelligence** in the sidebar to analyze {universe.extract_ticker(quick_asset, universe.EQUITY_UNIVERSE)}.")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Sparkline Feature Cards ──
    st.markdown("<div style='font-size:0.65rem; color:#4B5563; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;'>What You Can Do</div>", unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)

    with fc1:
        st.markdown("""
        <div style="background:#111827; border:1px solid #1F2937; border-radius:8px; padding:20px 20px 12px 20px;">
            <div style="font-size:1.4rem; margin-bottom:8px;">📈</div>
            <div style="font-size:0.95rem; font-weight:600; color:#F9FAFB; margin-bottom:6px;">Equity Intelligence</div>
            <div style="font-size:0.82rem; color:#9CA3AF; line-height:1.45;">
                Analyze returns, volatility, Sharpe ratios, and drawdowns for any public asset — benchmarked against SPY, QQQ, or a custom index.
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Mini sparkline
        if not sparkline_data.empty and "AAPL" in sparkline_data.columns:
            spark_fig = go.Figure()
            spark_series = sparkline_data["AAPL"].dropna()
            spark_color = "#10B981" if spark_series.iloc[-1] >= spark_series.iloc[0] else "#EF4444"
            spark_fig.add_trace(go.Scatter(x=spark_series.index, y=spark_series, mode='lines',
                line=dict(color=spark_color, width=1.5), fill='tozeroy',
                fillcolor=spark_color.replace(")", ",0.05)").replace("rgb", "rgba") if "rgb" in spark_color else f"rgba{tuple(int(spark_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.05,)}",
                hoverinfo='skip'))
            spark_fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=70,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.plotly_chart(spark_fig, use_container_width=True, config={"displayModeBar": False})

    with fc2:
        st.markdown("""
        <div style="background:#111827; border:1px solid #1F2937; border-radius:8px; padding:20px 20px 12px 20px;">
            <div style="font-size:1.4rem; margin-bottom:8px;">⚡</div>
            <div style="font-size:0.95rem; font-weight:600; color:#F9FAFB; margin-bottom:6px;">Strategy Backtesting</div>
            <div style="font-size:0.82rem; color:#9CA3AF; line-height:1.45;">
                Run moving-average crossover strategies against passive buy-and-hold. Compare cumulative returns and maximum drawdown side-by-side.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not sparkline_data.empty and "MSFT" in sparkline_data.columns:
            spark_fig2 = go.Figure()
            s2 = sparkline_data["MSFT"].dropna()
            sc2 = "#10B981" if s2.iloc[-1] >= s2.iloc[0] else "#EF4444"
            spark_fig2.add_trace(go.Scatter(x=s2.index, y=s2, mode='lines',
                line=dict(color=sc2, width=1.5), fill='tozeroy',
                fillcolor=f"rgba{tuple(int(sc2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.05,)}",
                hoverinfo='skip'))
            spark_fig2.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=70,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.plotly_chart(spark_fig2, use_container_width=True, config={"displayModeBar": False})

    with fc3:
        st.markdown("""
        <div style="background:#111827; border:1px solid #1F2937; border-radius:8px; padding:20px 20px 12px 20px;">
            <div style="font-size:1.4rem; margin-bottom:8px;">🔬</div>
            <div style="font-size:0.95rem; font-weight:600; color:#F9FAFB; margin-bottom:6px;">Portfolio Optimization</div>
            <div style="font-size:0.82rem; color:#9CA3AF; line-height:1.45;">
                Build multi-asset portfolios, assign custom weights or auto-optimize via Max Sharpe / Min Volatility, and visualize the efficient frontier.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not sparkline_data.empty and "GOOGL" in sparkline_data.columns:
            spark_fig3 = go.Figure()
            s3 = sparkline_data["GOOGL"].dropna()
            sc3 = "#10B981" if s3.iloc[-1] >= s3.iloc[0] else "#EF4444"
            spark_fig3.add_trace(go.Scatter(x=s3.index, y=s3, mode='lines',
                line=dict(color=sc3, width=1.5), fill='tozeroy',
                fillcolor=f"rgba{tuple(int(sc3.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.05,)}",
                hoverinfo='skip'))
            spark_fig3.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=70,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.plotly_chart(spark_fig3, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── How It Works ──
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.65rem; color:#4B5563; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:16px;'>How It Works</div>", unsafe_allow_html=True)

    hw1, hw2, hw3, hw4 = st.columns(4)
    steps = [
        ("1", "Select an asset", "Choose from 40+ major equities or type any ticker symbol."),
        ("2", "Pick your lens", "Analyze performance, test strategies, or build a portfolio."),
        ("3", "Read the analysis", "Get institutional-grade metrics with plain-English explanations."),
        ("4", "Ask Copilot", "Use the AI assistant to dig deeper into any result on screen."),
    ]
    for col, (num, title, desc) in zip([hw1, hw2, hw3, hw4], steps):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding:12px 8px;">
                <div style="width:36px; height:36px; border-radius:50%; background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.2);
                            display:inline-flex; align-items:center; justify-content:center; font-size:0.85rem; font-weight:600; color:#3B82F6; margin-bottom:10px;">{num}</div>
                <div style="font-size:0.88rem; font-weight:500; color:#F9FAFB; margin-bottom:4px;">{title}</div>
                <div style="font-size:0.78rem; color:#6B7280; line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Platform Stats ──
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    stat_items = [
        ("40+", "Tracked Assets"),
        ("5", "Index Benchmarks"),
        ("2", "Optimization Modes"),
        ("Real-time", "Yahoo Finance Data"),
    ]
    for col, (val, label) in zip([s1, s2, s3, s4], stat_items):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding:16px 0;">
                <div style="font-size:1.5rem; font-weight:700; color:#F9FAFB;">{val}</div>
                <div style="font-size:0.7rem; color:#6B7280; text-transform:uppercase; letter-spacing:0.04em; margin-top:2px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.session_state['ai_context'] = {'page': 'overview', 'asset': 'the platform overview', 'horizon': 'N/A'}


elif page_key == "equity":
    # ── Controls Row ──
    c1, c2, c3 = st.columns([1.4, 1.4, 2.2])
    asset_sel = c1.selectbox("Asset", options=list(universe.EQUITY_UNIVERSE.keys()), index=0)
    ticker = universe.extract_ticker(asset_sel, universe.EQUITY_UNIVERSE)
    if asset_sel == "Custom (Type your own)":
        ticker = c1.text_input("Ticker", value="AAPL").upper().strip()

    bench_sel = c2.selectbox("Benchmark", options=list(universe.BENCHMARK_PRESETS.keys()), index=0)
    benchmark = universe.extract_ticker(bench_sel, universe.BENCHMARK_PRESETS)
    if bench_sel == "Custom (Type your own)":
        benchmark = c2.text_input("Benchmark Ticker", value="SPY").upper().strip()

    with c3:
        start_date, end_date = render_horizon_selector("eq")

    if start_date >= end_date:
        st.error("Invalid date range.")
        st.stop()

    if data_loader.validate_ticker(ticker):
        with st.spinner(f"Loading {ticker}..."):
            fetch_list = [ticker]
            if data_loader.validate_ticker(benchmark):
                fetch_list.append(benchmark)
            data = data_loader.fetch_stock_data(fetch_list, start_date, end_date)

            if not data.empty and ticker in data.columns:
                prices = data[ticker]
                daily_ret = metrics.calculate_daily_returns(prices)
                if len(daily_ret) == 0:
                    st.warning("Not enough trading data for this range.")
                    st.stop()

                ann_ret = metrics.calculate_annualized_return(daily_ret)
                ann_vol = metrics.calculate_annualized_volatility(daily_ret)
                max_dd = metrics.calculate_max_drawdown(prices)
                sharpe = metrics.calculate_sharpe_ratio(daily_ret)
                bench_ret = None
                if benchmark in data.columns:
                    bench_ret = metrics.calculate_annualized_return(metrics.calculate_daily_returns(data[benchmark]))

                # ── Action Toolbar ──
                rep_c1, rep_c2 = st.columns([5, 1])
                with rep_c2:
                    if st.button("Generate Report", use_container_width=True, key="btn_rep_eq"):
                        rep_state = reporting.ReportState(
                            page_type="equity",
                            tickers=[ticker],
                            benchmark=benchmark,
                            start_date=str(start_date),
                            end_date=str(end_date),
                            metrics={
                                "Annualized_Return": f"{ann_ret*100:+.2f}%",
                                "Volatility": f"{ann_vol*100:.2f}%",
                                "Sharpe_Ratio": f"{sharpe:.2f}",
                                "Max_Drawdown": f"{max_dd*100:.2f}%"
                            }
                        )
                        trigger_report_generation(rep_state)
                
                display_report_preview()

                st.session_state['ai_context'] = {
                    'page': 'equity',
                    'asset': ticker, 'benchmark': benchmark,
                    'horizon': 'the selected period',
                    'sharpe': f"{sharpe:.2f}",
                    'ann_ret': f"{ann_ret*100:+.2f}%",
                    'vol': f"{ann_vol*100:.2f}%",
                    'max_dd': f"{max_dd*100:.2f}%"
                }

                # ── KPI Row ──
                k1, k2, k3, k4 = st.columns(4)
                with k1: utils.render_metric_card("Ann. Return", f"{ann_ret*100:+.2f}%")
                with k2: utils.render_metric_card("Volatility", f"{ann_vol*100:.2f}%")
                with k3: utils.render_metric_card("Max Drawdown", f"{max_dd*100:.2f}%")
                with k4: utils.render_metric_card("Sharpe Ratio", f"{sharpe:.2f}")

                utils.render_insight_box(commentary)

                # ── Chart Controls ──
                tc1, tc2, tc3, tc4 = st.columns(4)
                show_price = tc1.checkbox("Price", value=True)
                show_50 = tc2.checkbox("50-day SMA", value=True)
                show_200 = tc3.checkbox("200-day SMA", value=False)
                show_dd = tc4.checkbox("Drawdown", value=False)

                if show_dd:
                    dd = (prices - prices.cummax()) / prices.cummax()
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=dd.index, y=dd*100, name="Drawdown", line=dict(color="#EF4444", width=1.5), fill='tozeroy', fillcolor="rgba(239,68,68,0.08)"))
                    fig = utils.apply_default_layout(fig, "Drawdown")
                    fig.update_yaxes(ticksuffix="%")
                else:
                    fig = go.Figure()
                    if show_price:
                        fig.add_trace(go.Scatter(x=prices.index, y=prices, name="Price", line=dict(color="#3B82F6", width=1.5)))
                    sma50 = prices.rolling(50).mean()
                    sma200 = prices.rolling(200).mean()
                    if show_50:
                        fig.add_trace(go.Scatter(x=sma50.index, y=sma50, name="50d SMA", line=dict(color="#10B981", width=1, dash='dot')))
                    if show_200:
                        fig.add_trace(go.Scatter(x=sma200.index, y=sma200, name="200d SMA", line=dict(color="#C5A572", width=1, dash='dash')))
                    fig = utils.apply_default_layout(fig, f"{ticker} — Price & Moving Averages")

                st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "toImageButtonOptions": {"format": "png", "filename": f"{ticker}_chart"}})

                # ── Detailed mode extras ──
                if mode == "Detailed":
                    fig_hist = px.histogram(daily_ret, nbins=60)
                    fig_hist.update_traces(marker_color="#3B82F6", opacity=0.65)
                    fig_hist = utils.apply_default_layout(fig_hist, "Return Distribution")
                    st.plotly_chart(fig_hist, use_container_width=True, config={"displaylogo": False})
                    csv_download(pd.DataFrame({ticker: prices}), f"{ticker}_data.csv")


elif page_key == "strategy":
    c1, c2 = st.columns([1.5, 2.5])
    asset_sel = c1.selectbox("Asset", options=list(universe.EQUITY_UNIVERSE.keys()), index=0)
    ticker = universe.extract_ticker(asset_sel, universe.EQUITY_UNIVERSE)
    if asset_sel == "Custom (Type your own)":
        ticker = c1.text_input("Ticker", value="AAPL").upper().strip()

    with c2:
        start_date, end_date = render_horizon_selector("st")

    # Strategy params inline, not buried in sidebar
    pc1, pc2 = st.columns(2)
    short_window = pc1.number_input("Fast MA window", min_value=5, max_value=100, value=50)
    long_window = pc2.number_input("Slow MA window", min_value=20, max_value=300, value=200)

    if data_loader.validate_ticker(ticker):
        with st.spinner(f"Backtesting {ticker}..."):
            data = data_loader.fetch_stock_data([ticker], start_date, end_date)
            if not data.empty and ticker in data.columns:
                prices = data[ticker]
                strat_df = strategies.run_moving_average_crossover(prices, short_window, long_window)
                bh_ret = metrics.calculate_daily_returns(prices)
                strat_ret = strat_df['Strategy_Daily_Return'].dropna()

                bh_ann = metrics.calculate_annualized_return(bh_ret)
                bh_dd = metrics.calculate_max_drawdown(prices)
                st_ann = metrics.calculate_annualized_return(strat_ret)
                st_dd = metrics.calculate_max_drawdown(strat_df['Strategy_Cum_Ret'])

                # ── Action Toolbar ──
                rep_c1, rep_c2 = st.columns([5, 1])
                with rep_c2:
                    if st.button("Generate Report", use_container_width=True, key="btn_rep_st"):
                        rep_state = reporting.ReportState(
                            page_type="strategy",
                            tickers=[ticker],
                            start_date=str(start_date),
                            end_date=str(end_date),
                            settings={"Short_Window": short_window, "Long_Window": long_window},
                            metrics={
                                "Strategy_Return": f"{st_ann*100:+.2f}%",
                                "Buy_Hold_Return": f"{bh_ann*100:+.2f}%",
                                "Strategy_Drawdown": f"{st_dd*100:.2f}%",
                                "Buy_Hold_Drawdown": f"{bh_dd*100:.2f}%"
                            },
                            tables={'comparison': pd.DataFrame({
                                'Metric': ['Annual Return', 'Max Drawdown'],
                                'Strategy': [f"{st_ann*100:.2f}%", f"{st_dd*100:.2f}%"],
                                'Buy & Hold': [f"{bh_ann*100:.2f}%", f"{bh_dd*100:.2f}%"]
                            })}
                        )
                        trigger_report_generation(rep_state)
                
                display_report_preview()

                st.session_state['ai_context'] = {
                    'page': 'strategy',
                    'asset': ticker, 'horizon': 'the backtest period',
                    'short': short_window, 'long': long_window,
                    'ann_ret': f"{st_ann*100:+.2f}%",
                    'max_dd': f"{st_dd*100:.2f}%"
                }

                m1, m2 = st.columns(2)
                with m1: utils.render_metric_card("Buy & Hold Return", f"{bh_ann*100:.2f}%", f"Max drawdown: {bh_dd*100:.2f}%")
                with m2: utils.render_metric_card(f"MA {short_window}/{long_window} Return", f"{st_ann*100:.2f}%", f"Max drawdown: {st_dd*100:.2f}%")

                utils.render_insight_box(commentary)

                fig = go.Figure()
                bh_cum = (1 + bh_ret).cumprod()
                fig.add_trace(go.Scatter(x=bh_cum.index, y=bh_cum, name="Buy & Hold", line=dict(color="#6B7280", width=1.5, dash="dash")))
                fig.add_trace(go.Scatter(x=strat_df.index, y=strat_df['Strategy_Cum_Ret'], name="Strategy", line=dict(color="#3B82F6", width=2)))
                fig = utils.apply_default_layout(fig, "Cumulative Returns — Strategy vs Buy & Hold")
                st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

                if mode == "Detailed":
                    csv_download(strat_df, f"{ticker}_backtest.csv", "Export Backtest")


elif page_key == "portfolio":
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("<p style='font-size:0.75rem;color:#6B7280;text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px'>Select Assets</p>", unsafe_allow_html=True)
        defaults = ["Apple Inc. (AAPL)", "Microsoft Corp. (MSFT)", "Alphabet Inc. Class A (GOOGL)", "Amazon.com Inc. (AMZN)"]
        asset_sels = st.multiselect("assets", options=list(universe.EQUITY_UNIVERSE.keys()),
                                     default=defaults, label_visibility="collapsed")
        tickers = [universe.extract_ticker(x, universe.EQUITY_UNIVERSE) for x in asset_sels]
        if "Custom (Type your own)" in asset_sels:
            custom = st.text_input("Custom tickers (comma-separated)")
            if custom:
                tickers.extend([x.strip().upper() for x in custom.split(",")])
                if "CUSTOM" in tickers: tickers.remove("CUSTOM")
    with c2:
        start_date, end_date = render_horizon_selector("pf")

    if len(tickers) < 2:
        st.warning("Select at least 2 assets to build a portfolio.")
        st.stop()

    data = data_loader.fetch_stock_data(tickers, start_date, end_date)
    if data.empty:
        st.error("Could not load data for the selected assets.")
        st.stop()

    valid = [t for t in tickers if t in data.columns]
    prices = data[valid]

    # ── Weight Builder ──
    wb, wa = st.columns([2, 1])
    with wb:
        init_w = [round(1.0/len(valid), 3)] * len(valid)
        df_w = pd.DataFrame({"Asset": valid, "Weight": init_w})
        edited = st.data_editor(df_w,
            column_config={"Weight": st.column_config.NumberColumn("Weight", min_value=0.0, max_value=1.0, step=0.01, format="%.3f")},
            hide_index=True, use_container_width=True)
    with wa:
        st.markdown("<p style='font-size:0.7rem;color:#6B7280;text-transform:uppercase;letter-spacing:0.04em;margin-bottom:6px'>Optimizer</p>", unsafe_allow_html=True)
        objective = st.selectbox("Objective", ["Max Sharpe", "Min Volatility"], label_visibility="collapsed")
        do_opt = st.button("Optimize", use_container_width=True)
        total_w = edited["Weight"].sum()
        if abs(total_w - 1.0) > 0.01 and not do_opt:
            st.caption(f"⚠ Weights sum to {total_w:.2f} — should be 1.0")

    st.markdown("<hr>", unsafe_allow_html=True)

    with st.spinner("Computing..."):
        if do_opt:
            res = optimizer.optimize_portfolio(prices, objective)
            final_w = res["weights"]
            ret, vol, sh = res["return"], res["volatility"], res["sharpe"]
            frontier = res["frontier"]
        else:
            if abs(total_w - 1.0) > 0.01:
                st.stop()
            final_w = edited["Weight"].tolist()
            cust = optimizer.calculate_custom_portfolio(prices, final_w)
            ret, vol, sh = cust["return"], cust["volatility"], cust["sharpe"]
            full = optimizer.optimize_portfolio(prices, "Max Sharpe")
            frontier = full["frontier"]

        utils.render_insight_box(commentary)

        st.session_state['ai_context'] = {
            'page': 'portfolio',
            'tickers': valid,
            'asset': f"portfolio ({', '.join(valid)})", 'horizon': 'the selected period',
            'sharpe': f"{sh:.2f}", 'ann_ret': f"{ret*100:+.2f}%",
            'vol': f"{vol*100:.2f}%", 'max_dd': 'N/A'
        }

        # ── Action Toolbar ──
        rep_c1, rep_c2 = st.columns([5, 1])
        with rep_c2:
            if st.button("Generate Report", use_container_width=True, key="btn_rep_pf"):
                rep_state = reporting.ReportState(
                    page_type="portfolio",
                    tickers=valid,
                    start_date="the selected period",
                    metrics={
                        "Expected_Annual_Return": f"{ret*100:+.2f}%",
                        "Projected_Volatility": f"{vol*100:.2f}%",
                        "Portfolio_Sharpe": f"{sh:.2f}"
                    },
                    tables={'weights': pd.DataFrame({"Asset": valid, "Weight": final_w})}
                )
                trigger_report_generation(rep_state)
        
        display_report_preview()

        k1, k2, k3 = st.columns(3)
        with k1: utils.render_metric_card("Expected Return", f"{ret*100:.2f}%")
        with k2: utils.render_metric_card("Volatility", f"{vol*100:.2f}%")
        with k3: utils.render_metric_card("Sharpe Ratio", f"{sh:.2f}")

        cf, cp = st.columns(2)
        with cf:
            st.plotly_chart(utils.plot_efficient_frontier(frontier, vol, ret), use_container_width=True, config={"displaylogo": False})
        with cp:
            pie = pd.DataFrame({"Asset": valid, "Weight": final_w})
            pie = pie[pie["Weight"] > 0.005]
            fig_pie = px.pie(pie, values='Weight', names='Asset', hole=0.55,
                             color_discrete_sequence=["#3B82F6","#C5A572","#10B981","#8B5CF6","#F59E0B","#14B8A6"])
            fig_pie = utils.apply_default_layout(fig_pie, "Allocation")
            fig_pie.update_traces(textposition='outside', textinfo='percent+label',
                                  marker=dict(line=dict(color="#0A0E17", width=2)))
            st.plotly_chart(fig_pie, use_container_width=True, config={"displaylogo": False})

        if mode == "Detailed":
            st.plotly_chart(utils.plot_correlation_heatmap(prices), use_container_width=True, config={"displaylogo": False})
            csv_download(pd.DataFrame({"Asset": valid, "Weight": final_w}), "portfolio_weights.csv", "Export Weights")


# ══════════════════════════════════════════
# COPILOT (persistent across all pages)
# ══════════════════════════════════════════

# FAB Button
if st.button("💬", key="copilot_fab"):
    st.session_state.show_chat = not st.session_state.show_chat
    st.rerun()

# Apply the class via Javascript/Markdown hack for the floating button
st.markdown(f"""
    <script>
        var btn = window.parent.document.querySelector('button[key="copilot_fab"]');
        if (btn) {{
            btn.classList.add('floating-copilot-btn');
        }}
    </script>
""", unsafe_allow_html=True)

# Render Chat Drawer
copilot.render_chat_drawer()
