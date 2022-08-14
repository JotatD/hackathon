import streamlit as st
import pandas as pd
import plotly.express as px
from endpoint import financial_metrics_calculation
import datetime

time_measures = ['SEC', 'MIN', 'HRS', 'DAY', 'MTH', 'YRS']
time_units = {
    'SEC':['1', '2', '3', '4', '5', '6', '10', '15', '20', '30'],
    'MIN': ['1', '2', '3', '4', '5', '6', '10', '15', '20', '30'],
    'HRS': ['1', '2', '3', '4', '6', '8', '12'],
    'DAY': ['1', '2', '3', '5', '7', '10'],
    'MTH': ['1', '2', '3', '4', '6'],
    'YRS': ['1', '2', '3', '4', '5']
}

@st.cache
def fetch_data(coin1, coin2, time_unit, time_measure, init_time, final_time):
    return financial_metrics_calculation(coin1, coin2, time_unit, time_measure, init_time.isoformat(), final_time.isoformat())

with st.form("my_form"):
    col1, col2 = st.columns(2)

    with col1:
        coin1 = st.text_input('Coin 1', value="BTC", key=1)
        init_time = st.date_input("Beginning time of compparisson",  datetime.date(2022, 5, 1))
        time_measure = st.selectbox('Time measure', time_measures, index=3)
    with col2:
        coin2 = st.text_input('Coin 2', value = 'ETH', key=2)
        final_time = st.date_input("Final time of compparisson", datetime.date(2022, 8, 1))
        time_unit = st.selectbox('Time unit', time_units[time_measure], index=0)
    submitted = st.form_submit_button("Submit")

if submitted:
    data = fetch_data(coin1, coin2, time_unit, time_measure, init_time, final_time)
    fig_return = px.line(data[0], title="Return of coins")
    fig_return.update_layout(yaxis_title="Return")
    fig_return['data'][0]['line']['color']="#332FD0"
    fig_return['data'][1]['line']['color']="#D89216"
    st.plotly_chart(fig_return)
    fig_volatility = px.line(data[1], title="Volatility of coins")
    fig_volatility.update_layout(yaxis_title="Volatility")
    fig_volatility['data'][0]['line']['color']="#332FD0"
    fig_volatility['data'][1]['line']['color']="#D89216"
    st.plotly_chart(fig_volatility)
    st.write(data[1])




