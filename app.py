import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit import session_state as ss
st.set_page_config(layout="wide")


st.title("CRED assignment")

def create_emi_table(p,r,n):
    dic = {
        "Month":[],
        "Balance Outstanding at start of period":[],
        "Payment received (EMI amount)" :[],
        "Principal paid": [],
        "Interest paid": [],
        "Balance outstanding at end of period":[]
    }
    balance = p
    for i in range(n):
        dic["Balance Outstanding at start of period"].append(balance)
        rpowern = (1 + r)**n
        emi = round(p * (r*rpowern)/(rpowern-1),2)
        interest_paid = round(balance*r,2)
        principal_paid = round(emi-interest_paid,2)
        balance -= principal_paid
        dic["Month"].append(i+1)
        dic["Payment received (EMI amount)"].append(emi)
        dic["Principal paid"].append(principal_paid)
        dic["Interest paid"].append(interest_paid)
        dic["Balance outstanding at end of period"].append(balance)
    return dic

def update(last):
    global annualized_interest_rate, monthly_interest_rate
    if last == "A":
        ss.M = round(ss.A/12,5) 
    else:
        ss.A = ss.M*12



loan_value = st.number_input("Loan value", value = 100000)
annualized_interest_rate = st.number_input("Annualized Interest rate", key = "A", value = 0.15, on_change=update, format = "%f", args = ("A",))
monthly_interest_rate = st.number_input("Monthly Interest rate", key = "M", value = 0.0125, on_change=update, format = "%f", args = ("M",))
columns = st.columns(2)


with columns[0]:
    st.header("Question 1")
    tenure = st.number_input("Tenure in months", key = "T", value = 6)
    p = loan_value
    r = monthly_interest_rate
    n = tenure

    dic = create_emi_table(p,r,n)

    st.write("Total emi paid", round(sum(dic["Payment received (EMI amount)"]),2))
    st.write("Total Principal paid", round(sum(dic["Principal paid"]),2))
    st.write("Total Interest paid", round(sum(dic["Interest paid"]),2))

    df = pd.DataFrame.from_dict(dic)
    st.write(df)
    x=[i for i in range(1,n+1)]
    principal=dic["Principal paid"]
    interest=dic["Interest paid"]
    emipayment=dic["Payment received (EMI amount)"]
    fig=px.line(x=x,y=[principal,interest,emipayment],
    labels={'x':"Month"},markers=True)    
    fig.update_layout(yaxis=dict(title=dict(text='Amount')))

    # Add a legend to each line
    fig.update_traces(name='Principal paid', legendgroup='Principal paid')
    fig.update_traces(name='Interest paid', legendgroup='Interest paid')
    fig.update_traces(name='EMI paid', legendgroup='EMI paid')

    fig.update_traces(textposition="bottom right")


    fig.update_layout(annotations=[
    dict(x=x[1], y=principal[1], text='Principal paid', xref='x', yref='y', showarrow=True, arrowhead=7,arrowcolor='white',font=dict(size=18)),
    dict(x=x[0], y=interest[0], text='Interest paid', xref='x', yref='y', showarrow=True, arrowhead=7,arrowcolor='white',font=dict(size=18)),
    dict(x=x[0], y=emipayment[0], text='EMI paid', xref='x', yref='y', showarrow=True,arrowcolor='white',arrowhead=7,font=dict(size=18))])


    # Increase the line width and add circles to each data point
    fig.data[0].update(name='Principal paid')
    fig.data[0].line.color = "#eba408"

    fig.data[1].update(name='Interest paid')
    fig.data[1].line.color = "#0aff37"

    fig.data[2].update(name='EMI paid')
    fig.data[2].line.color = "#aa00ff"
    fig.update_layout(title=dict(text="Loan Payment Graph-Question 1",x=0.5), legend=dict(title=dict(text='Payment Line')))

    

    
    st.plotly_chart(fig)









with columns[1]:
    st.header("Question 2")
    no = st.number_input("Number of loans", value = 12)
    loans = [0 for i in range(no)]
    default_distribution = [5, 5, 10, 2, 5, 25, 2, 2, 15, 2, 2, 25]
    tenure = [int(0) for i in range(no)]
    default_tenure =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    with st.expander("Open to Edit distribution and Tenure"):
        for i in range(no):
            if no == 12:
                default_loan = default_distribution[i]
                default_tenure_val = default_tenure[i]
            else:
                default_loan = 0
                default_tenure_val = 0
        
            loans[i] = st.number_input(f"Loan {i+1} %", key = f"L{i}", value = default_loan)
            tenure[i] = st.number_input(f"Tenure for loan" , key = f"T{i}", value = default_tenure_val)
            st.write(f"Sum of current Distribution is {sum(loans)}%")
            st.write("-------------")
        if(sum(loans)!=100):
            st.error(f"Sum of distributions should be 100,Current distributions is {sum(loans)}")
    
    max_tenure = max(tenure)
    dic = {
        "Month":[],
        "Balance Outstanding at start of period":[],
        "Payment received (EMI amount)" :[],
        "Principal paid": [],
        "Interest paid": [],
        "Balance outstanding at end of period":[]
    }

    for key in dic:
        if key == "Month":
            dic[key] = [ i+1 for i in range(max_tenure)]
        else:
            dic[key] = [ 0 for i in range(max_tenure)]
    loan_tables = []
    for i in range(no):
        p = loans[i]*loan_value/100
        r = monthly_interest_rate
        n = tenure[i]

        d = create_emi_table(p,r,n)
        loan_tables.append(d)
        for index in d["Month"]:
            for key in d:
                if key != "Month":
                    dic[key][index-1] += d[key][index-1]
    
    df = pd.DataFrame.from_dict(dic)
    st.write("Total emi paid", round(sum(dic["Payment received (EMI amount)"]),2))
    st.write("Total Principal paid", round(sum(dic["Principal paid"]),2))
    st.write("Total Interest paid", round(sum(dic["Interest paid"]),2))
    without_foreclosure_amount=round(sum(dic["Interest paid"]),2)
    st.write(df)
    with st.expander("Check individual loan tables"):
        for i in loan_tables:
            df = pd.DataFrame.from_dict(i)
            st.write(df)
            st.write("Total Interest paid", round(sum(i["Interest paid"]),2))
    x=[i for i in range(1,n+1)]
    principal=dic["Principal paid"]
    interest=dic["Interest paid"]
    emipayment=dic["Payment received (EMI amount)"]
    fig=px.line(x=x,y=[principal,interest,emipayment],
    labels={'x':"Month"},markers=True)    
    fig.update_layout(yaxis=dict(title=dict(text='Amount')))

    # Add a legend to each line
    fig.update_traces(name='Principal paid', legendgroup='Principal paid')
    fig.update_traces(name='Interest paid', legendgroup='Interest paid')
    fig.update_traces(name='EMI paid', legendgroup='EMI paid')

    fig.update_traces(textposition="bottom right")


    fig.update_layout(annotations=[
    dict(x=x[1], y=principal[1], text='Principal paid', xref='x', yref='y', showarrow=True, arrowhead=7,arrowcolor='white',font=dict(size=18)),
    dict(x=x[0], y=interest[0], text='Interest paid', xref='x', yref='y', showarrow=True, arrowhead=7,arrowcolor='white',font=dict(size=18)),
    dict(x=x[0], y=emipayment[0], text='EMI paid', xref='x', yref='y', showarrow=True,arrowcolor='white',arrowhead=7,font=dict(size=18))])


    # Increase the line width and add circles to each data point
    fig.data[0].update(name='Principal paid')
    fig.data[0].line.color = "#eba408"

    fig.data[1].update(name='Interest paid')
    fig.data[1].line.color = "#0aff37"

    fig.data[2].update(name='EMI paid')
    fig.data[2].line.color = "#aa00ff"
    fig.update_layout(title=dict(text="Loan Payment Graph-Question 2",x=0.5), legend=dict(title=dict(text='Payment Line')))

    

    
    st.plotly_chart(fig)
       

    st.header("Question 3")
    with st.expander("Open to edit foreclosure curve"):
        foreclosure_tenure = int(st.number_input("Enter the number of months in the foreclosure curve", 12))
        default_values = [4.44, 2.58, 2.47, 2.35, 2.32, 2.36, 2.17, 2.22, 2.26, 2.17, 2.33, 2.72]
        foreclosures = [0 for i in range(foreclosure_tenure)]
        for i in range(foreclosure_tenure):
            foreclosures[i] = st.number_input(f"Enter foreclosure % for period {i+1}", value = default_values[i])


    dic = {
        "Month":[],
        "Balance Outstanding at start of period":[],
        "Payment received (EMI amount)" :[],
        "Principal paid": [],
        "Interest paid": [],
        "Foreclosure Charge paid": [],
        "Balance outstanding at end of period":[]
    }

    for key in dic:
        if key == "Month":
            dic[key] = [ i+1 for i in range(max_tenure)]
        else:
            dic[key] = [ 0 for i in range(max_tenure)]

        # Checking individual loans , and listing the period where it makes sense to foreclose
    st.subheader("Scenarios where it makes sense to foreclose")
    foreclosing_months = []
    total_savings = 0
    min_charges_foreclosure = []
    for l in range(len(loan_tables)):
        loan_table = loan_tables[l]
        total_charges_no_foreclosure = sum(loan_table["Interest paid"])
        max_savings_for_loan = 0
        max_savings_month = 0
        min_charges = 0
        for month in loan_table["Month"]: # 1-based
            starting = loan_table["Balance Outstanding at start of period"][month-1]
            foreclose_charge = starting*foreclosures[month-1]/100

            total_charges_foreclosure = foreclose_charge + sum(loan_table["Interest paid"][:month])
            #st.write(foreclose_charge,total_charges_foreclosure, total_charges_no_foreclosure, l)
            if(total_charges_foreclosure < total_charges_no_foreclosure):
                savings = total_charges_no_foreclosure - total_charges_foreclosure
                
                if savings > max_savings_for_loan:
                    max_savings_for_loan = savings
                    max_savings_month = month
                    min_charges = foreclose_charge
                #st.write(f"Foreclose Loan {l+1} on month {month} to save {savings}")
        if max_savings_for_loan == 0:
            #st.write(f"Best foreclosing scenario for loan {l+1} is to NOT to foreclose")
            st.markdown(f'Best foreclosing scenario for loan {l+1} is to <span style="color:red">NOT</span> to foreclose',unsafe_allow_html=True)
        else:
            st.write(f'Best foreclosing scenario for loan {l+1}, is on month <span style="font-weight:bold;font-size:18px;color:yellow">{max_savings_month}</span> to save <span style="color:green">{round(max_savings_for_loan,2)}</span>',unsafe_allow_html=True)
        foreclosing_months.append(max_savings_month-1)
        total_savings += max_savings_for_loan
        min_charges_foreclosure.append(min_charges)
        #st.write("----------------------------------------------------------------")

    for l in range(len(loan_tables)):
        loan_table = loan_tables[l]
        foreclosed_month = foreclosing_months[l]
        if(foreclosed_month == -1):
            for index in loan_table["Month"]:
                for key in loan_table:
                    if key != "Month":
                        dic[key][index-1] += loan_table[key][index-1]
                        
        else:
            for index in loan_table["Month"][:foreclosed_month]:
                for key in loan_table:
                    if key != "Month":
                        dic[key][index-1] += loan_table[key][index-1]

            dic["Balance Outstanding at start of period"][foreclosed_month] += loan_table["Balance Outstanding at start of period"][foreclosed_month]
            dic["Payment received (EMI amount)"][foreclosed_month] += loan_table["Balance Outstanding at start of period"][foreclosed_month] + loan_table["Interest paid"][foreclosed_month]
            dic["Principal paid"][foreclosed_month] += loan_table["Balance Outstanding at start of period"][foreclosed_month]
            dic["Interest paid"][foreclosed_month] += loan_table["Interest paid"][foreclosed_month]
            dic["Foreclosure Charge paid"][foreclosed_month] += min_charges_foreclosure[l]
    df = pd.DataFrame.from_dict(dic)
    st.write("Total EMI paid", round(sum(dic["Payment received (EMI amount)"]),2))
    st.write("Total Principal paid", round(sum(dic["Principal paid"]),2))
    st.write("Total Interest paid", round(sum(dic["Interest paid"]),2))
    st.write("Total foreclose charges paid", round(sum(dic["Foreclosure Charge paid"]),2))
    st.write("Total charges paid", round(sum(dic["Foreclosure Charge paid"]),2) + round(sum(dic["Interest paid"]),2))
    st.write("Total Savings",without_foreclosure_amount-round(sum(dic["Foreclosure Charge paid"]),2) - round(sum(dic["Interest paid"]),2))
    principal=dic["Principal paid"]
    interest=dic["Interest paid"]
    emipayment=dic["Payment received (EMI amount)"]
    foreclose_charge=dic["Foreclosure Charge paid"]

    fig=px.line(x=x,y=[principal,interest,emipayment,foreclose_charge],
    labels={'x':"Month"},markers=True)    
    fig.update_layout(yaxis=dict(title=dict(text='Amount')))

    # Add a legend to each line
    fig.update_traces(name='Principal paid', legendgroup='Principal paid')
    fig.update_traces(name='Interest paid', legendgroup='Interest paid')
    fig.update_traces(name='EMI paid', legendgroup='EMI paid')
    fig.update_traces(name='Foreclosure Charges paid', legendgroup='EMI paid')

    fig.update_traces(textposition="bottom right")


    fig.update_layout(annotations=[
    dict(x=x[1], y=principal[1], text='Principal paid', xref='x', yref='y', showarrow=True, arrowhead=7,arrowcolor='white',font=dict(size=18)),
    dict(x=x[0], y=interest[0], text='Interest paid', xref='x', yref='y', showarrow=True, arrowhead=7,arrowcolor='white',font=dict(size=18)),
    dict(x=x[0], y=emipayment[0], text='EMI paid', xref='x', yref='y', showarrow=True,arrowcolor='white',arrowhead=7,font=dict(size=18)),
    dict(x=x[0], y=foreclose_charge[0], text='Foreclosure Charges paid', xref='x', yref='y', showarrow=True,arrowcolor='white',arrowhead=7,font=dict(size=18))])

    # Increase the line width and add circles to each data point
    fig.data[0].update(name='Principal paid')
    fig.data[0].line.color = "#eba408"

    fig.data[1].update(name='Interest paid')
    fig.data[1].line.color = "#0aff37"

    fig.data[2].update(name='EMI paid')
    fig.data[2].line.color = "#aa00ff"
    fig.update_layout(title=dict(text="Loan Payment Graph-Question 3",x=0.5), legend=dict(title=dict(text='Payment Line')))

    fig.data[3].update(name='Foreclosure Charges paid')
    fig.data[3].line.color = "#f70000"

    
    st.plotly_chart(fig)


    st.write(df)