import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Automation Dashboard", layout="wide")

st.title("📊 Excel Automation Dashboard")

uploaded_file = st.file_uploader(
    "📂 Upload Excel File",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

else:
    df = pd.read_excel("output/cleaned_sales.xlsx")


sales_chart = df.sort_values(by="Price", ascending=False)
quantity_chart = df.sort_values(by="Quantity", ascending=False)

st.subheader("Sales Data")

st.dataframe(df, width="stretch")

st.subheader("Sales Chart")

st.bar_chart(
    sales_chart,
    x="Product",
    y="Price",
    width="stretch"
)

st.subheader("Statistics")

st.subheader("Product Quantity")

st.bar_chart(
    quantity_chart,
    x="Product",
    y="Quantity",
    width="stretch"
)

col1, col2, col3 = st.columns(3)

col1.metric("Orders", len(df))
col2.metric("Products", df["Product"].nunique())
col3.metric("Revenue", f"₹{(df['Quantity']*df['Price']).sum():,}")