from utils import *
from financial import *
import pandas as pd
import streamlit as st
import plotly.express as px
import datetime



def financial_metrics_calculation(info_coin_a, info_coin_b, initial_time, final_time):
    '''
    Calculates the return and the volatility of two assets

    Parameters:
    - info_coin_a (Panda Dataframe) : Historical data of the first asset, can be fetched from cryptoCompare API
    - info_coin_b (Panda Dataframe) : Historical data of the second asset, can be fetched from cryptoCompare API
    - initial_time (String) : Beginning of comparisson. Date formatted as yyyy-mm-dd
    - final_time (String) : End of comparisson. Date formatted as yyyy-mm-dd

    Return:
    - Panda dataframe: Dataframe of the daily returns calculated for the two assets.
    - Panda dataframe: Dataframe of the assets volatilities per day. The volatility is calculated as the standard deviation in the last 30 days of the assets' returns.
    '''
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
    '''
    Calculates the complete return and volatility of two assets from the beginning time of comparison until the end.

    Parameters:
    - returns_df (Panda Dataframe) : Historical data of the daily returns for two assets. Can be obtained from financial_metrics_calculation

    Return:
    - Panda dataframe: Dataframe with the complete return and volatility of the two assets, from the beginning time of comparison until the end.
    '''
    complete_return = calculate_complete_return(returns_df)
    complete_volatility = calculate_complete_volatility(returns_df)
    comparison_data = pd.concat([complete_return, complete_volatility], axis=1)
    comparison_data = comparison_data*100
    comparison_data = comparison_data.T
    comparison_data.index = ["Return", "Volatility"]

    return comparison_data


def global_minimum_variance(returns_df):
    '''
    Applies Global Minimum Variance to the selected asset portfolio minimizing volatility and maximizing return 

    Parameters:
    - returns_df (Panda Dataframe) : Historical data of the daily returns for two assets. Can be obtained from financial_metrics_calculation

    Return:
    - Python list containing 4 elements: 
        -Panda dataframe with the returns and volatility for possible weight distributions
        -Panda dataframe with the weighted dristibution of the optimized portfolio 
        -Float Return of the gmv point
        -Float Volatility of the gmv point
    '''

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

def st_ui():

    with st.form("my_form"):
        col1, col2 = st.columns(2)

        with col1:
            coin1 = st.text_input('Asset 1', value="ADA", key=1)
            init_time = st.date_input("Beginning time of comparison",  pd.Timestamp.now() - pd.Timedelta(30, "d"))
        with col2:
            coin2 = st.text_input('Asset 2', value='APE', key=2)
            final_time = st.date_input("Final time of comparison", pd.Timestamp.now())

        submitted = st.form_submit_button("Submit")

    if submitted:
        data = fetch_data(coin1, coin2, init_time, final_time)

        st.subheader('Total Volatility and Return')
        comparison_data = financial_data_comparison(data[0])
        comparison_data.iloc[:, 0] = comparison_data.iloc[:, 0].map("{:,.4f}%".format)
        comparison_data.iloc[:, 1] = comparison_data.iloc[:, 1].map("{:,.4f}%".format)
        st.table(comparison_data)

        st.subheader('Assets return')
        fig_return = px.line(data[0])
        fig_return.update_layout(yaxis_title="Return")
        fig_return.update_layout(xaxis_title="Date")
        fig_return['data'][0]['line']['color'] = "#332FD0"
        fig_return['data'][1]['line']['color'] = "#D89216"
        st.plotly_chart(fig_return)

        st.subheader("Assets Volatility")
        fig_volatility = px.line(data[1])
        fig_volatility.update_layout(yaxis_title="Volatility")
        fig_volatility.update_layout(xaxis_title="Date")
        fig_volatility['data'][0]['line']['color'] = "#332FD0"
        fig_volatility['data'][1]['line']['color'] = "#D89216"
        st.plotly_chart(fig_volatility)

        st.subheader("Global Minimum Variance Optimization")
        [ef, w_gmv, r_gmv, vol_gmv] = global_minimum_variance(data[0])
        fig_gmv = px.line(x=ef["Volatility"], y=ef["Returns"])
        fig_gmv.add_scatter(x=[vol_gmv], y=[r_gmv], name="GMV Point")
        fig_gmv.update_layout(yaxis_title="Return")
        fig_gmv.update_layout(xaxis_title="Volatility")
        st.plotly_chart(fig_gmv)

        w_gmv.iloc[:, 0] = w_gmv.iloc[:, 0].map("{:,.4f}%".format)
        w_gmv.iloc[:, 1] = w_gmv.iloc[:, 1].map("{:,.4f}%".format)
        st.subheader('Weighted distribution')
        st.table(w_gmv)

        # st.write(data[1])

@st.cache
def fetch_data(coin1, coin2, init_time, final_time):
    info_coin1 = get_data(coin1)
    info_coin2 = get_data(coin2)
    return financial_metrics_calculation(info_coin1, info_coin2, init_time, final_time)



if __name__ == "__main__":
    st_ui()

