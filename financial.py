import pandas as pd
import numpy as np
from scipy.optimize import minimize


def calculate_return(crypto_data: pd.DataFrame):
    crypto_data["returns"] = crypto_data["price"].pct_change()*100
    return crypto_data


def calculate_volatility(crypto_data: pd.DataFrame):
    crypto_data["volatility"] = crypto_data["returns"].rolling(30).std()
    return crypto_data


def calculate_complete_return(crypto_data: pd.DataFrame):
    crypto_data = crypto_data/100
    complete_return = (1+crypto_data[1:]).cumprod() - 1
    return complete_return.iloc[-1]


def calculate_complete_volatility(crypto_data: pd.DataFrame):
    crypto_data = crypto_data/100
    complete_volatility = crypto_data.std()
    return complete_volatility


def portfolio_return(weights, returns):
    return weights.T @ returns


def portfolio_vol(weights, covmat):
    return (weights.T @ covmat @ weights)**0.5


def annualized_rets(returns, periods_per_year):
    compound_growth = (1+returns).prod()
    n_periods = returns.shape[0]
    return compound_growth**(periods_per_year/n_periods) - 1


def optimal_weights(n_points, er, cov):
    target_rs = np.linspace(er.min(), er.max(), n_points)
    weights = [minimize_vol(target_return, er, cov) for target_return in target_rs]
    return weights


def minimize_vol(target_return, er, cov):
    n = er.shape[0]
    init_guess = np.repeat(1/n, n)
    bounds = ((0.0, 1.0),)*n
    return_is_target = {
        'type': 'eq',
        'args': (er,),
        'fun': lambda weights, er: target_return - portfolio_return(weights, er)
    }
    weights_sum_to_1 = {
        'type': 'eq',
        'fun': lambda weights: np.sum(weights) - 1
    }
    results = minimize(
        portfolio_vol,
        init_guess,
        args=(cov,),
        method="SLSQP",
        options={'disp': False},
        constraints=(return_is_target, weights_sum_to_1),
        bounds=bounds
    )

    return results.x


def msr(risk_free_rate, er, cov):
    n = er.shape[0]
    init_guess = np.repeat(1/n, n)
    bounds = ((0.0, 1.0),)*n
    weights_sum_to_1 = {
        'type': 'eq',
        'fun': lambda weights: np.sum(weights) - 1
    }

    def neg_sharpe_ratio(weights, riskfree_rate, er, cov):
        r = portfolio_return(weights, er)
        vol = portfolio_vol(weights, cov)
        return -(r - riskfree_rate)/vol

    results = minimize(
        neg_sharpe_ratio,
        init_guess,
        args=(risk_free_rate, er, cov),
        method="SLSQP",
        # options={'disp': False},
        constraints=(weights_sum_to_1),
        bounds=bounds
    )

    return results.x


def gmv(cov):
    n = cov.shape[0]
    return msr(0, np.repeat(1, n), cov)
