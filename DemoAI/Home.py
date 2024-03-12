import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
import os
from streamlit_extras.metric_cards import style_metric_cards
from PIL import Image
st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go

def auto_refresh(interval):
    script = f"""
        <script>
        function refresh() {{
            setTimeout(() => {{
                window.location.reload();
            }}, {interval});
        }}
        refresh();
        </script>
    """
    st.markdown(script, unsafe_allow_html=True)


st.set_page_config(page_title="Morison PlatForm",page_icon="🌍",layout="wide")
img = Image.open('logo.png')
#uncomment this line if you use mysql
#from query import *
#st.image(img, width=300)
st.image(img, width=300)
st.title(" :bar_chart:  AI Financial Dashboard")
st.subheader('Developed by Morison Global.')
st.header("ANALYTICAL PROCESSING, KPI, TRENDS & PREDICTIONS")

#all graphs we use custom css not streamlit 
theme_plotly = None 


# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
#st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
#uncomment these two lines if you fetch data from mysql
#result = view_all_data()
#df=pd.DataFrame(result,columns=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])

#load excel file | comment this line when  you fetch data from mysql
#df=pd.read_excel('data.xlsx', sheet_name='Sheet1')
df = pd.read_csv("naya.csv", encoding = "ISO-8859-1")
df2 = pd.read_csv("proloss.csv", encoding = "ISO-8859-1")



#side bar logo


#switcher

#contactname=st.sidebar.multiselect(
#    "SELECT CONTACTNAME",
#     options=df["ContactName"].unique(),
     #default=df["ContactName"].unique(),
#)

#description=st.sidebar.multiselect(
#    "SELECT DESCRIPTION",
#     options=df["Description"].unique(),
     #default=df["Description"].unique(),
#)

#construction=st.sidebar.multiselect(
#    "SELECT CONSTRUCTION",
#     options=df["Construction"].unique(),
#     default=df["Construction"].unique(),
#)

#df_selection=df.query(
#    "ContactName==@contactname & Description==@description"
#)


df_selection=df
df2_selection=df2
df_delivery_income=df.query("Type == 'ACCPAY'")
df_delivery_income2=df.query("Type == 'ACCREC'")
#this function performs basic descriptive analytics like Mean,Mode,Sum  etc
def Home():
    with st.expander("VIEW EXCEL DATASET"):
        #showData=st.multiselect('Filter: ',df_selection.columns,default=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating"])
        #showData=st.multiselect('Filter: ',df_selection.columns,default=["ContactName","InvoiceNumber","Reference","InvoiceDate","Total","InvoiceAmountPaid","InvoiceAmountDue","Description","Quantity","UnitAmount","Sale","Currency","Type","GrossProfit","NetProfit"])
        showData=st.multiselect('Filter: ',df_selection.columns,default=["Type","Name","Total","Date"])
        st.dataframe(df_selection[showData],use_container_width=True)
    #compute top analytics
    total_investment = float(pd.Series(df_delivery_income['Total']).sum())
    investment_mode = float(pd.Series(df_delivery_income2['Total']).sum())
    #investment_mean = float(pd.Series(df_selection['GrossProfit']).sum())
    #investment_median= float(pd.Series(df_selection['NetProfit']).sum()) 
    #total_delivery_charge = float(pd.Series(df_delivery_income['Total']).sum())
    #rating = float(pd.Series(df_selection['Rating']).sum())

    current_status = investment_mode - total_investment
    total1,total2,total3,total4,total5=st.columns(5,gap='small')    
    with total1:
        st.info('Payments',icon="💰")
        st.metric(label="Total Payments",value=f"{total_investment:,.2f} KD")

    with total2:
        st.info('Receievd',icon="💰")
        st.metric(label="Total Receive",value=f"{investment_mode:,.2f} KD")

    with total3:
        if current_status < 0:
           st.info('Loss ↓', icon="🔻")
           st.metric(label="Total Loss", value=f"({abs(current_status):,.2f}) KD")
           #t.metric(label="Total Loss",value=f"{current_status:,.2f} KD")
        else:
           st.info('Profit',icon="💰")
           st.metric(label="Total Profit",value=f"{current_status:,.2f} KD")
    #with total4:
    #    st.info('Gross',icon="💰")
    #    st.metric(label="Gross Profit",value=f"{investment_mean:,.2f} KD")

    #with total5:
    #    st.info('Net Profit',icon="💰")
    #    st.metric(label="Net Profit",value=f"{investment_median:,.2f} KD")
    
    style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")

    #variable distribution Histogram
    with st.expander("HISTOGRAM BY TOTAL"):
     df.hist(figsize=(16,8),color='#898784', zorder=2, rwidth=0.9,legend = ['Total']);
     st.pyplot()

#graphs
def graphs():
    #total_investment=int(df_selection["Investment"]).sum()
    #averageRating=int(round(df_selection["Rating"]).mean(),2) 
    #simple bar graph  investment by business type
    
    
    #simple line graph investment by state
    investment_by_business_type=df_delivery_income.groupby(by=["Name"]).sum()[["Total"]]
    fig_investment=px.line(
       investment_by_business_type,
       x=investment_by_business_type.index,
       y="Total",
       orientation="v",
       title="<b> EXPENSES BY TYPE </b>",
       color_discrete_sequence=["#0083b8"]*len(investment_by_business_type),
       template="plotly_white",
    )
    fig_investment.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
     )

    #simple line graph investment by state
    investment_state=df_delivery_income2.groupby(by=["Name"]).sum()[["Total"]]
    fig_state=px.line(
       investment_state,
       x=investment_state.index,
       y="Total",
       orientation="v",
       title="<b> INCOME BY CUSTOMERS </b>",
       color_discrete_sequence=["#0083b8"]*len(investment_state),
       template="plotly_white",
    )
    fig_state.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
     )

    left,right,center=st.columns(3)
    left.plotly_chart(fig_state,use_container_width=True)
    right.plotly_chart(fig_investment,use_container_width=True)
    
    with center:
      #pie chart
      fig = px.pie(df_selection, values='Total', names='Name', title='INCOME PERCENTAGE BY CUSTOMERS')
      fig.update_layout(legend_title="Customers", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

#function to show current earnings against expected target     
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #ffffff , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=20000
    current=df_delivery_income2['Total'].sum() - df_delivery_income['Total'].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)

    if percent>100:
        st.subheader("Target done !")
    else:
     #st.write("you have ",percent, "% " ,"of ", (format(target, 'd')), "Profit")
     st.write("you have reached <span style='color:red'>{:}%</span> of {} ".format(percent, format(target, 'd')), "Profit", unsafe_allow_html=True)

     for percent_complete in range(percent):
        time.sleep(0.1)
        mybar.progress(percent_complete+1,text=" Target Percentage")

#menu bar
def sideBar():
 with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="Home":
    #st.subheader(f"Page: {selected}")
    Home()
    graphs()
 if selected=="Progress":
    #st.subheader(f"Page: {selected}")
    Progressbar()
    graphs()

sideBar()
st.sidebar.image("data/Morison.png",caption="Online Analytics")




df2_trading=df2.query("Type == 'Trading Income'")
df2_cost=df2.query("Type == 'Gross Profit'")
df2_operation=df2.query("Type == 'Net Profit'")

#total_trading_income = df2['Trading Income'].sum()
total_trading_income = float(pd.Series(df2_trading['Total']).sum())
total_cost_of_sales = float(pd.Series(df2_cost['Total']).sum())
total_operating_expenses = float(pd.Series(df2_operation['Total']).sum())

st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(f"Monthly Analysis Section  <span style='color:red'></span>", unsafe_allow_html=True)
trade_type=(
        df2_selection.groupby(by=["Type"]).sum()[["Total"]].sort_values(by="Total")
    )
fig_investment=px.bar(
       trade_type,
       x="Total",
       y=trade_type.index,
       orientation="h",
       title="<b> SALE BY ITEMS </b>",
       color_discrete_sequence=["#0083B8"]*len(trade_type),
       template="plotly_white",
    )
fig_investment.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color  
     paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
     xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
     )
st.plotly_chart(fig_investment,use_container_width=True)

st.write(df2)


st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(f"© 2024 Alkhuzam Co. | An Independent Member Of Morison Global. All Right Reserved.  <span style='color:red'></span>", unsafe_allow_html=True)


auto_refresh(60000)  # Refresh every 1 minute


#theme

hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""





