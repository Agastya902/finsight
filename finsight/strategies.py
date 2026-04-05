import pandas as pd
import numpy as np

def run_buy_and_hold(prices: pd.Series) -> pd.Series:
    """
    Calculates the Daily Return and Cumulative Return of a buy and hold strategy.
    Returns the cumulative return series starting from 1.0.
    """
    if len(prices) == 0: return pd.Series()
    daily_returns = prices.pct_change().fillna(0)
    return (1 + daily_returns).cumprod()

def run_moving_average_crossover(prices: pd.Series, short_window: int = 50, long_window: int = 200) -> pd.DataFrame:
    """
    Simulates a Moving Average Crossover strategy.
    Go long (1) when short MA > long MA, otherwise flat (0) or short (-1).
    For a standard equity MVP, we assume long-only (1) or cash (0).
    Returns a dataframe containing prices, MAs, and Strategy Cumulative Returns.
    """
    if len(prices) < long_window:
        # Not enough data for crossover, fallback to Buy and Hold
        b_h = run_buy_and_hold(prices)
        df = pd.DataFrame({'Price': prices, 'SMA_Short': np.nan, 'SMA_Long': np.nan, 'Strategy_Cum_Ret': b_h})
        return df
        
    df = pd.DataFrame(index=prices.index)
    df['Price'] = prices
    df['Daily_Return'] = prices.pct_change().fillna(0)
    
    # Calculate Moving Averages
    df['SMA_Short'] = df['Price'].rolling(window=short_window, min_periods=1).mean()
    df['SMA_Long'] = df['Price'].rolling(window=long_window, min_periods=1).mean()
    
    # Generate Signals (0 or 1)
    # Shift signal by 1 day to represent trading at the NEXT day's close
    df['Signal'] = np.where(df['SMA_Short'] > df['SMA_Long'], 1, 0)
    df['Position'] = df['Signal'].shift(1).fillna(0) # start flat
    
    # Calculate Strategy Return
    df['Strategy_Daily_Return'] = df['Position'] * df['Daily_Return']
    df['Strategy_Cum_Ret'] = (1 + df['Strategy_Daily_Return']).cumprod()
    
    return df
