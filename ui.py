import streamlit as st
import plotly.express as px
from endpoint import financial_metrics_calculation, financial_data_comparison, global_minimum_variance
from utils import get_data
import datetime


@st.cache
def fetch_data(coin1, coin2, init_time, final_time):
    info_coin1 = get_data(coin1)
    info_coin2 = get_data(coin2)
    return financial_metrics_calculation(info_coin1, info_coin2, init_time, final_time)


def create_graphs():

    with st.form("my_form"):
        col1, col2 = st.columns(2)

        with col1:
            coin1 = st.text_input('Asset 1', value="BTC", key=1)
            init_time = st.date_input("Beginning time of comparison",  datetime.date(2022, 5, 1))
        with col2:
            coin2 = st.text_input('Asset 2', value='ETH', key=2)
            final_time = st.date_input("Final time of comparison", datetime.date(2022, 8, 1))

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


if __name__ == "__main__":

    create_graphs()
