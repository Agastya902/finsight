import numpy as np
import pandas as pd
from scipy.optimize import minimize
from metrics import TRADING_DAYS

def calculate_expected_returns(prices: pd.DataFrame) -> pd.Series:
    """Calculate mean historical annualized returns."""
    daily_returns = prices.pct_change().dropna()
    return daily_returns.mean() * TRADING_DAYS

def calculate_covariance_matrix(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate annualized covariance matrix of daily returns."""
    daily_returns = prices.pct_change().dropna()
    return daily_returns.cov() * TRADING_DAYS

def portfolio_performance(weights: np.ndarray, mean_returns: pd.Series, cov_matrix: pd.DataFrame) -> tuple:
    """Calculates annualized portfolio return and volatility."""
    returns = np.sum(mean_returns * weights)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, volatility

def min_variance_objective(weights: np.ndarray, mean_returns: pd.Series, cov_matrix: pd.DataFrame) -> float:
    return portfolio_performance(weights, mean_returns, cov_matrix)[1]

def negative_sharpe_objective(weights: np.ndarray, mean_returns: pd.Series, cov_matrix: pd.DataFrame, risk_free_rate: float = 0.0) -> float:
    p_ret, p_vol = portfolio_performance(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_vol

def optimize_portfolio(prices: pd.DataFrame, objective: str = "Max Sharpe") -> dict:
    """
    Optimizes portfolio weights according to the specified objective.
    Returns dict containing weights, return, volatility, and sharpe ratio.
    """
    num_assets = len(prices.columns)
    mean_returns = calculate_expected_returns(prices)
    cov_matrix = calculate_covariance_matrix(prices)

    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})
    bounds = tuple((0.0, 1.0) for asset in range(num_assets))
    
    # Initial guess (equal weighting)
    init_guess = num_assets * [1.0 / num_assets,]

    if objective == "Max Sharpe":
        result = minimize(negative_sharpe_objective, init_guess, args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    elif objective == "Min Volatility":
        result = minimize(min_variance_objective, init_guess, args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    else:
        raise ValueError(f"Unknown objective: {objective}")

    weights = np.round(result.x, 4)
    # Ensure they sum to exactly 1 (accounting for rounding errors)
    weights = weights / np.sum(weights)
    
    p_ret, p_vol = portfolio_performance(weights, mean_returns, cov_matrix)
    p_sharpe = p_ret / p_vol if p_vol > 0 else 0
    
    return {
        "weights": weights.tolist(),
        "return": float(p_ret),
        "volatility": float(p_vol),
        "sharpe": float(p_sharpe)
    }
