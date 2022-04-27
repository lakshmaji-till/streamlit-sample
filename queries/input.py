
import streamlit as st

query_params = st.experimental_get_query_params()

def getOrganizationId():
    st.write('query_params', query_params)
    return query_params['organizationId']