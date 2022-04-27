# streamlit_app.py
# organizationId = cf39128c-d1f2-4dc8-bc85-73dcf1d3c7f1

from turtle import title
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
def run_query(query, extras = {}):
    with conn.cursor() as cur:
        cur.execute(query, extras)
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
    
organizationId = query_params['organizationId']    
    
    
# try dynamic charts

ordersColumns = run_query('SHOW COLUMNS IN TABLE ORDERS');
# rows = run_query("SELECT ORDER_NUMBER, ORGANIZATION_ID, ORDER_TYPE_ID from ORDERS;")
st.subheader('Columns from orders table')
st.dataframe(ordersColumns)

customerColumns = run_query('SHOW COLUMNS IN TABLE CUSTOMERS');
# rows = run_query("SELECT ORDER_NUMBER, ORGANIZATION_ID, ORDER_TYPE_ID from ORDERS;")
st.subheader('Columns from customer table')
st.dataframe(customerColumns)


orderPaymentsColumns = run_query('SHOW COLUMNS IN TABLE ORDER_PAYMENTS');
# rows = run_query("SELECT ORDER_NUMBER, ORGANIZATION_ID, ORDER_TYPE_ID from ORDERS;")
st.subheader('Columns from order payments table')
st.dataframe(orderPaymentsColumns)





paymentTypesRecords = run_query('select payment_type_name as paymentMethod, count(payment_type_id) as noOfOrders from order_payments group by payment_type_name');
paymentTypesRecordsCount = run_query('select count(*) from order_payments');
st.subheader('Payment Methods')
st.subheader(paymentTypesRecordsCount)
st.subheader("Product Variation Breakdown")

fig1 = px.pie(paymentTypesRecords, values=1, names=0, title='Payment Methods', hole=0.6)
st.plotly_chart(fig1)



totalRevenue = """
SELECT
    CONCAT(round(COALESCE(SUM(
      (orders."TOTAL_GROSS_PRICE")
    ), 0), 2), '') AS "orders.total_revenue_string",
    COUNT(*) AS "orders.orders_count",
    CONCAT(round(AVG(
      (orders."TOTAL_GROSS_PRICE")
    ), 2), '') AS "orders.orders_average_string",
    1=1  AS "orders.total_revenue_block"
FROM "PUBLIC"."ORDERS"
     AS orders
WHERE (orders."ORGANIZATION_ID" ) = %(organizationId)s
"""


totalRevenueRecord = run_query(totalRevenue, {'organizationId':organizationId});
st.subheader('Total Revenue')
st.write(list(totalRevenueRecord[0])[0])


avgGuestSpend = """
SELECT
    CONCAT(round(AVG(
      (orders."TOTAL_GROSS_PRICE")
    ), 2), '') AS "orders.orders_average_string",
    1=1  AS "orders.orders_average_block"
FROM "PUBLIC"."ORDERS"
     AS orders
WHERE (orders."ORGANIZATION_ID" ) IS NOT NULL
FETCH NEXT 500 ROWS ONLY
"""

avgGuestSpendRecord = run_query(avgGuestSpend);
st.subheader('Avg Guest Spend')
st.write(list(avgGuestSpendRecord[0])[0])


productCategoryBreakDownSql = """
SELECT
    order_items."PRODUCT_TYPE_NAME"  AS "order_items.product_type_name",
    COUNT(DISTINCT order_payments."ID" ) AS "order_payments.count"
FROM "PUBLIC"."ORDERS"
     AS orders
LEFT JOIN "PUBLIC"."ORDER_ITEMS"
     AS order_items ON (orders."ID") = (order_items."ORDER_ID")
LEFT JOIN "PUBLIC"."ORDER_PAYMENTS"
     AS order_payments ON (orders."ID") = (order_payments."ORDER_ID")
WHERE LENGTH(order_payments."PAYMENT_TYPE_NAME" ) <> 0 AND (order_payments."PAYMENT_TYPE_NAME" ) IS NOT NULL AND (orders."ORGANIZATION_ID" ) IS NOT NULL
GROUP BY
    1
ORDER BY
    2 DESC
FETCH NEXT 4 ROWS ONLY


"""

productCategoryBreakDownRecords = run_query(productCategoryBreakDownSql);
st.subheader('Product Category Breakdown')
fig2 = px.pie(productCategoryBreakDownRecords, values=1, names=0, title='Product Category Breakdown')
st.plotly_chart(fig2)









topPerformaingProductsSql = """
SELECT
    order_items."PRODUCT_NAME"  AS "order_items.product_name",
    COALESCE(SUM(
      ( order_items."TOTAL_PRICE"  )
    ), 0) AS "order_items.sum_total_price",
    COALESCE(SUM(( order_items."QUANTITY"  ) ), 0) AS "order_items.sum_total_quantity"
FROM "PUBLIC"."ORDERS"
     AS orders
LEFT JOIN "PUBLIC"."ORDER_ITEMS"
     AS order_items ON (orders."ID") = (order_items."ORDER_ID")
WHERE (orders."ORGANIZATION_ID" ) IS NOT NULL
GROUP BY
    1
ORDER BY
    2 DESC
FETCH NEXT 500 ROWS ONLY


"""

topPerformaingProductsRecords = run_query(topPerformaingProductsSql);
st.subheader('Top Performing products by revenue & qty sold')
st.dataframe(topPerformaingProductsRecords)

fig3 = px.histogram(topPerformaingProductsRecords, x=0, y=1,
             color=2, barmode='group',
             height=400)


# fig2 = px.pie(productCategoryBreakDownRecords, values=1, names=0, title='Product Category Breakdown')
st.plotly_chart(fig3)















weekOnWeekSalesSql = """
-- raw sql results do not include filled-in values for 'orders.created_date'


SELECT
    (TO_CHAR(TO_DATE(CONVERT_TIMEZONE('UTC', 'Australia/Melbourne', CAST(CAST(orders."CREATED_AT" AS TIMESTAMP_NTZ)  AS TIMESTAMP_NTZ))), 'YYYY-MM-DD')) AS "orders.created_date",
    COALESCE(SUM(
      ( order_items."TOTAL_PRICE"  )
    ), 0) AS "order_items.sum_total_price"
FROM "PUBLIC"."ORDERS"
     AS orders
LEFT JOIN "PUBLIC"."ORDER_ITEMS"
     AS order_items ON (orders."ID") = (order_items."ORDER_ID")
WHERE (orders."ORGANIZATION_ID" ) IS NOT NULL
GROUP BY
    (TO_DATE(CONVERT_TIMEZONE('UTC', 'Australia/Melbourne', CAST(CAST(orders."CREATED_AT" AS TIMESTAMP_NTZ)  AS TIMESTAMP_NTZ))))
ORDER BY
    1 DESC
FETCH NEXT 500 ROWS ONLY

"""

weekOnWeekSalesRecords = run_query(weekOnWeekSalesSql);
st.subheader('Week on Week Sales')
st.dataframe(weekOnWeekSalesRecords)
fig4 = px.line(weekOnWeekSalesRecords, x=0, y=1)
st.plotly_chart(fig4)
