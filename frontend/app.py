from http.client import responses
from add_update_tab import add_update_tab
import streamlit as st
from datetime import datetime
import requests
from analytics_monthwise_ui import AnalyticsUiMonthWise
from analytics_category_ui import AnalyticsUiCategoryWise
API_URL = 'http://localhost:8000'
st.title('Expense Tracking System')

tab1, tab2, tab3 = st.tabs(['Add/Update', 'Analytics Category Wise', 'Analytics Month Wise'])
with tab1:
    add_update_tab()
with tab2:
    tabObj = AnalyticsUiCategoryWise()
    tabObj.analytics_tab()
with tab3:
    tabObj = AnalyticsUiMonthWise()
    tabObj.analytics_tab()






