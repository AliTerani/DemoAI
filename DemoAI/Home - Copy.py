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
st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
img = Image.open('logo.png')
#uncomment this line if you use mysql
#from query import *
#st.image(img, width=300)
st.image(img, width=300)
st.title(" :bar_chart: Naya Financial Dashboard")
st.subheader('Developed by Alkhuzam & CO.')
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
df2 = pd.read_csv("nayadet.csv", encoding = "ISO-8859-1")

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
df_delivery_income=df.query("Description == 'Delivery'")
#this function performs basic descriptive analytics like Mean,Mode,Sum  etc
def Home():
    with st.expander("VIEW EXCEL DATASET"):
        #showData=st.multiselect('Filter: ',df_selection.columns,default=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating"])
        showData=st.multiselect('Filter: ',df_selection.columns,default=["ContactName","InvoiceNumber","Reference","InvoiceDate","Total","InvoiceAmountPaid","InvoiceAmountDue","Description","Quantity","UnitAmount","Sale","Currency","Type","GrossProfit","NetProfit"])
        st.dataframe(df_selection[showData],use_container_width=True)
    #compute top analytics
    total_investment = float(pd.Series(df_selection['Sale']).sum())
    investment_mode = float(pd.Series(df_selection['Sale']).mode())
    investment_mean = float(pd.Series(df_selection['GrossProfit']).sum())
    investment_median= float(pd.Series(df_selection['NetProfit']).sum()) 
    total_delivery_charge = float(pd.Series(df_delivery_income['Sale']).sum())
    #rating = float(pd.Series(df_selection['Rating']).sum())

    
    total1,total2,total3,total4,total5=st.columns(5,gap='small')    
    with total1:
        st.info('Sales',icon="💰")
        st.metric(label="Total Trading Income",value=f"{total_investment:,.2f} KD")

    with total2:
        st.info('Most Sales',icon="💰")
        st.metric(label="Most Item Price",value=f"{investment_mode:,.2f} KD")

    with total3:
        st.info('Charges',icon="💰")
        st.metric(label="Delivery Charges Income",value=f"{total_delivery_charge:,.2f} KD")

    with total4:
        st.info('Gross',icon="💰")
        st.metric(label="Gross Profit",value=f"{investment_mean:,.2f} KD")

    with total5:
        st.info('Net Profit',icon="💰")
        st.metric(label="Net Profit",value=f"{investment_median:,.2f} KD")
    
    style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")

    #variable distribution Histogram
    with st.expander("DISTRIBUTIONS BY FREQUENCY"):
     df.hist(figsize=(16,8),color='#898784', zorder=2, rwidth=0.9,legend = ['Sale']);
     st.pyplot()

#graphs
def graphs():
    #total_investment=int(df_selection["Investment"]).sum()
    #averageRating=int(round(df_selection["Rating"]).mean(),2) 
    #simple bar graph  investment by business type
    investment_by_business_type=(
        df_selection.groupby(by=["Description"]).sum()[["Sale"]].sort_values(by="Sale")
    )
    fig_investment=px.bar(
       investment_by_business_type,
       x="Sale",
       y=investment_by_business_type.index,
       orientation="h",
       title="<b> SALE BY ITEMS </b>",
       color_discrete_sequence=["#0083B8"]*len(investment_by_business_type),
       template="plotly_white",
    )
    fig_investment.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color  
     paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
     xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
     )

    #simple line graph investment by state
    investment_state=df_selection.groupby(by=["ContactName"]).sum()[["Sale"]]
    fig_state=px.line(
       investment_state,
       x=investment_state.index,
       y="Sale",
       orientation="v",
       title="<b> SALES BY CUSTOMERS </b>",
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
      fig = px.pie(df_selection, values='Sale', names='ContactName', title='SALES PERCENTAGE BY CUSTOMERS')
      fig.update_layout(legend_title="Customers", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

#function to show current earnings against expected target     
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #ffffff , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=20000
    current=df_selection["Sale"].sum()
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
st.sidebar.image("data/nayalogo.png",caption="Online Analytics")


st.subheader('PICK FEATURES TO EXPLORE DISTRIBUTIONS TRENDS BY ITEMS',)
#feature_x = st.selectbox('Select feature for x Qualitative data', df_selection.select_dtypes("object").columns)
feature_y = st.selectbox('Select feature for y Quantitative Data', df_selection.select_dtypes("number").columns)
fig2 = go.Figure(
    data=[go.Box(x=df['Description'], y=df[feature_y])],
    layout=go.Layout(
        title=go.layout.Title(text="BUSINESS TYPE BY QUARTILES OF INVESTMENT"),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
        font=dict(color='#cecdcd'),  # Set text color to black
    )
)
# Display the Plotly figure using Streamlit
st.plotly_chart(fig2,use_container_width=True)

df2_trading=df2.query("Type == 'Trading Income'")
df2_cost=df2.query("Type == 'Cost of Sales'")
df2_operation=df2.query("Type == 'Operating Expenses'")

#total_trading_income = df2['Trading Income'].sum()
total_trading_income = float(pd.Series(df2_trading['Total']).sum())
total_cost_of_sales = float(pd.Series(df2_cost['Total']).sum())
total_operating_expenses = float(pd.Series(df2_operation['Total']).sum())

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
gros_profit = total_trading_income - total_cost_of_sales
net_profit = gros_profit - total_operating_expenses
if gros_profit < 0:
        st.write(f"Gross Profit:  <span style='color:red'>{gros_profit}</span>", unsafe_allow_html=True)
else:
        st.write(f"Gross Profit: {gros_profit}")

if net_profit < 0:
        st.write(f"Net Profit:  <span style='color:red'>{net_profit}</span>", unsafe_allow_html=True)
else:
        st.write(f"Net Profit: {net_profit}")


st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(f"© 2024 Alkhuzam Co. | An Independent Member Of Morison Global. All Right Reserved.  <span style='color:red'></span>", unsafe_allow_html=True)



#theme

hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""






