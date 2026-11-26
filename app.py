from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"/"sales_data.csv"
REQUIRED={"order_id","order_date","customer_id","product_name","category","quantity","revenue","profit","region","sales_channel","customer_segment"}
st.set_page_config(page_title="Business Sales Analytics",page_icon="📊",layout="wide")
st.title("📊 Business Sales Analytics Dashboard")
st.caption("Interactive portfolio project | Synthetic sample data | Jan 2024 – Dec 2025")

@st.cache_data
def load_data():
    df=pd.read_csv(DATA,parse_dates=["order_date"])
    missing=REQUIRED-set(df.columns)
    if missing: raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    return df

df=load_data()
with st.sidebar:
    st.header("Filters")
    min_date,max_date=df.order_date.min().date(),df.order_date.max().date()
    dates=st.date_input("Order date range",value=(min_date,max_date),min_value=min_date,max_value=max_date)
    regions=st.multiselect("Region",sorted(df.region.unique()),default=sorted(df.region.unique()))
    categories=st.multiselect("Category",sorted(df.category.unique()),default=sorted(df.category.unique()))
    channels=st.multiselect("Sales channel",sorted(df.sales_channel.unique()),default=sorted(df.sales_channel.unique()))
if isinstance(dates,(tuple,list)) and len(dates)==2: start,end=dates
elif isinstance(dates,(tuple,list)) and len(dates)==1: start=end=dates[0]
else: start,end=min_date,max_date
f=df[df.order_date.dt.date.between(start,end)&df.region.isin(regions)&df.category.isin(categories)&df.sales_channel.isin(channels)].copy()
if f.empty:
    st.warning("No records match the selected filters. Please broaden your selection.")
    st.stop()
revenue,profit=f.revenue.sum(),f.profit.sum()
orders,customers=f.order_id.nunique(),f.customer_id.nunique()
margin=profit/revenue*100 if revenue else 0
cols=st.columns(5)
for col,label,value in zip(cols,["Total Revenue","Total Profit","Orders","Unique Customers","Profit Margin"],[f"${revenue:,.0f}",f"${profit:,.0f}",f"{orders:,}",f"{customers:,}",f"{margin:.1f}%"]): col.metric(label,value)
monthly=f.assign(month=f.order_date.dt.to_period("M").astype(str)).groupby("month",as_index=False).agg(Revenue=("revenue","sum"),Profit=("profit","sum"))
left,right=st.columns([1.6,1])
with left:
    st.subheader("Monthly Revenue Trend")
    fig=px.line(monthly,x="month",y="Revenue",markers=True,template="plotly_white")
    fig.update_layout(xaxis_title="Month",yaxis_title="Revenue (USD)")
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader("Revenue by Category")
    cat=f.groupby("category",as_index=False).revenue.sum().sort_values("revenue",ascending=False)
    fig=px.pie(cat,names="category",values="revenue",hole=.55,template="plotly_white")
    st.plotly_chart(fig,use_container_width=True)
left,right=st.columns(2)
with left:
    st.subheader("Top 10 Products")
    top=f.groupby("product_name",as_index=False).agg(Revenue=("revenue","sum"),Units=("quantity","sum")).nlargest(10,"Revenue").sort_values("Revenue")
    fig=px.bar(top,x="Revenue",y="product_name",orientation="h",text_auto=".2s",template="plotly_white")
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader("Regional Performance")
    reg=f.groupby("region",as_index=False).agg(Revenue=("revenue","sum"),Profit=("profit","sum"))
    fig=px.bar(reg,x="region",y=["Revenue","Profit"],barmode="group",template="plotly_white")
    st.plotly_chart(fig,use_container_width=True)
st.subheader("Customer Trends")
customer=f.groupby("customer_id",as_index=False).agg(Revenue=("revenue","sum"),Orders=("order_id","nunique"))
repeat=customer.Orders.gt(1).mean()*100 if len(customer) else 0
a,b,c=st.columns(3)
a.metric("Repeat Customer Rate",f"{repeat:.1f}%")
b.metric("Average Order Value",f"${revenue/orders:,.2f}" if orders else "$0.00")
c.metric("Revenue per Customer",f"${revenue/customers:,.2f}" if customers else "$0.00")
mc=f.assign(month=f.order_date.dt.to_period("M").astype(str)).groupby("month").customer_id.nunique().reset_index(name="Unique Customers")
fig=px.area(mc,x="month",y="Unique Customers",template="plotly_white")
st.plotly_chart(fig,use_container_width=True)
st.subheader("Filtered Sales Records")
st.dataframe(f.sort_values("order_date",ascending=False),use_container_width=True,hide_index=True)
st.download_button("Download filtered data (CSV)",f.to_csv(index=False).encode("utf-8"),file_name="filtered_sales_data.csv",mime="text/csv")
st.caption("Synthetic sample data generated for portfolio demonstration. Currency is illustrative USD.")
