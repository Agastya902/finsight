import numpy as np
import pandas as pd

TRADING_DAYS = 252

def calculate_daily_returns(prices: pd.Series) -> pd.Series:
    """Calculate simple daily returns."""
    return prices.pct_change().dropna()

def calculate_annualized_return(daily_returns: pd.Series) -> float:
    """Calculate compound annualized return."""
    if len(daily_returns) == 0: return 0.0
    cumulative_return = (1 + daily_returns).prod()
    years = len(daily_returns) / TRADING_DAYS
    return (cumulative_return ** (1 / years)) - 1 if years > 0 else 0.0

def calculate_annualized_volatility(daily_returns: pd.Series) -> float:
    """Calculate annualized volatility from daily returns."""
    if len(daily_returns) == 0: return 0.0
    return daily_returns.std() * np.sqrt(TRADING_DAYS)

def calculate_sharpe_ratio(daily_returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """Calculate annualized Sharpe Ratio."""
    ann_ret = calculate_annualized_return(daily_returns)
    ann_vol = calculate_annualized_volatility(daily_returns)
    if ann_vol == 0: return 0.0
    return (ann_ret - risk_free_rate) / ann_vol

def calculate_max_drawdown(prices: pd.Series) -> float:
    """Calculate maximum drawdown from peak."""
    if len(prices) == 0: return 0.0
    rolling_max = prices.cummax()
    drawdown = (prices - rolling_max) / rolling_max
    return drawdown.min()

def calculate_cumulative_returns(daily_returns: pd.Series) -> pd.Series:
    """Calculate cumulative return series starting at 1.0."""
    return (1 + daily_returns).cumprod()
