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
st.set_page_config(page_title="FinSight", page_icon="📈", layout="wide")

# --- UI Sidebar & Mode Setting ---
st.sidebar.title("📈 FinSight")
st.sidebar.markdown("**Explainable Fintech Portfolio Intelligence**")

mode = st.sidebar.radio("View Mode", ["Client Mode", "Analyst Mode"])
st.sidebar.markdown("---")

st.sidebar.info("This tool is for educational and demonstration purposes only and does not constitute investment advice.")

# Default dates
def_start, def_end = data_loader.get_default_date_range()

# Navigation
page = st.sidebar.selectbox("Navigation", ["Overview", "Stock Analysis", "Strategy Backtesting", "Portfolio Optimizer"])

def show_analyst_charts(charts, columns=2):
    """Helper to conditionally show charts."""
    if mode == "Analyst Mode":
        cols = st.columns(columns)
        for i, fig in enumerate(charts):
            cols[i % columns].plotly_chart(fig, use_container_width=True)

# --- Routing ---
if page == "Overview":
    st.title("Welcome to FinSight")
    st.markdown("""
    FinSight is an explainable portfolio intelligence tool designed for financial analysts, fintech product teams, and client presentations.
    It marries institutional-grade analytics with plain-English insights.
    
    **Key Features**:
    - **Stock Analytics**: Visualize daily returns, moving averages, and cumulative risk-adjusted metrics.
    - **Strategy Backtesting**: Compare standard technical trading strategies against simple Buy & Hold.
    - **Portfolio Optimization**: Modern Portfolio Theory (MPT) powered asset allocation.
    - **Explainable Insights**: Automated summarizations translating complex metrics to narrative English.
    
    ### Try entering these default tickers in the tools:
    `AAPL`, `MSFT`, `NVDA`, `SPY`, `AMZN`, `GOOGL`
    """)

elif page == "Stock Analysis":
    st.title("Stock Analysis")
    
    col1, col2, col3 = st.columns(3)
    ticker = col1.text_input("Ticker Symbol", value="AAPL")
    benchmark = col2.text_input("Benchmark Ticker", value="SPY")
    
    date_col1, date_col2 = col3.columns(2)
    start_date = date_col1.date_input("Start Date", value=def_start)
    end_date = date_col2.date_input("End Date", value=def_end)
    
    if start_date >= end_date:
        st.error("Error: End date must fall after start date.")
        st.stop()
        
    ticker = ticker.upper()
    benchmark = benchmark.upper()
    
    if data_loader.validate_ticker(ticker):
        tickers_to_fetch = [ticker]
        if benchmark:
            tickers_to_fetch.append(benchmark)
            
        data = data_loader.fetch_stock_data(tickers_to_fetch, start_date, end_date)
        
        if not data.empty and ticker in data.columns:
            prices = data[ticker]
            daily_returns = metrics.calculate_daily_returns(prices)
            
            ann_ret = metrics.calculate_annualized_return(daily_returns)
            ann_vol = metrics.calculate_annualized_volatility(daily_returns)
            max_dd = metrics.calculate_max_drawdown(prices)
            sharpe = metrics.calculate_sharpe_ratio(daily_returns)
            
            # Benchmark processing
            bench_ret = None
            if benchmark and benchmark in data.columns:
                bench_prices = data[benchmark]
                bench_daily = metrics.calculate_daily_returns(bench_prices)
                bench_ret = metrics.calculate_annualized_return(bench_daily)
            
            # --- Results ---
            st.markdown("### Explainable Insight")
            st.info(explainability.summarize_stock_performance(ticker, ann_ret, ann_vol, max_dd, bench_ret))
            
            st.markdown("### Metrics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Annualized Return", f"{ann_ret*100:.2f}%")
            m2.metric("Annualized Volatility", f"{ann_vol*100:.2f}%", help="Measure of price fluctuations over time.")
            m3.metric("Max Drawdown", f"{max_dd*100:.2f}%", help="Maximum observed loss from a peak to a trough.")
            m4.metric("Sharpe Ratio", f"{sharpe:.2f}", help="Risk-adjusted return.")
            
            # Charts
            prices_df = pd.DataFrame({ticker: prices})
            prices_df['SMA (50)'] = prices.rolling(window=50).mean()
            prices_df['SMA (200)'] = prices.rolling(window=200).mean()
            
            fig_price = go.Figure()
            fig_price.add_trace(go.Scatter(x=prices_df.index, y=prices_df[ticker], name="Price", line=dict(color=utils.COLORS["primary"])))
            fig_price.add_trace(go.Scatter(x=prices_df.index, y=prices_df['SMA (50)'], name="50-day SMA", line=dict(color=utils.COLORS["warning"], dash='dot')))
            fig_price.add_trace(go.Scatter(x=prices_df.index, y=prices_df['SMA (200)'], name="200-day SMA", line=dict(color=utils.COLORS["secondary"], dash='dash')))
            fig_price = utils.apply_default_layout(fig_price, "Price History & Moving Averages")
            
            if mode == "Analyst Mode":
                st.plotly_chart(fig_price, use_container_width=True)
                
                fig_hist = px.histogram(daily_returns, nbins=50, title="Daily Returns Distribution")
                fig_hist.update_traces(marker_color=utils.COLORS["primary"])
                fig_hist = utils.apply_default_layout(fig_hist, "Daily Returns Distribution")
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.plotly_chart(fig_price, use_container_width=True)


elif page == "Strategy Backtesting":
    st.title("Strategy Backtesting")
    
    col1, col2 = st.columns(2)
    ticker = col1.text_input("Asset Ticker", value="SPY").upper()
    benchmark = col2.text_input("Benchmark Ticker (for comparison)", value="SPY").upper()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Strategy Parameters")
    short_window = st.sidebar.number_input("Short Window", min_value=5, max_value=100, value=50)
    long_window = st.sidebar.number_input("Long Window", min_value=20, max_value=300, value=200)
    
    if data_loader.validate_ticker(ticker):
        data = data_loader.fetch_stock_data([ticker], def_start, def_end)
        
        if not data.empty and ticker in data.columns:
            prices = data[ticker]
            
            # Run strategies
            strat_df = strategies.run_moving_average_crossover(prices, short_window, long_window)
            buy_hold_returns = metrics.calculate_daily_returns(prices)
            strat_returns = strat_df['Strategy_Daily_Return'].dropna()
            
            # Metrics
            bh_ann_ret = metrics.calculate_annualized_return(buy_hold_returns)
            bh_dd = metrics.calculate_max_drawdown(strat_df['Price'])
            
            strat_ann_ret = metrics.calculate_annualized_return(strat_returns)
            strat_dd = metrics.calculate_max_drawdown(strat_df['Strategy_Cum_Ret'])
            
            # Comparison Summary
            st.markdown("### Explainable Insight")
            st.info(explainability.summarize_strategy_comparison(strat_ann_ret, bh_ann_ret, strat_dd, bh_dd))
            
            # Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=strat_df.index, y=strat_df['Strategy_Cum_Ret'], name="MA Crossover", line=dict(color=utils.COLORS["primary"])))
            
            bh_cum = (1 + buy_hold_returns).cumprod()
            fig.add_trace(go.Scatter(x=bh_cum.index, y=bh_cum, name="Buy & Hold", line=dict(color=utils.COLORS["benchmark"], dash="dash")))
            
            fig = utils.apply_default_layout(fig, "Cumulative Strategy Returns")
            st.plotly_chart(fig, use_container_width=True)
            
            # Analyst Mode detailed tables
            if mode == "Analyst Mode":
                st.markdown("### Strategy Metrics")
                metrics_df = pd.DataFrame({
                    "Strategy": ["Buy & Hold", "MA Crossover"],
                    "Ann. Return": [f"{bh_ann_ret*100:.2f}%", f"{strat_ann_ret*100:.2f}%"],
                    "Max Drawdown": [f"{bh_dd*100:.2f}%", f"{strat_dd*100:.2f}%"],
                    "Ann. Volatility": [f"{metrics.calculate_annualized_volatility(buy_hold_returns)*100:.2f}%", 
                                       f"{metrics.calculate_annualized_volatility(strat_returns)*100:.2f}%"]
                })
                st.dataframe(metrics_df, hide_index=True, use_container_width=True)

elif page == "Portfolio Optimizer":
    st.title("Portfolio Optimizer")
    
    # Inputs
    default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    tickers = st.multiselect("Select Assets (3 to 8 recommended)", default_tickers + ["NVDA", "TSLA", "META", "BRK-B", "JNJ", "V"], default=default_tickers)
    
    col1, col2 = st.columns(2)
    benchmark = col1.text_input("Benchmark", "SPY").upper()
    objective = col2.selectbox("Optimization Objective", ["Max Sharpe", "Min Volatility"])
    
    if len(tickers) < 2:
        st.warning("Please select at least 2 assets for optimization.")
        st.stop()
        
    if st.button("Run Optimization"):
        with st.spinner("Optimizing..."):
            all_tickers = list(set([t.upper() for t in tickers] + ([benchmark] if benchmark else [])))
            data = data_loader.fetch_stock_data(all_tickers, def_start, def_end)
            
            if not data.empty:
                # Isolate target asset prices, handle missing columns
                valid_tickers = [t for t in tickers if t in data.columns]
                
                if len(valid_tickers) < 2:
                    st.error("Insufficient valid data to run optimization.")
                    st.stop()
                    
                target_prices = data[valid_tickers]
                
                # Perform Optimization
                opt_result = optimizer.optimize_portfolio(target_prices, objective)
                opt_weights = opt_result["weights"]
                opt_ret = opt_result["return"]
                opt_vol = opt_result["volatility"]
                
                # Benchmark return
                bench_ret = None
                if benchmark and benchmark in data.columns:
                    b_daily = metrics.calculate_daily_returns(data[benchmark])
                    bench_ret = metrics.calculate_annualized_return(b_daily)
                
                # Insights
                st.markdown("### Explainable Insight")
                st.info(explainability.summarize_optimization(valid_tickers, opt_weights, opt_ret, bench_ret, opt_vol, objective))
                
                # Visualization
                col_chart, col_metrics = st.columns([1, 1])
                
                with col_metrics:
                    st.markdown(f"**Objective Used:** {objective}")
                    st.metric("Expected Annualized Return", f"{opt_ret*100:.2f}%")
                    st.metric("Expected Volatility", f"{opt_vol*100:.2f}%")
                    st.metric("Expected Sharpe Ratio", f"{opt_result['sharpe']:.2f}")
                    
                with col_chart:
                    # Pie Chart mapping nonzero weights
                    pie_data = pd.DataFrame({"Asset": valid_tickers, "Weight": opt_weights})
                    pie_data = pie_data[pie_data["Weight"] > 0.01] # Filter out tiny weights for clean UI
                    
                    fig_pie = px.pie(pie_data, values='Weight', names='Asset', hole=0.4)
                    fig_pie = utils.apply_default_layout(fig_pie, "Optimized Allocation")
                    st.plotly_chart(fig_pie, use_container_width=True)
                    
                if mode == "Analyst Mode":
                    st.markdown("### Weight Analysis")
                    st.dataframe(pd.DataFrame({"Asset": valid_tickers, "Optimal Weight (%)": [f"{w*100:.2f}%" for w in opt_weights]}), hide_index=True)
