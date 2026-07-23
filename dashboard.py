import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Automation Dashboard", layout="wide")

st.title("📊 Excel Automation Dashboard")

df = pd.read_excel("output/cleaned_sales.xlsx")

st.subheader("Sales Data")

st.dataframe(df, width="stretch")

st.subheader("Sales Chart")

st.bar_chart(
    data=df,
    x="Product",
    y="Price",
    width="stretch"
)

st.subheader("Statistics")

st.subheader("Product Quantity")

st.bar_chart(
    data=df,
    x="Product",
    y="Quantity",
    width="stretch"
)

col1, col2, col3 = st.columns(3)

col1.metric("Orders", len(df))
col2.metric("Products", df["Product"].nunique())
col3.metric("Revenue", f"₹{(df['Quantity']*df['Price']).sum():,}")