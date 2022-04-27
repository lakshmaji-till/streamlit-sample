import streamlit as st
import snowflake.connector


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_db():
    return snowflake.connector.connect(**st.secrets["snowflake"])


# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(_conn, query, extras = {}):
    with _conn.cursor() as cur:
        cur.execute(query, extras)
        return cur.fetchall()