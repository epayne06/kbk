import streamlit as st
import pandas as pd
import openpyxl
import plotly
from streamlit_extras.app_logo import add_logo
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

st.set_option('browser.serverFileWatcherType', 'none')

# --------------------------
# --Page tab configuration--
# --------------------------
st.set_page_config(
        page_title="KBK Dashboard",
        page_icon="💻",
)

# -----------------------
# --User Authentication--
# -----------------------
names = ["Evan Spencer",  "Keith Key"]
usernames = ["espencer",  "kkey"]

credentials = {"usernames": {}}

file_path = Path(__file__).parent / "hashed_pw_kbk.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

for uname, name, pwd in zip(usernames, names, hashed_passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})

authenticator = stauth.Authenticate(credentials, 
    "kbk dashboard", "abcdef", cookie_expiry_days=30)

name, authenticator_status, username = authenticator.login("Login", "main")

if authenticator_status == False:
    st.error("Username/password is incorrect")

if authenticator_status == None:
    st.warning("Please enter your username and password")

if authenticator_status == True:
    # -----------
    # --Sidebar--
    # -----------
    st.sidebar.title(f"Welcome {name}")
    authenticator.logout("Logout", "sidebar")

    # ---------------------
    # --Application Title--
    # ---------------------
    
    st.title("KBK Portfolio Dashboard")
    st.subheader("Crafted to optimize the company's portfolio of assets")
    st.write('''One important note is that the Financial Modeling page is \
                the only production ready page to intake and export actionable \
                data. The Portfolio and Performance pages can be brought up to \
                speed at a moment's notice with real data via an Excel \
                spreadsheet. For now, however, these two pages are populated \
                with hypothetical data parameters to illustrate the proof of concept.''')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(':red[Operating instructions for Financial Modeling]')

    with col2:
        st.write('''There two-way to upload and compare real estate data for \
                    financial due diligence. First, navigate to :red[Financial Modeling]\
                    in the side bar. Once you're there, you'll notice a dropdown titled\
                    Data Entry Options. If you'd like to :red[upload a CSV] of a single or \
                    list of properties for evaluation, you'll need to follow the prompt \
                    to drag and drop a file. Before tapping the Process CSV button, \
                    make sure your file has the format illustrated below. ''')
        
    format_file = 'CSV_file_format.csv'
    df = pd.read_csv(format_file)
    st.write(df)
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("")
    with col4:
        st.write('''When ready, tap Process CSV to perform the due diligence \
                    calculation function. Here you'll be able to see a table of the \
                    inputs and outputs.''')
        
    col5, col6 = st.columns(2)
    with col5:
        st.write('''If you like to manually enter data for the internal modeling system \
                    to perform due diligence on, select :red[User Input] from the Data Entry Options \
                    dropdown in the sidebar and follow the prompt.''')

    st.subheader("_This system is fully customizable and has more in store for the future_")