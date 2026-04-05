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

def generate_monte_carlo_frontier(mean_returns: pd.Series, cov_matrix: pd.DataFrame, num_portfolios: int = 2500) -> dict:
    """Generates thousands of randomized portfolios to construct the mathematical efficient frontier scatter."""
    num_assets = len(mean_returns)
    results = np.zeros((3, num_portfolios))
    weights_record = []
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        p_ret, p_vol = portfolio_performance(weights, mean_returns, cov_matrix)
        results[0,i] = p_vol
        results[1,i] = p_ret
        results[2,i] = p_ret / p_vol if p_vol > 0 else 0  # Sharpe
        
    return {
        "volatility": results[0,:],
        "returns": results[1,:],
        "sharpe": results[2,:],
        "weights": weights_record
    }

def optimize_portfolio(prices: pd.DataFrame, objective: str = "Max Sharpe") -> dict:
    """
    Optimizes portfolio weights according to the specified institutional objective.
    Returns dict containing weights, return, volatility, sharpe ratio, and the frontier array.
    """
    num_assets = len(prices.columns)
    mean_returns = calculate_expected_returns(prices)
    cov_matrix = calculate_covariance_matrix(prices)

    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})
    bounds = tuple((0.0, 1.0) for asset in range(num_assets))
    
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
    weights = weights / np.sum(weights)
    
    p_ret, p_vol = portfolio_performance(weights, mean_returns, cov_matrix)
    p_sharpe = p_ret / p_vol if p_vol > 0 else 0
    
    # Generate the frontier background
    frontier_data = generate_monte_carlo_frontier(mean_returns, cov_matrix, num_portfolios=2500)
    
    return {
        "weights": weights.tolist(),
        "return": float(p_ret),
        "volatility": float(p_vol),
        "sharpe": float(p_sharpe),
        "frontier": frontier_data,
        "mean_returns": mean_returns,
        "cov_matrix": cov_matrix
    }

def calculate_custom_portfolio(prices: pd.DataFrame, weights: list) -> dict:
    """Calculate performance metrics for a manually constructed portfolio."""
    mean_returns = calculate_expected_returns(prices)
    cov_matrix = calculate_covariance_matrix(prices)
    weights_arr = np.array(weights)
    p_ret, p_vol = portfolio_performance(weights_arr, mean_returns, cov_matrix)
    p_sharpe = p_ret / p_vol if p_vol > 0 else 0
    return {
        "return": float(p_ret),
        "volatility": float(p_vol),
        "sharpe": float(p_sharpe),
        "mean_returns": mean_returns,
        "cov_matrix": cov_matrix
    }
