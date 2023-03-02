import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_extras.chart_container import chart_container
from streamlit_extras.altex import line_chart
import plotly, plotly.graph_objects as go

# --------------------------------
# --Sidebar User Name and Logout--
# --------------------------------
credentials = {"usernames": {}}
authenticator = stauth.Authenticate(credentials, 
    "kbk dashboard", "abcdef", cookie_expiry_days=30)
name, authenticator_status, username = authenticator.login("Login", "main")
st.sidebar.title(f"{name}'s Profile")
authenticator.logout("Logout", "sidebar")

# --------------------------------
# --Code to call portfolio KPI's--
# --------------------------------

st.subheader("Financial Reporting 📈")
st.write("_The only two company's available now are ALLIANCE CONSTRUCTION and RHINO SECURITY (case sensitive)_")
portfolio_company = st.text_input('Portfolio Company', value="ALLIANCE CONSTRUCTION")
excel_file = 'KBK Protfolio Data.xlsx'
df = pd.read_excel(excel_file, sheet_name=portfolio_company)
with chart_container(df):
    st.write(f"Here are the financials of {portfolio_company}")
    st.area_chart(df)

net_profit = df['Total Cumulative'].subtract(df['COGS'])
st.write(f"{portfolio_company}'s net profit per month")
st.bar_chart(net_profit)


