import pandas as pd
import sys
import streamlit as st
import streamlit_authenticator as stauth
import plotly_express as px

# ---------------------
# --Sidebar Naviation--
# ---------------------
credentials = {"usernames": {}}
authenticator = stauth.Authenticate(credentials, 
    "kbk dashboard", "abcdef", cookie_expiry_days=30)
name, authenticator_status, username = authenticator.login("Login", "main")


st.sidebar.title(f"{name}'s Profile")

# Get the monthly mortgage payment from mortgage details
def get_mortgage_pmt(principal, irate, term):
    irate = irate / 1200 # interest rate percentage / 12 monthly payments
    return float(principal) * float((irate*(1+irate)**term) / (((1+irate)**term)-1))

# returns all non-mortgage payment expenses for a month
def calc_expenses (rent, vac_rate, maint_rate, prop_mgmt_fees, taxes, insurance):
    return (rent * vac_rate) \
            + (rent * maint_rate) \
            + (rent * prop_mgmt_fees) \
            + (taxes / 12) \
            + (insurance / 12)

# determines the monthly cash flow expected from the property (mgt_payment == mortgage payment)
def calc_cash_flow(rent, vac_rate, maint_rate, prop_mgmt_fees, taxes, insurance, mgt_payment):
    expenses = calc_expenses(rent, vac_rate, maint_rate, prop_mgmt_fees, taxes, insurance)
    return rent - expenses - mgt_payment

# Maximum Principal for this property to ensure cash flow >= min_cf
def calc_max_principal(rent, vac_rate, maint_rate, prop_mgmt_fees, taxes, insurance, \
                    irate, term, min_cf=100):
    irate = irate/1200
    expenses = calc_expenses(rent, vac_rate, maint_rate, prop_mgmt_fees, taxes, insurance)
    qty = float((irate*(1+irate)**term) / (((1+irate)**term)-1))
    p = (-min_cf + rent - expenses) / qty
    return p/.8

st.title("Financial Modeling 📊")
st.subheader('''This modeling application is designed to calculate and visualize key variables\
            associated with real estate due diligence projects.''')
st.write('''In the future, this can be built out to evaluate the financial health of prospective\
            businesses as well.''')
menu = ["Upload a CSV", "User Input"]
choice = st.sidebar.selectbox("Data Entry Options", menu)
authenticator.logout("Logout", "sidebar")

if choice == "Upload a CSV":
    data_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if st.button("Process CSV"):
        if data_file is not None:
            df = pd.read_csv(data_file)
            st.dataframe(df)
        
        results = {
            "ID": [],
            "Mortgage Payment" : [],
            "Total Payments": [],
            "Total Interest": [],
            "Cash Required": [],
            "Minimum Monthly Expenses": [],
            "Monthly Cash Flow": [],
            "Max Purhcase Price": [],
            "Annual Yield (CoC ROI)": [],
            "Cap Rate": []
    }

        # iterate all provided data 
        for i in range(df.shape[0]):
            row = df.iloc[i]
            
            pmt = get_mortgage_pmt(row["Purchase Price"], row["Interest Rate"], row["Loan Term"])
            # the property's ID
            results["ID"].append(row["ID"])
            # the mortgage payment
            results["Mortgage Payment"].append(round(pmt, 2))
            # the total amount of payments made on the mortgage
            results["Total Payments"].append(round(pmt*row["Loan Term"], 2))
            # the interest that will be paid (total payments - actual principle, the remainder is interest)
            results["Total Interest"].append(round((pmt*row["Loan Term"] - row["Loan Amount"]), 2))

            # the cash required to purchase the property
            upfront_cash = row["Closing Costs"] + (row["Purchase Price"] - row["Loan Amount"])
            results["Cash Required"].append(round(upfront_cash, 2))
            
            # Monthly exenses if there are no maintenance, property management, and vacancy fees
            expenses = pmt + (row["Annual Property Taxes"]/12) + (row["Annual Property Insurance"]/12)      # exludes maintenance, prop. management, and vacancy
            results["Minimum Monthly Expenses"].append(round(expenses, 2))
            
            # the monthly cash flow we can expect from the property
            cf = calc_cash_flow(row["Rental Income"], row["Vacancy Rate"], row["Maintenance Expense"], row["Property Management Fees"], 
                row["Annual Property Taxes"], row["Annual Property Insurance"], pmt)
            results["Monthly Cash Flow"].append(round(cf, 2))

            # this is the most you should pay for a property assuming that you want to earn 
            # at least $100 per month in cash flow; the minimum cash flow is actually a parameter
            # to the calc_max_principal function.
            max_purchase = calc_max_principal(row["Rental Income"], row["Vacancy Rate"], row["Maintenance Expense"], row["Property Management Fees"], 
                row["Annual Property Taxes"], row["Annual Property Insurance"], row["Interest Rate"], row["Loan Term"])
            results["Max Purhcase Price"].append(round(max_purchase, 2))

            # the cap rate and CoC return as decribed above.
            cap_rate = ((cf+pmt)*12)/row["Purchase Price"] ## cap rate = what if we bought the property with cash?
            results["Annual Yield (CoC ROI)"].append(round(((12*cf)/upfront_cash)*100, 2))
            results["Cap Rate"].append(round(cap_rate*100, 2))

        result_df = pd.DataFrame.from_dict(results)
        st.write(result_df)
        fig = px.bar(result_df, 
                    x="ID", 
                    y=["Mortgage Payment", "Total Payments", "Total Interest", 
                        "Cash Required", "Minimum Monthly Expenses", "Monthly Cash Flow", 
                        "Max Purhcase Price"],
                    barmode='relative',
                    title='Dollar Figure Visulization'
                    )
        st.write(fig)
        fig2 = px.bar(result_df, 
                    x="ID", 
                    y=["Annual Yield (CoC ROI)", "Cap Rate"],
                    barmode='group',
                    title='Return % Visulization'
                    )
        st.write(fig2)


if choice == "User Input":
    with st.form(key='input1'):
        address = st.text_input("Address")
        purchase_price = st.text_input("Purchase Price: $")
        if purchase_price is not None:
            try:
                pp_float = float(purchase_price)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
      #          st.warning("Please enter a valid number")
        rent = st.text_input("Estimated Rent: $")
        if rent is not None:
            try:
                rent_float = float(rent)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        closing_costs = st.text_input("Estimated Closing Costs: $")
        if closing_costs is not None:
            try:
                cc_float = float(closing_costs)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        loan_amt = st.text_input("Loan Amount (Enter for default): $")
        if loan_amt is not None:
            try:
                loan_amt_float = float(loan_amt)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        irate = st.text_input("Interest Rate (% as a whole number):")
        if irate is not None:
            try:
                irate_float = float(irate)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        term = st.text_input("Loan Term (Months):")
        if term is not None:
            try:
                term_float = float(term)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        vac = st.text_input("Vacancy Rate (% as a decimal):")
        if vac is not None:
            try:
                vac_float = float(vac)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        maint = st.text_input("Maintenance (% of rent as a decimal):")
        if maint is not None:
            try:
                maint_float = float(maint)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        pmf = st.text_input("Prop. Mgmt. Fees (% of rent as a decimal):")
        if pmf is not None:
            try:
                pmf_float = float(pmf)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        txs = st.text_input("Annual Prop. Tax: $")
        if txs is not None:
            try:
                txs_float = float(txs)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        ins = st.text_input("Annual Prop. Insurance: $")
        if ins is not None:
            try:
                ins_float = float(ins)
            except Exception:
                print('''Sorry. You havn't completed your submission.''')
        process_button = st.form_submit_button("Process")
        st.write('The error message below will disappear as soon as you complete the form \
                    and click process')

        data = {
            "ID": [address],
            "Purchase Price": [pp_float],
            "Rental Income": [rent_float],
            "Closing Costs": [cc_float],
            "Loan Amount": [loan_amt_float],
            "Interest Rate": [irate_float],
            "Vacancy Rate": [vac_float],
            "Loan Term": [term_float],
            "Maintenance Expense": [maint_float],
            "Property Management Fees": [pmf_float],
            "Annual Property Taxes": [txs_float],
            "Annual Property Insurance": [ins_float]
        }
        df1 = pd.DataFrame(data)
        if process_button:
            results = {
                "ID": [],
                "Mortgage Payment" : [],
                "Total Payments": [],
                "Total Interest": [],
                "Cash Required": [],
                "Minimum Monthly Expenses": [],
                "Monthly Cash Flow": [],
                "Max Purhcase Price": [],
                "Annual Yield (CoC ROI)": [],
                "Cap Rate": []
            }

            for i in range(df1.shape[0]):
                row = df1.iloc[i]
                
                pmt = get_mortgage_pmt(row["Purchase Price"], row["Interest Rate"], row["Loan Term"])
                results["ID"].append(row["ID"])
                results["Mortgage Payment"].append(round(pmt, 2))
                results["Total Payments"].append(round(pmt*row["Loan Term"], 2))
                results["Total Interest"].append(round((pmt*row["Loan Term"] - row["Loan Amount"]), 2))

                upfront_cash = row["Closing Costs"] + (row["Purchase Price"] - row["Loan Amount"])
                results["Cash Required"].append(round(upfront_cash, 2))
                
                expenses = pmt + (row["Annual Property Taxes"]/12) + (row["Annual Property Insurance"]/12)      # exludes maintenance, prop. management, and vacancy
                results["Minimum Monthly Expenses"].append(round(expenses, 2))
                
                cf = calc_cash_flow(row["Rental Income"], row["Vacancy Rate"], row["Maintenance Expense"], row["Property Management Fees"], 
                    row["Annual Property Taxes"], row["Annual Property Insurance"], pmt)
                results["Monthly Cash Flow"].append(round(cf, 2))

                max_purchase = calc_max_principal(row["Rental Income"], row["Vacancy Rate"], row["Maintenance Expense"], row["Property Management Fees"], 
                    row["Annual Property Taxes"], row["Annual Property Insurance"], row["Interest Rate"], row["Loan Term"])
                results["Max Purhcase Price"].append(round(max_purchase, 2))

                cap_rate = ((cf+pmt)*12)/row["Purchase Price"] ## cap rate = what if we bought the property with cash?
                results["Annual Yield (CoC ROI)"].append(round(((12*cf)/upfront_cash)*100, 2))
                results["Cap Rate"].append(round(cap_rate*100, 2))

            result_df1 = pd.DataFrame.from_dict(results)
            st.write(result_df1)
            fig3 = px.bar(result_df1, 
                    x="ID", 
                    y=["Mortgage Payment", "Total Payments", "Total Interest", 
                        "Cash Required", "Minimum Monthly Expenses", "Monthly Cash Flow", 
                        "Max Purhcase Price"],
                    barmode='relative',
                    title='Dollar Figure Visulization'
                    )
            st.write(fig3)
            fig4 = px.bar(result_df1, 
                    x="ID", 
                    y=["Annual Yield (CoC ROI)", "Cap Rate"],
                    barmode='group',
                    title='Return % Visulization'
                    )
            st.write(fig4)

        




