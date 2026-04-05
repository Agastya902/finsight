import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Imports from local modules
import data_loader
import metrics
import explainability
import strategies
import optimizer
import utils
import universe
import ai_copilot

# --- Setup Global Config ---
st.set_page_config(page_title="FinSight | Analytics", page_icon="🏦", layout="wide", initial_sidebar_state="expanded")
utils.inject_premium_css()

# --- Initialize AI Copilot State ---
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [{"role": "assistant", "content": "I am FinSight AI, your Portfolio Intelligence Copilot. How can I assist you with your quantitative analysis today?"}]
if 'ai_context' not in st.session_state:
    st.session_state['ai_context'] = {}

# --- Helpers for time horizon presets ---
def get_horizon_dates(horizon: str):
    end_date = datetime.today()
    if horizon == "1Y":
        start = end_date - relativedelta(years=1)
    elif horizon == "3Y":
        start = end_date - relativedelta(years=3)
    elif horizon == "5Y":
        start = end_date - relativedelta(years=5)
    elif horizon == "10Y":
        start = end_date - relativedelta(years=10)
    elif horizon == "Max":
        start = end_date - relativedelta(years=30)
    else:
        start = end_date - relativedelta(years=5)
    return start.date(), end_date.date()

def render_horizon_selector(key_prefix: str):
    h = st.radio("Temporal Horizon", ["1Y", "3Y", "5Y", "10Y", "Max", "Custom"], horizontal=True, key=f"{key_prefix}_rad", label_visibility="collapsed")
    if h == "Custom":
        c1, c2 = st.columns(2)
        s = c1.date_input("Start", value=datetime.today().date() - relativedelta(years=5), key=f"{key_prefix}_start")
        e = c2.date_input("End", value=datetime.today().date(), key=f"{key_prefix}_end")
        return s, e
    return get_horizon_dates(h)

def create_csv_download(df: pd.DataFrame, filename: str, label: str = "📥 Export CSV"):
    csv = df.to_csv(index=True).encode('utf-8')
    st.download_button(label=label, data=csv, file_name=filename, mime='text/csv')

# --- UI Sidebar & Mode Setting ---
st.sidebar.markdown(f"<h1 style='font-size: 1.5rem; color: #F9FAFB; margin-bottom: 0px;'>FinSight</h1>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='font-size: 0.8rem; color: #C5A572; letter-spacing: 0.05em; text-transform: uppercase;'>Quantitative Edge</p>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

nav_options = {
    "🌐 Platform Overview": "Platform Overview",
    "📊 Equity Intelligence": "Equity Analysis",
    "🤖 Algorithmic Validator": "Strategy Backtesting",
    "⚖️ Portfolio Builder": "Portfolio Allocation"
}
page_selection = st.sidebar.radio("WORKSPACE", list(nav_options.keys()), disabled=False)
page = nav_options[page_selection]
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 0.75rem; color: #64748B; letter-spacing: 0.05em; text-transform: uppercase;'>ACTIVE PERSONA</p>", unsafe_allow_html=True)
mode = st.sidebar.selectbox("Persona Selection", ["Client Presentation", "Analyst Workstation"], label_visibility="collapsed")

st.sidebar.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size: 0.75rem; color: #4B5563; line-height: 1.4;'>FinSight Analytics v2.0<br>Confidential. Not investment advice.</p>", unsafe_allow_html=True)

def show_analyst_table(df: pd.DataFrame, title: str):
    if mode == "Analyst Workstation":
        st.markdown(f"<h4 style='color: #F9FAFB; font-size: 1.1rem; margin-top: 30px; margin-bottom: 15px;'>{title}</h4>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)


# ==========================================
# PAGE ROUTING
# ==========================================

if page == "Platform Overview":
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-title">Intelligent Portfolio Architecture</div>
        <div class="hero-subtitle">
            FinSight delivers institutional-grade quantitative modeling married seamlessly with elegant client-facing narratives. Transform complex data into actionable, intuitive insights.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-card'><h3 style='color: #3B82F6; font-size: 1.1rem; margin-bottom: 12px; font-weight: 500;'>Equity Analysis</h3><p style='color: #9CA3AF; font-size: 0.95rem; line-height: 1.5;'>Robust extraction of absolute returns, Sharpe profiles, and maximum drawdowns calculated tightly against normalized benchmark correlations.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h3 style='color: #3B82F6; font-size: 1.1rem; margin-bottom: 12px; font-weight: 500;'>Algorithmic Backtesting</h3><p style='color: #9CA3AF; font-size: 0.95rem; line-height: 1.5;'>Execute trailing validation for standard and bespoke trading methodologies utilizing sophisticated crossover analytics against generic holding profiles.</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><h3 style='color: #3B82F6; font-size: 1.1rem; margin-bottom: 12px; font-weight: 500;'>Capital Allocation (MPT)</h3><p style='color: #9CA3AF; font-size: 0.95rem; line-height: 1.5;'>Solve strict objective functions leveraging SciPy nonlinear optimization for high-fidelity discovery of the efficient frontier and volatility boundaries.</p></div>", unsafe_allow_html=True)
        
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #9CA3AF; font-size: 0.9rem;'>Navigate via the sidebar to evaluate institutional models.</p>", unsafe_allow_html=True)
    
    # Store Context
    st.session_state['ai_context'] = {'horizon': 'the global overview span'}


elif page == "Equity Analysis":
    st.markdown(f"<h2 style='color: #F9FAFB; margin-bottom: 30px;'>Core Equity Intelligence</h2>", unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns([1.5, 1.5, 2])
    
    asset_sel = sc1.selectbox("Underlying Asset", options=list(universe.EQUITY_UNIVERSE.keys()), index=0)
    if asset_sel == "Custom (Type your own)":
        ticker = sc1.text_input("Custom Ticker", value="AAPL").upper().strip()
    else:
        ticker = universe.extract_ticker(asset_sel, universe.EQUITY_UNIVERSE)
        
    bench_sel = sc2.selectbox("Relative Benchmark", options=list(universe.BENCHMARK_PRESETS.keys()), index=0)
    if bench_sel == "Custom (Type your own)":
        benchmark = sc2.text_input("Custom Benchmark", value="SPY").upper().strip()
    else:
        benchmark = universe.extract_ticker(bench_sel, universe.BENCHMARK_PRESETS)
        
    with sc3:
        st.write("Temporal Horizon")
        start_date, end_date = render_horizon_selector("eq")
    
    if start_date >= end_date:
        st.error("Protocol Error: The evaluated temporal span is negative.")
        st.stop()
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if data_loader.validate_ticker(ticker):
        with st.spinner(f"Aggregating distributed market data for {ticker}..."):
            tickers_to_fetch = [ticker]
            if data_loader.validate_ticker(benchmark):
                tickers_to_fetch.append(benchmark)
                
            data = data_loader.fetch_stock_data(tickers_to_fetch, start_date, end_date)
            
            if not data.empty and ticker in data.columns:
                prices = data[ticker]
                daily_returns = metrics.calculate_daily_returns(prices)
                
                if len(daily_returns) == 0:
                    st.warning("Insufficient valid trading data returned to compute statistical features.")
                    st.stop()
                
                ann_ret = metrics.calculate_annualized_return(daily_returns)
                ann_vol = metrics.calculate_annualized_volatility(daily_returns)
                max_dd = metrics.calculate_max_drawdown(prices)
                sharpe = metrics.calculate_sharpe_ratio(daily_returns)
                
                bench_ret = None
                if benchmark and benchmark in data.columns:
                    bench_prices = data[benchmark]
                    bench_daily = metrics.calculate_daily_returns(bench_prices)
                    bench_ret = metrics.calculate_annualized_return(bench_daily)
                
                m1, m2, m3, m4 = st.columns(4)
                with m1: utils.render_metric_card("Compound Ann. Return", f"{ann_ret*100:+.2f}%")
                with m2: utils.render_metric_card("Annualized Volatility", f"{ann_vol*100:.2f}%")
                with m3: utils.render_metric_card("Maximum Drawdown", f"{max_dd*100:+.2f}%")
                with m4: utils.render_metric_card("Sharpe Ratio", f"{sharpe:.2f}")
                
                # Context integration for AI
                st.session_state['ai_context'] = {
                    'asset': ticker,
                    'benchmark': benchmark,
                    'horizon': 'the selected horizon',
                    'sharpe': f"{sharpe:.2f}",
                    'ann_ret': f"{ann_ret*100:+.2f}%",
                    'vol': f"{ann_vol*100:.2f}%",
                    'max_dd': f"{max_dd*100:+.2f}%"
                }
                
                c_insight, c_gauge = st.columns([2, 1])
                with c_insight:
                    utils.render_insight_box(explainability.summarize_stock_performance(ticker, ann_ret, ann_vol, max_dd, bench_ret))
                with c_gauge:
                    st.plotly_chart(utils.plot_risk_gauge(max_dd), use_container_width=True, config={"displayModeBar": False})
                
                st.markdown("<br>", unsafe_allow_html=True)
                t1, t2, t3, t4 = st.columns(4)
                show_price = t1.checkbox("Base Price Overlay", value=True)
                show_50 = t2.checkbox("50-Day Momentum", value=True)
                show_200 = t3.checkbox("200-Day Macro Trend", value=True)
                show_dd = t4.checkbox("Drawdown Topology", value=False)
                
                prices_df = pd.DataFrame({ticker: prices})
                prices_df['SMA (50)'] = prices.rolling(window=50).mean()
                prices_df['SMA (200)'] = prices.rolling(window=200).mean()
                
                if show_dd:
                    rolling_max = prices.cummax()
                    drawdown = (prices - rolling_max) / rolling_max
                    fig_price = go.Figure()
                    fig_price.add_trace(go.Scatter(x=drawdown.index, y=drawdown*100, name="Drawdown %", line=dict(color="#EF4444", width=1.5), fill='tozeroy', fillcolor="rgba(239, 68, 68, 0.1)"))
                    fig_price = utils.apply_default_layout(fig_price, "Historical Drawdown Profile")
                    fig_price.update_yaxes(title="Loss %", ticksuffix="%")
                    st.plotly_chart(fig_price, use_container_width=True, config={"displaylogo": False})
                else:
                    fig_price = go.Figure()
                    if show_price:
                        fig_price.add_trace(go.Scatter(x=prices_df.index, y=prices_df[ticker], name="Close Price", line=dict(color="#3B82F6", width=1.5)))
                    if show_50:
                        fig_price.add_trace(go.Scatter(x=prices_df.index, y=prices_df['SMA (50)'], name="50-day Mean", line=dict(color="#10B981", width=1, dash='dot')))
                    if show_200:
                        fig_price.add_trace(go.Scatter(x=prices_df.index, y=prices_df['SMA (200)'], name="200-day Mean", line=dict(color="#C5A572", width=1, dash='dash')))
                    
                    fig_price = utils.apply_default_layout(fig_price, "Asset Trajectory & Moving Averages")
                    st.plotly_chart(fig_price, use_container_width=True, config={"displaylogo": False, "toImageButtonOptions": {"format": "png", "filename": f"{ticker}_chart"}})
                
                if mode == "Analyst Workstation":
                    st.markdown("<br>", unsafe_allow_html=True)
                    df_export = prices_df.copy()
                    create_csv_download(df_export, f"{ticker}_pricing_data.csv")
                    fig_hist = px.histogram(daily_returns, nbins=60)
                    fig_hist.update_traces(marker_color="#3B82F6", opacity=0.7)
                    fig_hist = utils.apply_default_layout(fig_hist, "Statistical Probability Density: Daily Returns")
                    st.plotly_chart(fig_hist, use_container_width=True, config={"displaylogo": False})
                
                if st.button("Generate Dashboard Summary", icon="📝", use_container_width=True):
                    ext = explainability.summarize_stock_performance(ticker, ann_ret, ann_vol, max_dd, bench_ret)
                    with st.container():
                        st.markdown("<div style='background-color: rgba(17,24,39,0.7); border: 1px solid #1F2937; padding: 24px; border-radius: 8px; margin-top: 15px;'>", unsafe_allow_html=True)
                        st.markdown(ext)
                        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Strategy Backtesting":
    st.markdown(f"<h2 style='color: #F9FAFB; margin-bottom: 30px;'>Algorithmic Validator</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<br><hr>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='font-size: 0.75rem; color: #9CA3AF; letter-spacing: 0.05em; text-transform: uppercase;'>Model Hyperparameters</p>", unsafe_allow_html=True)
    short_window = st.sidebar.number_input("Fast Signal Period", min_value=5, max_value=100, value=50)
    long_window = st.sidebar.number_input("Slow Trend Period", min_value=20, max_value=300, value=200)
    
    sc1, sc3 = st.columns([1.5, 2])
    asset_sel = sc1.selectbox("Asset Under Test", options=list(universe.EQUITY_UNIVERSE.keys()), index=0)
    if asset_sel == "Custom (Type your own)":
        ticker = sc1.text_input("Custom Ticker", value="AAPL").upper().strip()
    else:
        ticker = universe.extract_ticker(asset_sel, universe.EQUITY_UNIVERSE)
        
    with sc3:
        st.write("Temporal Horizon")
        start_date, end_date = render_horizon_selector("strat")
    
    if data_loader.validate_ticker(ticker):
        with st.spinner("Backtesting strategy vectors..."):
            data = data_loader.fetch_stock_data([ticker], start_date, end_date)
            
            if not data.empty and ticker in data.columns:
                prices = data[ticker]
                
                strat_df = strategies.run_moving_average_crossover(prices, short_window, long_window)
                buy_hold_returns = metrics.calculate_daily_returns(prices)
                strat_returns = strat_df['Strategy_Daily_Return'].dropna()
                
                bh_ann_ret = metrics.calculate_annualized_return(buy_hold_returns)
                bh_dd = metrics.calculate_max_drawdown(strat_df['Price'])
                strat_ann_ret = metrics.calculate_annualized_return(strat_returns)
                strat_dd = metrics.calculate_max_drawdown(strat_df['Strategy_Cum_Ret'])
                
                st.session_state['ai_context'] = {'asset': ticker, 'horizon': 'the backtest horizon', 'sharpe': 'N/A', 'ann_ret': f"{strat_ann_ret*100:+.2f}%", 'vol': f"{metrics.calculate_annualized_volatility(strat_returns)*100:.2f}%", 'max_dd': f"{strat_dd*100:+.2f}%"}
                
                st.markdown("<br>", unsafe_allow_html=True)
                m1, m2 = st.columns(2)
                with m1: utils.render_metric_card("Buy & Hold Strategy CAGR", f"{bh_ann_ret*100:.2f}%", f"Drawdown tolerance: {bh_dd*100:.2f}%")
                with m2: utils.render_metric_card(f"Algorithmic (MA {short_window}/{long_window}) CAGR", f"{strat_ann_ret*100:.2f}%", f"Drawdown tolerance: {strat_dd*100:.2f}%")
                
                utils.render_insight_box(explainability.summarize_strategy_comparison(strat_ann_ret, bh_ann_ret, strat_dd, bh_dd))
                
                fig = go.Figure()
                bh_cum = (1 + buy_hold_returns).cumprod()
                fig.add_trace(go.Scatter(x=bh_cum.index, y=bh_cum, name="Underlying Buy & Hold", line=dict(color="#9CA3AF", width=1.5, dash="dash")))
                fig.add_trace(go.Scatter(x=strat_df.index, y=strat_df['Strategy_Cum_Ret'], name="Crossover Model Outcome", line=dict(color="#3B82F6", width=2)))
                fig = utils.apply_default_layout(fig, "Algorithm Capital Cultivation vs Passive Benchmark")
                st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})
                
                if mode == "Analyst Workstation":
                    create_csv_download(strat_df, f"{ticker}_strategy_export.csv", "📥 Export Backtest Data")

elif page == "Portfolio Allocation":
    st.markdown(f"<h2 style='color: #F9FAFB; margin-bottom: 30px;'>Portfolio Builder & Optimizer</h2>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown(f"<p style='color: #9CA3AF; margin-bottom: 4px; font-size: 0.9rem;'>Target Asset Pool (Select up to 10)</p>", unsafe_allow_html=True)
        default_idx = [list(universe.EQUITY_UNIVERSE.keys()).index(x) for x in ["Apple Inc. (AAPL)", "Microsoft Corp. (MSFT)", "Alphabet Inc. Class A (GOOGL)", "Amazon.com Inc. (AMZN)"]]
        asset_selections = st.multiselect("", options=list(universe.EQUITY_UNIVERSE.keys()), default=[list(universe.EQUITY_UNIVERSE.keys())[i] for i in default_idx], label_visibility="collapsed")
        tickers = [universe.extract_ticker(x, universe.EQUITY_UNIVERSE) for x in asset_selections]
        if "Custom (Type your own)" in asset_selections:
            custom = st.text_input("Add Custom Ticker Sequence (comma separated)")
            if custom:
                tickers.extend([x.strip().upper() for x in custom.split(",")])
                try:
                    tickers.remove("CUSTOM")
                except ValueError:
                    pass
                
    with col_r:
        st.write("Temporal Evaluation Horizon")
        start_date, end_date = render_horizon_selector("opt")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if len(tickers) < 2:
        st.warning("Insufficient parameters: Portfolio construction requires at least two discrete components.")
        st.stop()
        
    data = data_loader.fetch_stock_data(tickers, start_date, end_date)
    if data.empty:
        st.error("Failed to acquire data matrix for selected assets.")
        st.stop()
        
    valid_tickers = [t for t in tickers if t in data.columns]
    target_prices = data[valid_tickers]
    
    st.markdown("### Allocation Builder")
    c_build, c_action = st.columns([2, 1])
    
    with c_build:
        init_weights = [1.0/len(valid_tickers)] * len(valid_tickers)
        df_builder = pd.DataFrame({"Asset": valid_tickers, "Weight": init_weights})
        edited_df = st.data_editor(df_builder, column_config={"Weight": st.column_config.NumberColumn("Weight", min_value=0.0, max_value=1.0, step=0.01, format="%.3f")}, hide_index=True, use_container_width=True)
        
    with c_action:
        st.markdown("<p style='font-size: 0.8rem; color: #9CA3AF;'>Optimization Engine</p>", unsafe_allow_html=True)
        objective = st.selectbox("Algorithmic Priority", ["Max Sharpe", "Min Volatility"])
        do_optimize = st.button("▶ Execute Institutional Optimization", use_container_width=True)
        
        total_w = edited_df["Weight"].sum()
        if abs(total_w - 1.0) > 0.01 and not do_optimize:
            st.warning(f"Weights sub-optimal: Sum = {total_w:.2f} (Target = 1.0)")
            
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    with st.spinner("Compiling portfolio tensors and generating analytical views..."):
        if do_optimize:
            opt_result = optimizer.optimize_portfolio(target_prices, objective)
            final_weights = opt_result["weights"]
            opt_ret = opt_result["return"]
            opt_vol = opt_result["volatility"]
            opt_sharpe = opt_result["sharpe"]
            frontier = opt_result["frontier"]
            utils.render_insight_box(explainability.summarize_optimization(valid_tickers, final_weights, opt_ret, None, opt_vol, objective))
        else:
            if abs(total_w - 1.0) > 0.01:
                st.stop() 
            final_weights = edited_df["Weight"].tolist()
            custom_result = optimizer.calculate_custom_portfolio(target_prices, final_weights)
            opt_ret = custom_result["return"]
            opt_vol = custom_result["volatility"]
            opt_sharpe = custom_result["sharpe"]
            opt_full = optimizer.optimize_portfolio(target_prices, "Max Sharpe") 
            frontier = opt_full["frontier"]
            utils.render_insight_box(explainability.summarize_optimization(valid_tickers, final_weights, opt_ret, None, opt_vol, "Custom Allocation Matrix"))
            
        m1, m2, m3 = st.columns(3)
        with m1: utils.render_metric_card("Expected Target CAGR", f"{opt_ret*100:.2f}%")
        with m2: utils.render_metric_card("Constrained Volatility", f"{opt_vol*100:.2f}%")
        with m3: utils.render_metric_card("Calculated Sharpe Profile", f"{opt_sharpe:.2f}")
        
        st.session_state['ai_context'] = {'asset': f"Portfolio composed of {valid_tickers}", 'horizon': 'the portfolio lifespan', 'sharpe': f"{opt_sharpe:.2f}", 'ann_ret': f"{opt_ret*100:+.2f}%", 'vol': f"{opt_vol*100:.2f}%", 'max_dd': "unknown"}
        
        st.markdown("<br>", unsafe_allow_html=True)
        c_p, c_f = st.columns(2)
        with c_p:
            fig_front = utils.plot_efficient_frontier(frontier, opt_vol, opt_ret)
            st.plotly_chart(fig_front, use_container_width=True, config={"displaylogo": False, "toImageButtonOptions": {"format": "png", "filename": "efficient_frontier"}})
        with c_f:
            pie_data = pd.DataFrame({"Asset": valid_tickers, "Weight": final_weights})
            pie_data = pie_data[pie_data["Weight"] > 0.005]
            fig_pie = px.pie(pie_data, values='Weight', names='Asset', hole=0.6, color_discrete_sequence=[utils.COLORS['primary'], utils.COLORS['secondary'], utils.COLORS['success'], "#8B5CF6", "#F59E0B", "#14B8A6"])
            fig_pie = utils.apply_default_layout(fig_pie, f"Live Composition Matrix")
            fig_pie.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color=utils.COLORS['background'], width=2)))
            st.plotly_chart(fig_pie, use_container_width=True, config={"displaylogo": False})
            
        if mode == "Analyst Workstation":
            st.markdown("<br>", unsafe_allow_html=True)
            st.plotly_chart(utils.plot_correlation_heatmap(target_prices), use_container_width=True, config={"displaylogo": False})
            export_df = pd.DataFrame({"Asset": valid_tickers, "Capital Allocation": final_weights})
            create_csv_download(export_df, "portfolio_allocation_export.csv", "📥 Download Portfolio Configuration")


# ==========================================
# FLOATING AI COPILOT
# ==========================================

# Use Streamlit Popover directly inside the floating UI CSS block
with st.popover("💬"):
    st.markdown("<h4 style='color: #F9FAFB; margin-bottom: 2px;'>FinSight AI</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.8rem; color: #9CA3AF; margin-bottom: 15px;'>Portfolio Intelligence Copilot</p>", unsafe_allow_html=True)
    
    # Render Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Prompts
    qp1, qp2 = st.columns(2)
    qp3, qp4 = st.columns(2)
    
    selected_quick_prompt = None
    if qp1.button("Explain Sharpe ratio"): selected_quick_prompt = "Explain my Sharpe ratio"
    if qp2.button("Compare AAPL vs SPY"): selected_quick_prompt = "Compare AAPL vs SPY"
    if qp3.button("Build diversified portfolio"): selected_quick_prompt = "Build diversified portfolio"
    if qp4.button("What does drawdown mean?"): selected_quick_prompt = "What does drawdown mean?"
    
    # Input Processing
    def handle_submit(user_input: str):
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            ai_response = ai_copilot.generate_response(user_input, st.session_state.ai_context)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

    if selected_quick_prompt:
        handle_submit(selected_quick_prompt)
        st.rerun()

    # Chat string input wrapper
    user_q = st.chat_input("Ask FinSight AI...")
    if user_q:
        handle_submit(user_q)
        st.rerun()
