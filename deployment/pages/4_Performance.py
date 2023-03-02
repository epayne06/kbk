import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.metric_cards import style_metric_cards
import plotly_express as px
import pandas as pd

# ---------------------
# --Sidebar Naviation--
# ---------------------
credentials = {"usernames": {}}
authenticator = stauth.Authenticate(credentials, 
    "kbk dashboard", "abcdef", cookie_expiry_days=30)
name, authenticator_status, username = authenticator.login("Login", "main")


st.sidebar.title(f"{name}'s Profile")
authenticator.logout("Logout", "sidebar")

# ----------------
# --Metric Cards--
# ----------------
st.subheader("Acquisition Fund 🏦")
col1, col2, col3 = st.columns(3)
col1.metric(label="Residual Value", value="$20,250,000", delta="$3,250,000")
col2.metric(label="Paid In Capital", value="$2,500,000", delta="$0")
col3.metric(label="Distributions", value="$16,200,000", delta="$0")
style_metric_cards()

#col4, col5 = st.columns(2)
#with col4:
excel_file = "Pie Chart Allocations.xlsx"
df = pd.read_excel(excel_file)
fig = px.pie(df, values="Allocation", names="Portfolio", title="Currrent Ownership")
st.write(fig)

#with col5:
st.subheader("Alliance")
st.write('''Alliance's lastest valuation was 10 million dollars in a round funded by Moody Nolan. 
                This increases our residual value in this company to a total of 1.5 million dollars from 
                an inital investment of 225 thousand dollars. No follow on investments have be issued to Alliance at this point.
                View the attached link for more details [link](https://www.kbkenterprises.net/services).''')
st.subheader("Fintech")
st.write('''Fintech's lastest valuation was 80 million dollars in a round funded by Drive Capital. 
                This increases our residual value in this company to a total of 8 million dollars 
                from an inital investment of 375 thousand dollars and a follow on investment of 375 thousand dollars.
                View the attached link for more details [link](https://techcrunch.com/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAKYetKadWO6zsu1JsCaLzHX6zjRx8qB91znBwmSxfcqIU7joUrkYs7yI3A1lmioPD24XPE78tSHHc2fZOOivIj-gPYE-BWvGYGVFhp7TnAyH6YSu8pSp2YyE1VRP79IsK8_8akFgxqJBQXed92awq3GoNd1sFTyfXOhWEWIvbcsc).''')
st.subheader("General Tech")
st.write('''General Tech's lastest valuation was 4.5 million dollars in a round funded by News Stack Ventures. 
                This increases our residual value in this company to a total of 750 thousand dollars from an inital 
                investment of 150 thousand dollars. 
                View the attached link for more details [link](https://techcrunch.com/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAKYetKadWO6zsu1JsCaLzHX6zjRx8qB91znBwmSxfcqIU7joUrkYs7yI3A1lmioPD24XPE78tSHHc2fZOOivIj-gPYE-BWvGYGVFhp7TnAyH6YSu8pSp2YyE1VRP79IsK8_8akFgxqJBQXed92awq3GoNd1sFTyfXOhWEWIvbcsc)''')
st.subheader("Healthcare Tech")
st.write('''Healthcare Tech's lastest valuation was 26 million dollars in a round funded by Cardinal Health. 
                This increases our residual value in this company to a total of 3.25 million dollars 
                from an inital investment of 225 thousand dollars and a follow on investment of 275 thousday dollars.
                View the attached link for more details [link](https://techcrunch.com/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAKYetKadWO6zsu1JsCaLzHX6zjRx8qB91znBwmSxfcqIU7joUrkYs7yI3A1lmioPD24XPE78tSHHc2fZOOivIj-gPYE-BWvGYGVFhp7TnAyH6YSu8pSp2YyE1VRP79IsK8_8akFgxqJBQXed92awq3GoNd1sFTyfXOhWEWIvbcsc)''')
st.subheader("SaaS Co.")
st.write('''SaaS Co's lastest valuation was 24 million dollars in a round funded by Rev1 Ventures. 
                This increases our residual value in this company to a total of 6 million dollars 
                from an inital investment of 300 thousand dollars and a follow on investment of 300 thousand dollars.
                View the attached link for more details [link](https://techcrunch.com/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAKYetKadWO6zsu1JsCaLzHX6zjRx8qB91znBwmSxfcqIU7joUrkYs7yI3A1lmioPD24XPE78tSHHc2fZOOivIj-gPYE-BWvGYGVFhp7TnAyH6YSu8pSp2YyE1VRP79IsK8_8akFgxqJBQXed92awq3GoNd1sFTyfXOhWEWIvbcsc)''')
st.subheader("Rhino Security")
st.write('''Rhino Security's lastest valuation was $7.5 million dollars in a round funded by KBK Enterprises. 
                This increases our residual value in this company to a total of 750 thousand dollars from 
                an inital investment of 225 thousand dollars. No follow on investments have be issued to Alliance at this point.
                View the attached link for more details [link](https://www.kbkenterprises.net/services).''')
