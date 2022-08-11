import streamlit as st
import pandas as pd
from endpoint import financial_metrics_calculation
from datetime import date

time_measures = ['SEC', 'MIN', 'HRS', 'DAY', 'MTH', 'YRS']
time_units = {
    'SEC':['1', '2', '3', '4', '5', '6', '10', '15', '20', '30'],
    'MIN': ['1', '2', '3', '4', '5', '6', '10', '15', '20', '30'],
    'HRS': ['1', '2', '3', '4', '6', '8', '12'],
    'DAY': ['1', '2', '3', '5', '7', '10'],
    'MTH': ['1', '2', '3', '4', '6'],
    'YRS': ['1', '2', '3', '4', '5']
}
col1, col2 = st.columns(2)

with st.form("my_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        coin1 = st.text_input('Coin 1', value="BTC", key=1)
        init_time = st.date_input("Beginning time of compparisson")
        time_measure = st.selectbox('Time measure', time_measures)
    with col2:
        coin2 = st.text_input('Coin 2', value = 'ETH', key=2)
        final_time = st.date_input("Final time of compparisson")
        time_unit = st.selectbox('Time unit', time_units[time_measure])

    submitted = st.form_submit_button("Submit")
    if submitted:
        data = financial_metrics_calculation(coin1, coin2, time_unit, time_measure, init_time.isoformat(), final_time.isoformat())
        st.line_chart(data[0], x='Return')
        st.line_chart(data[1], y='Volatility')
        st.write(data[1])



