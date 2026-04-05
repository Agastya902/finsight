import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

@st.cache_data(show_spinner=False, ttl=3600)  # Cached for 1 hour
def fetch_stock_data(tickers: list, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Fetch historical prices for a list of tickers robustly.
    Prefers 'Adj Close' to account for dividends/splits, but falls back to 'Close' if necessary.
    """
    if not tickers:
        return pd.DataFrame()
        
    valid_tickers = [t.upper().strip() for t in tickers if len(t.strip()) > 0]
    
    if not valid_tickers:
        return pd.DataFrame()
        
    try:
        raw_data = yf.download(valid_tickers, start=start_date, end=end_date, progress=False)
        
        if raw_data.empty:
            st.error("Data ingestion failed: The API returned an empty dataset. Try adjusting the date range.")
            return pd.DataFrame()

        # Handle multi-index columns vs single-index correctly
        if isinstance(raw_data.columns, pd.MultiIndex):
            # Prefer Adj Close, fallback to Close
            if 'Adj Close' in raw_data.columns.levels[0]:
                prices = raw_data['Adj Close']
            elif 'Close' in raw_data.columns.levels[0]:
                prices = raw_data['Close']
            else:
                st.error("Data ingestion failed: Recognized pricing columns not found in payload.")
                return pd.DataFrame()
                
            # If only 1 ticker was requested (but passed inside a list to yfinance), 
            # yfinance sometimes drops the multi-index natively in older versions, 
            # but usually retains it if multiple tickers.
            # Convert series to dataframe if necessary.
            if isinstance(prices, pd.Series):
                prices = prices.to_frame()
                
        else:
            # Single ticker fallback mapping
            if 'Adj Close' in raw_data.columns:
                prices = raw_data[['Adj Close']]
            elif 'Close' in raw_data.columns:
                prices = raw_data[['Close']]
            else:
                st.error("Data ingestion failed: Recognized pricing columns not found.")
                return pd.DataFrame()
                
            # Re-assign the column name to the ticker for consistency
            prices.columns = valid_tickers
            
        # Ensure we only return columns requested
        prices = prices[valid_tickers] if isinstance(prices, pd.DataFrame) else prices.to_frame()

        # Premium data cleaning: forward fill then backward fill
        prices = prices.ffill().bfill()
        
        return prices
    except Exception as e:
        # Avoid dumping stack traces to client view. Provide a polite error.
        st.error(f"Platform Error: Unable to proxy a stable connection for {valid_tickers}. Ensure ticker validity and try again.")
        return pd.DataFrame()

def get_default_date_range():
    """Returns a tuple of (start_date, end_date) representing the last 5 years."""
    end_date = datetime.today()
    start_date = end_date - relativedelta(years=5)
    return start_date, end_date

def validate_ticker(ticker: str) -> bool:
    """Basic sanity check ensuring simple alphanumeric structures prior to fetching."""
    return len(ticker.strip()) > 0 and ticker.isalpha()
