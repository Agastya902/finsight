import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

@st.cache_data(show_spinner=False)
def fetch_stock_data(tickers: list, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Fetch historical adjusted close prices for a list of tickers.
    Uses st.cache_data to cache the result across Streamlit reruns.
    """
    if not tickers:
        return pd.DataFrame()
        
    try:
        # yfinance returns a DataFrame. If multiple tickers, columns are MultiIndex.
        # Use auto_adjust=False and get 'Adj Close' to be accurate for returns.
        raw_data = yf.download(tickers, start=start_date, end=end_date, progress=False)
        
        if raw_data.empty:
            return pd.DataFrame()
            
        # If multiple tickers, pick 'Adj Close', which will be a DataFrame of prices
        if isinstance(raw_data.columns, pd.MultiIndex):
            prices = raw_data['Adj Close']
        else:
            # Single ticker, raw_data['Adj Close'] is a Series
            prices = raw_data[['Adj Close']]
            prices.columns = tickers
            
        # Clean missing values: forward fill then backward fill
        prices = prices.ffill().bfill()
        return prices
    except Exception as e:
        st.warning(f"Error fetching data: {str(e)}")
        return pd.DataFrame()

def get_default_date_range():
    """Returns a tuple of (start_date, end_date) representing the last 5 years."""
    end_date = datetime.today()
    start_date = end_date - relativedelta(years=5)
    return start_date, end_date

def validate_ticker(ticker: str) -> bool:
    """Simple validation to ensure ticker is likely valid before complex fetching."""
    return len(ticker.strip()) > 0 and ticker.isalpha()
