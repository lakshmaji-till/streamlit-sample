# streamlit_app.py
# organizationId = cf39128c-d1f2-4dc8-bc85-73dcf1d3c7f1

from turtle import title
import streamlit as st
import snowflake.connector
import plotly.express as px
import altair as alt
import numpy as np
import pandas as pd
from queries.exec import run_query, init_db
from queries.input import getOrganizationId


conn = init_db()

organizationId = getOrganizationId()    
st.write('query_params: organizationId',organizationId)
    
    
# totalRevenue = """
#                     SELECT 
#                         tt.BOOKING_DATE as "Date_Time",
#                         tt.MAIN_AMOUNT as "Transaction Value",
#                         COALESCE(tt.PAYABLE, 0) as "Payouts"
#                     FROM 
#                         TRANSACTIONS_TEST tt 
#                     LEFT JOIN 
#                         ORGANIZATIONS_MERCHANTS om 
#                     ON 
#                         om.MERCHANT_ID = tt.MERCHANT_ACCOUNT 
#                     WHERE 
#                         om.ORGANIZATION_ID = %(organizationId)s;
# """
# totalRevenue = """
#                     SELECT 0 as \"Date\",
#                           0 as \"Time\",
#                           BOOKING_DATE as \"Date Time\",
#                           PSP_REFERENCE as \"PSP #\",
#                           MERCHANT_REFERENCE as \"Merchant #\",
#                           PAYMENT_METHOD as \"Payment Method\",
#                           MAIN_CURRENCY as \"Currency\",
#                           MAIN_AMOUNT as \"Transaction Value\",
#                           0 as \"Total Fees\",
#                           COALESCE(PROCESSING_FEE, 0) as \"Processing Fee\",
#                           COALESCE(COMMISSION, 0) as \"Commission\",
#                           COALESCE(INTERCHANGE, 0) as \"Interchange\",
#                           COALESCE(SCHEME_FEES, 0) as \"Scheme Fees\",
#                           COALESCE(MARKUP, 0) as \"Markup\",
#                           RECORD_TYPE as \"Status\",
#                           COALESCE(PAYABLE, 0) as \"Paid to You\"
#                     FROM TRANSACTIONS_TEST tt
#                     LEFT JOIN 
#                         ORGANIZATIONS_MERCHANTS om 
#                     ON 
#                         om.MERCHANT_ID = tt.MERCHANT_ACCOUNT 
#                     WHERE 
#                         om.ORGANIZATION_ID = %(organizationId)s;
# """
totalRevenue = """
                    SELECT CREATION_DATE as \"Created Date\",
                          BATCH_CLOSED_DATE as \"Closed Date\",
                          TIMEZONE as \"Time Zone\",
                          COALESCE(TERMINAL_ID, 'N/A') as \"Terminal ID\",
                          TRANSACTIONS as \"Transaction Count\",
                          COALESCE(NET_DEBIT, 0) - COALESCE(NET_CREDIT, 0) as \"Net Balance\",
                          NET_CURRENCY as \"Currency\",
                          COALESCE(BANK_COMMISSION, 0) as \"Bank Fees\",
                          JOURNAL_TYPE as \"Journal Type\",
                          COALESCE(PAYMENT_METHOD, 'N/A') as \"Payment Method\",
                          BATCH_NUMBER as \"Batch Number\",
                          COALESCE(DCC_MARKUP, 0) as \"DCC Markup\",
                          COUNTRY_CODE as \"Country\",
                          EXCHANGE_RATE as \"Exchange Rate\"
                    FROM SETTLEMENTS_TEST st
                    LEFT JOIN 
                        ORGANIZATIONS_MERCHANTS om 
                    ON 
                        om.MERCHANT_ID = st.MERCHANT_ACCOUNT 
                    WHERE 
                        om.ORGANIZATION_ID = %(organizationId)s;
"""


totalRevenueRecord = run_query(conn, totalRevenue, {'organizationId':organizationId});
st.subheader('Total Revenue')
st.write(totalRevenueRecord)
