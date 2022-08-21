from utils import process_date
from financial import *
import pandas as pd


def financial_metrics_calculation(info_coin_a, info_coin_b, initial_time, final_time):

    start_time = process_date(initial_time)
    end_time = process_date(final_time)

    info_coin_a = calculate_return(info_coin_a)
    info_coin_a = calculate_volatility(info_coin_a)
    info_coin_a = info_coin_a.loc[start_time:end_time]

    info_coin_b = calculate_return(info_coin_b)
    info_coin_b = calculate_volatility(info_coin_b)
    info_coin_b = info_coin_b.loc[start_time:end_time]

    returns_df = pd.DataFrame([])
    returns_df[info_coin_a.columns.name] = info_coin_a["returns"]
    returns_df[info_coin_b.columns.name] = info_coin_b["returns"]

    volatility_df = pd.DataFrame([])
    volatility_df[info_coin_a.columns.name] = info_coin_a["volatility"]
    volatility_df[info_coin_b.columns.name] = info_coin_b["volatility"]

    return returns_df, volatility_df


def financial_data_comparison(returns_df):
    complete_return = calculate_complete_return(returns_df)
    complete_volatility = calculate_complete_volatility(returns_df)
    comparison_data = pd.concat([complete_return, complete_volatility], axis=1)
    comparison_data = comparison_data*100
    comparison_data = comparison_data.T
    comparison_data.index = ["Return", "Volatility"]

    return comparison_data


def global_minimum_variance(returns_df):

    annualized_returns = annualized_rets(returns_df / 100, 365)
    covariance = (returns_df / 100).cov()
    weights = optimal_weights(25, annualized_returns, covariance)

    rets = [portfolio_return(w, annualized_returns) for w in weights]
    vols = [portfolio_vol(w, covariance) for w in weights]

    ef = pd.DataFrame({"Returns": rets, "Volatility": vols})

    w_gmv = gmv(covariance)
    r_gmv = portfolio_return(w_gmv, annualized_returns)
    vol_gmv = portfolio_vol(w_gmv, covariance)
    w_gmv = pd.DataFrame([w_gmv*100], index=["Weights"], columns=returns_df.columns)

    return [ef, w_gmv, r_gmv, vol_gmv]
