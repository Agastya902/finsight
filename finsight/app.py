import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Imports from local modules
import data_loader
import metrics
import explainability
import strategies
import optimizer
import utils

# --- Setup Global Config ---
st.set_page_config(page_title="FinSight | Analytics", page_icon="🏦", layout="wide", initial_sidebar_state="expanded")

# --- UI Premium Overrides ---
utils.inject_premium_css()

# --- UI Sidebar & Mode Setting ---
st.sidebar.markdown(f"<h1 style='font-size: 1.5rem; color: {utils.COLORS['text']}; margin-bottom: 0px;'>FinSight</h1>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='font-size: 0.8rem; color: {utils.COLORS['secondary']}; letter-spacing: 0.05em; text-transform: uppercase;'>Quantitative Edge</p>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

page = st.sidebar.radio("WORKSPACE", ["Platform Overview", "Equity Analysis", "Strategy Backtesting", "Portfolio Allocation"], disabled=False)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 0.75rem; color: #64748B; letter-spacing: 0.05em; text-transform: uppercase;'>ACTIVE PERSONA</p>", unsafe_allow_html=True)
mode = st.sidebar.selectbox("Persona Selection", ["Client Presentation", "Analyst Workstation"], label_visibility="collapsed")

st.sidebar.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size: 0.75rem; color: #4B5563; line-height: 1.4;'>FinSight Analytics v1.0<br>Confidential. Not investment advice.</p>", unsafe_allow_html=True)

# Default dates
def_start, def_end = data_loader.get_default_date_range()

# --- Component specific styling wrappers ---
def show_analyst_table(df: pd.DataFrame, title: str):
    """Render an elegant table specifically for analyst mode without breaking CSS constraints."""
    if mode == "Analyst Workstation":
        st.markdown(f"<h4 style='color: {utils.COLORS['text']}; font-size: 1.1rem; margin-top: 30px; margin-bottom: 15px;'>{title}</h4>", unsafe_allow_html=True)
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
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {utils.COLORS['primary']}; font-size: 1.1rem; margin-bottom: 12px; font-weight: 500;">Equity Analysis</h3>
            <p style="color: {utils.COLORS['muted_text']}; font-size: 0.95rem; line-height: 1.5;">Robust extraction of absolute returns, Sharpe profiles, and maximum drawdowns calculated tightly against normalized benchmark correlations.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {utils.COLORS['primary']}; font-size: 1.1rem; margin-bottom: 12px; font-weight: 500;">Algorithmic Backtesting</h3>
            <p style="color: {utils.COLORS['muted_text']}; font-size: 0.95rem; line-height: 1.5;">Execute trailing validation for standard and bespoke trading methodologies utilizing sophisticated crossover analytics against generic holding profiles.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {utils.COLORS['primary']}; font-size: 1.1rem; margin-bottom: 12px; font-weight: 500;">Capital Allocation (MPT)</h3>
            <p style="color: {utils.COLORS['muted_text']}; font-size: 0.95rem; line-height: 1.5;">Solve strict objective functions leveraging SciPy nonlinear optimization for high-fidelity discovery of the efficient frontier and volatility boundaries.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {utils.COLORS['muted_text']}; font-size: 0.9rem;'>To begin, navigate using the sidebar. Platform is currently pre-configured for broad-market assets (e.g., AAPL, MSFT, SPY).</p>", unsafe_allow_html=True)


elif page == "Equity Analysis":
    st.markdown(f"<h2 style='color: {utils.COLORS['text']}; margin-bottom: 30px;'>Core Equity Intelligence</h2>", unsafe_allow_html=True)
    
    # Premium search bar integration
    sc1, sc2, sc3, sc4 = st.columns([1.5, 1.5, 1, 1])
    ticker = sc1.text_input("Underlying Asset", value="AAPL")
    benchmark = sc2.text_input("Relative Benchmark", value="SPY")
    start_date = sc3.date_input("Horizon Start", value=def_start)
    end_date = sc4.date_input("Horizon End", value=def_end)
    
    if start_date >= end_date:
        st.error("Protocol Error: The evaluated temporal span is negative. Ensure the horizon end succeeds the origin.")
        st.stop()
        
    ticker = ticker.upper().strip()
    benchmark = benchmark.upper().strip()
    
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
                
                # Render Premium Metric Cards
                m1, m2, m3, m4 = st.columns(4)
                with m1: utils.render_metric_card("Compound Ann. Return", f"{ann_ret*100:+.2f}%")
                with m2: utils.render_metric_card("Annualized Volatility", f"{ann_vol*100:.2f}%")
                with m3: utils.render_metric_card("Maximum Drawdown", f"{max_dd*100:+.2f}%")
                with m4: utils.render_metric_card("Sharpe Ratio", f"{sharpe:.2f}")
                
                # Client Insight box
                utils.render_insight_box(explainability.summarize_stock_performance(ticker, ann_ret, ann_vol, max_dd, bench_ret))
                
                # Premium Charting
                prices_df = pd.DataFrame({ticker: prices})
                prices_df['SMA (50)'] = prices.rolling(window=50).mean()
                prices_df['SMA (200)'] = prices.rolling(window=200).mean()
                
                st.markdown("<br>", unsafe_allow_html=True)
                fig_price = go.Figure()
                fig_price.add_trace(go.Scatter(x=prices_df.index, y=prices_df[ticker], name="Close Price", line=dict(color=utils.COLORS["primary"], width=1.5)))
                fig_price.add_trace(go.Scatter(x=prices_df.index, y=prices_df['SMA (50)'] , name="50-day Mean", line=dict(color=utils.COLORS["success"], width=1, dash='dot')))
                fig_price.add_trace(go.Scatter(x=prices_df.index, y=prices_df['SMA (200)'], name="200-day Mean", line=dict(color=utils.COLORS["secondary"], width=1, dash='dash')))
                fig_price = utils.apply_default_layout(fig_price, "Asset Trajectory & Simple Moving Averages")
                
                st.plotly_chart(fig_price, use_container_width=True)
                
                if mode == "Analyst Workstation":
                    st.markdown("<br>", unsafe_allow_html=True)
                    fig_hist = px.histogram(daily_returns, nbins=60)
                    fig_hist.update_traces(marker_color=utils.COLORS["primary"], opacity=0.7)
                    fig_hist = utils.apply_default_layout(fig_hist, "Statistical Probability Density: Daily Returns")
                    st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.warning(f"Could not construct time-series for {ticker}. The asset may have been delisted or lacks historical volume.")


elif page == "Strategy Backtesting":
    st.markdown(f"<h2 style='color: {utils.COLORS['text']}; margin-bottom: 30px;'>Algorithmic Validator</h2>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<br><hr>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='font-size: 0.75rem; color: #9CA3AF; letter-spacing: 0.05em; text-transform: uppercase;'>Model Hyperparameters</p>", unsafe_allow_html=True)
    short_window = st.sidebar.number_input("Fast Signal Period", min_value=5, max_value=100, value=50)
    long_window = st.sidebar.number_input("Slow Trend Period", min_value=20, max_value=300, value=200)
    
    col1, col2 = st.columns([1, 2])
    ticker = col1.text_input("Asset Under Test", value="SPY").upper()
    
    if data_loader.validate_ticker(ticker):
        with st.spinner("Backtesting strategy vectors..."):
            data = data_loader.fetch_stock_data([ticker], def_start, def_end)
            
            if not data.empty and ticker in data.columns:
                prices = data[ticker]
                
                strat_df = strategies.run_moving_average_crossover(prices, short_window, long_window)
                buy_hold_returns = metrics.calculate_daily_returns(prices)
                strat_returns = strat_df['Strategy_Daily_Return'].dropna()
                
                bh_ann_ret = metrics.calculate_annualized_return(buy_hold_returns)
                bh_dd = metrics.calculate_max_drawdown(strat_df['Price'])
                
                strat_ann_ret = metrics.calculate_annualized_return(strat_returns)
                strat_dd = metrics.calculate_max_drawdown(strat_df['Strategy_Cum_Ret'])
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Metric Comparison Cards
                m1, m2 = st.columns(2)
                with m1: 
                    utils.render_metric_card("Buy & Hold Strategy CAGR", f"{bh_ann_ret*100:.2f}%", f"Drawdown tolerance: {bh_dd*100:.2f}%")
                with m2: 
                    utils.render_metric_card(f"Algorithmic (MA {short_window}/{long_window}) CAGR", f"{strat_ann_ret*100:.2f}%", f"Drawdown tolerance: {strat_dd*100:.2f}%")
                
                # Insight
                utils.render_insight_box(explainability.summarize_strategy_comparison(strat_ann_ret, bh_ann_ret, strat_dd, bh_dd))
                
                # Premium Comparison Chart
                fig = go.Figure()
                
                bh_cum = (1 + buy_hold_returns).cumprod()
                fig.add_trace(go.Scatter(x=bh_cum.index, y=bh_cum, name="Underlying Buy & Hold", line=dict(color=utils.COLORS["muted_text"], width=1.5, dash="dash")))
                fig.add_trace(go.Scatter(x=strat_df.index, y=strat_df['Strategy_Cum_Ret'], name="Crossover Model Outcome", line=dict(color=utils.COLORS["primary"], width=2)))
                
                fig = utils.apply_default_layout(fig, "Algorithm Capital Cultivation vs Passive Benchmark")
                st.plotly_chart(fig, use_container_width=True)
                
                if mode == "Analyst Workstation":
                    metrics_df = pd.DataFrame({
                        "Methodology": ["Passive Hold", f"Signal Model ({short_window},{long_window})"],
                        "Compound Rate (%)": [f"{bh_ann_ret*100:.2f}%", f"{strat_ann_ret*100:.2f}%"],
                        "Deepest Drawdown (%)": [f"{bh_dd*100:.2f}%", f"{strat_dd*100:.2f}%"],
                        "Expected Risk/Vol (%)": [f"{metrics.calculate_annualized_volatility(buy_hold_returns)*100:.2f}%", 
                                           f"{metrics.calculate_annualized_volatility(strat_returns)*100:.2f}%"]
                    })
                    show_analyst_table(metrics_df, "Empirical Strategy Testing Profile")


elif page == "Portfolio Allocation":
    st.markdown(f"<h2 style='color: {utils.COLORS['text']}; margin-bottom: 30px;'>Optimization Matrix</h2>", unsafe_allow_html=True)
    
    default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    st.markdown(f"<p style='color: {utils.COLORS['muted_text']}; margin-bottom: 4px; font-size: 0.9rem;'>Target Asset Pool (Max 10 recommended)</p>", unsafe_allow_html=True)
    tickers = st.multiselect("", default_tickers + ["NVDA", "TSLA", "META", "BRK-B", "JNJ", "V", "JPM", "UNH"], default=default_tickers, label_visibility="collapsed")
    
    col1, col2 = st.columns([1.5, 2])
    benchmark = col1.text_input("Relative Benchmark Index", "SPY").upper()
    objective = col2.selectbox("Mathematical Objective", ["Max Sharpe", "Min Volatility"])
    
    if len(tickers) < 2:
        st.warning("Insufficient parameters: Modern Portfolio Theory requires at least two discrete components to compute variance.")
        st.stop()
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Execute Portfolio Solvers", use_container_width=False):
        with st.spinner("Aligning covariant data structures and seeking minimums..."):
            all_tickers = list(set([t.upper().strip() for t in tickers] + ([benchmark] if benchmark else [])))
            data = data_loader.fetch_stock_data(all_tickers, def_start, def_end)
            
            if not data.empty:
                valid_tickers = [t for t in tickers if t in data.columns]
                
                if len(valid_tickers) < 2:
                    st.error("Insufficient robust data available to satisfy optimization array bounds.")
                    st.stop()
                    
                target_prices = data[valid_tickers]
                
                try:
                    opt_result = optimizer.optimize_portfolio(target_prices, objective)
                    opt_weights = opt_result["weights"]
                    opt_ret = opt_result["return"]
                    opt_vol = opt_result["volatility"]
                    
                    bench_ret = None
                    if benchmark and benchmark in data.columns:
                        b_daily = metrics.calculate_daily_returns(data[benchmark])
                        bench_ret = metrics.calculate_annualized_return(b_daily)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    m1, m2, m3 = st.columns(3)
                    with m1: utils.render_metric_card("Expected Target CAGR", f"{opt_ret*100:.2f}%")
                    with m2: utils.render_metric_card("Constrained Volatility", f"{opt_vol*100:.2f}%")
                    with m3: utils.render_metric_card("Optimum Sharpe", f"{opt_result['sharpe']:.2f}")
                    
                    utils.render_insight_box(explainability.summarize_optimization(valid_tickers, opt_weights, opt_ret, bench_ret, opt_vol, objective))
                    
                    col_chart, col_empty = st.columns([2, 1]) # Make chart slightly smaller
                    with col_chart:
                        pie_data = pd.DataFrame({"Asset": valid_tickers, "Weight": opt_weights})
                        pie_data = pie_data[pie_data["Weight"] > 0.005]
                        
                        fig_pie = px.pie(
                            pie_data, 
                            values='Weight', 
                            names='Asset', 
                            hole=0.6,
                            color_discrete_sequence=[utils.COLORS['primary'], utils.COLORS['secondary'], utils.COLORS['success'], "#8B5CF6", "#F59E0B", "#14B8A6"]
                        )
                        
                        fig_pie = utils.apply_default_layout(fig_pie, f"Calculated Composition Weights: {objective}")
                        fig_pie.update_traces(
                            textposition='outside', 
                            textinfo='percent+label', 
                            marker=dict(line=dict(color=utils.COLORS['background'], width=2))
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    if mode == "Analyst Workstation":
                        weight_df = pd.DataFrame({
                            "Underlying Token": valid_tickers, 
                            "Capital Mandate (%)": [f"{w*100:.2f}%" for w in opt_weights]
                        }).sort_values(by="Capital Mandate (%)", ascending=False)
                        show_analyst_table(weight_df, "Allocation Covariance Outputs")
                        
                except Exception as e:
                    st.error(f"Solver Failure: The optimization engine encountered an irreducible tensor limitation. ({str(e)})")
