# streamlit_app.py

import streamlit as st
import snowflake.connector
import plotly.express as px
import altair as alt
import numpy as np
import pandas as pd

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# rows = run_query("SELECT * from ORDERS;")

# Print results.
# for row in rows:
#     st.write(f"{row[0]} has a :{row[1]}:")

st.write('Product Overview for Last Week (wc 07/02/2022)')

revenueCol, avgGuestSpendCol = st.columns(2)


with revenueCol:
    st.write('Total Revenue')
    st.subheader('$6049.00')
    st.write('230 sales at an average sale total of $18.18')

with avgGuestSpendCol:
    st.write('Avg. Guest Spend')
    st.subheader('$26.30')
    st.write('No guest tracking data recorded!')


st.write('Top Performing Products by Revenue & Qty Sold')

# revenueCol.metric("Total Revenue", "$6049", "230 sales at an average sale total of $18.18")
# avgGuestSpendCol.metric("Avg. Guest Spend", "$26.30", "No guest tracking recorded")

    
    

productVariantionCol, popularPaymentMethodsCol = st.columns(2)

with productVariantionCol:
    # ploty
    data_frame = {'Small': 4500,
                'Regular': 2500,
                'Large': 1053,
    }
    
    fig = px.pie(
        hole = 0.6,
        labels = data_frame.values(),
        names = data_frame.keys(),
    )
    
    st.subheader("Product Variation Breakdown")
    st.plotly_chart(fig)
    


with popularPaymentMethodsCol:
    st.subheader("Popular Payment Methods")
    
    
    
df = pd.DataFrame(
     np.random.randn(200, 3),
     columns=['a', 'b', 'c'])

c = alt.Chart(df).mark_circle().encode(
     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.altair_chart(c, use_container_width=True)



query_params = st.experimental_get_query_params()
query_params
    
    