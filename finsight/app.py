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
import ai_copilot

# ── Page Config ──
st.set_page_config(page_title="FinSight", page_icon="◆", layout="wide", initial_sidebar_state="expanded")
utils.inject_premium_css()

# ── Session State ──
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [
        {"role": "assistant", "content": "Welcome to FinSight Copilot. Ask me about any metric, chart, or portfolio on screen."}
    ]
if 'ai_context' not in st.session_state:
    st.session_state['ai_context'] = {}

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

# ── Sidebar Navigation Shell ──
st.sidebar.markdown("""
<div style='padding: 8px 0 20px 0; border-bottom: 1px solid #1F2937; margin-bottom: 16px;'>
    <div style='font-size: 1.2rem; font-weight: 600; color: #F9FAFB; letter-spacing: -0.02em;'>◆ FinSight</div>
    <div style='font-size: 0.7rem; color: #6B7280; margin-top: 2px; letter-spacing: 0.04em; text-transform: uppercase;'>Portfolio Intelligence</div>
</div>
""", unsafe_allow_html=True)

NAV = {
    "📊  Equity Analysis": "equity",
    "⚡  Strategy Backtest": "strategy",
    "🔬  Portfolio Builder": "portfolio",
}
page = st.sidebar.radio("nav", list(NAV.keys()), index=0, label_visibility="collapsed")
page_key = NAV[page]

st.sidebar.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='font-size: 0.65rem; color: #4B5563; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 6px;'>View Mode</div>
""", unsafe_allow_html=True)
mode = st.sidebar.selectbox("mode", ["Summary", "Detailed"], label_visibility="collapsed")

st.sidebar.markdown("""
<div style='position: absolute; bottom: 16px; left: 16px; right: 16px;'>
    <hr style='border-color: #1F2937; margin-bottom: 10px;'>
    <div style='font-size: 0.65rem; color: #4B5563; line-height: 1.4;'>FinSight v2.1 · Not investment advice</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════

if page_key == "equity":
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

                # Context for copilot
                st.session_state['ai_context'] = {
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

                # ── Insight + Gauge side by side ──
                ci, cg = st.columns([2.5, 1])
                with ci:
                    commentary = explainability.summarize_stock_performance(ticker, ann_ret, ann_vol, max_dd, bench_ret)
                    utils.render_insight_box(commentary)
                with cg:
                    st.plotly_chart(utils.plot_risk_gauge(max_dd), use_container_width=True, config={"displayModeBar": False})

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

                st.session_state['ai_context'] = {
                    'asset': ticker, 'horizon': 'the backtest period',
                    'sharpe': 'N/A',
                    'ann_ret': f"{st_ann*100:+.2f}%",
                    'max_dd': f"{st_dd*100:.2f}%"
                }

                m1, m2 = st.columns(2)
                with m1: utils.render_metric_card("Buy & Hold Return", f"{bh_ann*100:.2f}%", f"Max drawdown: {bh_dd*100:.2f}%")
                with m2: utils.render_metric_card(f"MA {short_window}/{long_window} Return", f"{st_ann*100:.2f}%", f"Max drawdown: {st_dd*100:.2f}%")

                utils.render_insight_box(explainability.summarize_strategy_comparison(st_ann, bh_ann, st_dd, bh_dd))

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

        utils.render_insight_box(explainability.summarize_optimization(valid, final_w, ret, None, vol, objective if do_opt else "Custom"))

        st.session_state['ai_context'] = {
            'asset': f"portfolio ({', '.join(valid)})", 'horizon': 'the selected period',
            'sharpe': f"{sh:.2f}", 'ann_ret': f"{ret*100:+.2f}%",
            'vol': f"{vol*100:.2f}%", 'max_dd': 'N/A'
        }

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

with st.popover("💬"):
    st.markdown("<div style='font-size:1rem;font-weight:600;color:#F9FAFB'>FinSight Copilot</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.7rem;color:#6B7280;margin-bottom:12px'>Context-aware assistant</div>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Suggested prompts
    p1, p2 = st.columns(2)
    prompt = None
    if p1.button("Explain Sharpe ratio", key="qp1"): prompt = "Explain my Sharpe ratio"
    if p2.button("Explain this page", key="qp2"): prompt = "Explain this dashboard"
    p3, p4 = st.columns(2)
    if p3.button("Compare vs benchmark", key="qp3"): prompt = "Compare asset vs benchmark"
    if p4.button("Assess risk", key="qp4"): prompt = "Why is my portfolio risky"

    def submit(text):
        if text:
            st.session_state.chat_history.append({"role": "user", "content": text})
            resp = ai_copilot.generate_response(text, st.session_state.ai_context)
            st.session_state.chat_history.append({"role": "assistant", "content": resp})

    if prompt:
        submit(prompt)
        st.rerun()

    user_q = st.chat_input("Ask about your data...")
    if user_q:
        submit(user_q)
        st.rerun()
