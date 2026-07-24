import streamlit as st
import pandas as pd
import plotly.express as px

from modules.cleaner import clean_dataframe
from modules.dataset_detector import detect_dataset
from modules.insights import generate_insights
from modules.advanced_analysis import advanced_analysis

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Excel Automation Suite Pro",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Excel Automation Suite Pro")
st.caption("AI Powered Excel Analysis Dashboard")

# ==========================================================
# FILE UPLOADER
# ==========================================================

uploaded_file = st.file_uploader(
    "📂 Upload Excel / CSV File",
    type=["xlsx", "xls", "csv"]
)

# ==========================================================
# LOAD DATA
# ==========================================================

if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        else:

            df = pd.read_excel(uploaded_file)

    except Exception as e:

        st.error(f"Unable to read file.\n\n{e}")
        st.stop()

else:

    df = pd.read_excel("output/cleaned_sales.xlsx")

# ==========================================================
# CLEAN DATA
# ==========================================================

df, cleaning_report = clean_dataframe(df)

# ==========================================================
# DETECT DATASET
# ==========================================================

dataset_type = detect_dataset(df)

st.success(f"Detected Dataset : {dataset_type}")

# ==========================================================
# AUTO COLUMN DETECTION
# ==========================================================

numeric_columns = (
    df.select_dtypes(include="number")
    .columns
    .tolist()
)

text_columns = (
    df.select_dtypes(include="object")
    .columns
    .tolist()
)

date_columns = (
    df.select_dtypes(
        include=["datetime64", "datetime64[ns]"]
    )
    .columns
    .tolist()
)

product_column = None
value_column = None

if len(text_columns) > 0:

    product_column = text_columns[0]

if len(numeric_columns) > 0:

    value_column = numeric_columns[-1]

# ==========================================================
# AI INSIGHTS
# ==========================================================

if product_column and value_column:

    insights = generate_insights(
        df,
        value_column,
        product_column
    )

else:

    insights = None

analysis = advanced_analysis(df)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("⚙ Filters")

# ==========================================================
# DYNAMIC FILTERS
# ==========================================================

if len(text_columns) > 0:

    st.sidebar.subheader("Dynamic Filters")

    filter_column = st.sidebar.selectbox(

        "Filter Column",

        text_columns

    )

    filter_values = (

        df[filter_column]

        .fillna("Missing")

        .astype(str)

        .drop_duplicates()

        .sort_values()

        .tolist()

    )

    selected_value = st.sidebar.selectbox(

        "Filter Value",

        ["All"] + filter_values

    )

    if selected_value != "All":

        df = df[

            df[filter_column]

            .fillna("Missing")

            .astype(str)

            == selected_value

        ]

# ==========================================================
# DATASET PROFILE
# ==========================================================

total_rows = len(df)

total_columns = len(df.columns)

missing_values = int(

    df.isnull().sum().sum()

)

duplicate_rows = int(

    df.duplicated().sum()

)

numeric_columns = (

    df.select_dtypes(include="number")

    .columns

    .tolist()

)

text_columns = (

    df.select_dtypes(include="object")

    .columns

    .tolist()

)

date_columns = (

    df.select_dtypes(

        include=["datetime64", "datetime64[ns]"]

    )

    .columns

    .tolist()

)

st.subheader("📋 Dataset Profile")

c1, c2, c3 = st.columns(3)

c1.metric("Rows", total_rows)

c2.metric("Columns", total_columns)

c3.metric("Missing Values", missing_values)

c4, c5, c6 = st.columns(3)

c4.metric("Duplicate Rows", duplicate_rows)

c5.metric("Numeric Columns", len(numeric_columns))

c6.metric("Text Columns", len(text_columns))

# ==========================================================
# CLEANING REPORT
# ==========================================================

st.subheader("🧹 Cleaning Report")

r1, r2, r3 = st.columns(3)

r1.metric(
    "Duplicate Rows Removed",
    cleaning_report.get("duplicates_removed", 0)
)

r2.metric(
    "Empty Rows Removed",
    cleaning_report.get("empty_rows_removed", 0)
)

r3.metric(
    "Empty Columns Removed",
    cleaning_report.get("empty_columns_removed", 0)
)

# ==========================================================
# DATA PREVIEW
# ==========================================================

st.subheader("📄 Dataset Preview")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)

# ==========================================================
# CHART PREPARATION
# ==========================================================

if value_column:

    chart_df = df.sort_values(
        by=value_column,
        ascending=False
    )

else:

    chart_df = df.copy()

# ==========================================================
# BAR CHART
# ==========================================================

if product_column and value_column:

    st.subheader("📊 Interactive Bar Chart")

    fig = px.bar(
        chart_df,
        x=product_column,
        y=value_column,
        color=product_column,
        text_auto=True,
        title="Bar Chart"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# PIE CHART
# ==========================================================

if product_column and value_column:

    st.subheader("🥧 Pie Chart")

    pie = px.pie(
        chart_df,
        names=product_column,
        values=value_column,
        hole=0.4
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

# ==========================================================
# HISTOGRAM
# ==========================================================

if value_column:

    st.subheader("📈 Histogram")

    hist = px.histogram(
        df,
        x=value_column,
        nbins=20
    )

    st.plotly_chart(
        hist,
        use_container_width=True
    )

# ==========================================================
# SCATTER PLOT
# ==========================================================

if len(numeric_columns) >= 2:

    st.subheader("🔵 Scatter Plot")

    scatter = px.scatter(

        df,

        x=numeric_columns[0],

        y=numeric_columns[1],

        color=product_column if product_column else None,

        hover_data=df.columns

    )

    st.plotly_chart(
        scatter,
        use_container_width=True
    )

# ==========================================================
# BOX PLOT
# ==========================================================

if value_column:

    st.subheader("📦 Box Plot")

    box = px.box(

        df,

        y=value_column,

        points="all"

    )

    st.plotly_chart(

        box,

        use_container_width=True

    )

# ==========================================================
# STATISTICAL SUMMARY
# ==========================================================

if analysis:

    st.subheader("📑 Statistical Summary")

    if "describe" in analysis:

        st.dataframe(

            analysis["describe"],

            use_container_width=True

        )

# ==========================================================
# CORRELATION MATRIX
# ==========================================================

if analysis:

    if "correlation" in analysis:

        st.subheader("🔗 Correlation Matrix")

        st.dataframe(

            analysis["correlation"],

            use_container_width=True

        )

# ==========================================================
# QUICK STATISTICS
# ==========================================================

st.subheader("📌 Quick Statistics")

s1, s2, s3 = st.columns(3)

s1.metric(
    "Rows",
    len(df)
)

s2.metric(
    "Columns",
    len(df.columns)
)

if value_column:

    s3.metric(
        "Maximum Value",
        f"{df[value_column].max():,.2f}"
    )

else:

    s3.metric(
        "Maximum Value",
        "N/A"
    )

# ==========================================================
# AI INSIGHTS
# ==========================================================

st.subheader("🤖 AI Insights")

if insights:

    a1, a2 = st.columns(2)

    with a1:

        st.success(
            f"📈 Highest Value : {insights.get('max','N/A')}"
        )

        st.info(
            f"📊 Average Value : {insights.get('mean','N/A')}"
        )

        st.warning(
            f"❗ Missing Values : {insights.get('missing',0)}"
        )

    with a2:

        st.success(
            f"🏆 Top Category : {insights.get('top_category','N/A')}"
        )

        st.info(
            f"📄 Total Records : {insights.get('rows',len(df))}"
        )

        st.warning(
            f"🧹 Duplicate Rows : {insights.get('duplicates',0)}"
        )

# ==========================================================
# SMART RECOMMENDATIONS
# ==========================================================

st.subheader("🧠 Smart Recommendations")

recommendations = []

if missing_values > 0:
    recommendations.append(
        f"• Dataset contains {missing_values} missing values. Consider cleaning them."
    )

if duplicate_rows > 0:
    recommendations.append(
        f"• Dataset contains {duplicate_rows} duplicate rows."
    )

if len(numeric_columns) > 5:
    recommendations.append(
        "• Large numeric dataset detected. Correlation analysis is recommended."
    )

if len(text_columns) > 5:
    recommendations.append(
        "• Multiple categorical columns detected."
    )

if len(df) > 10000:
    recommendations.append(
        "• Large dataset detected. Consider filtering before analysis."
    )

if len(recommendations) == 0:

    st.success(
        "✅ Dataset looks clean and ready for analysis."
    )

else:

    for rec in recommendations:

        st.info(rec)

# ==========================================================
# TOP & BOTTOM RECORDS
# ==========================================================

if value_column:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏆 Top 10 Records")

        st.dataframe(

            df.nlargest(
                10,
                value_column
            ),

            use_container_width=True

        )

    with col2:

        st.subheader("📉 Bottom 10 Records")

        st.dataframe(

            df.nsmallest(
                10,
                value_column
            ),

            use_container_width=True

        )

# ==========================================================
# DOWNLOAD SECTION
# ==========================================================

st.subheader("📥 Downloads")

d1, d2 = st.columns(2)

try:

    with open(
        "output/cleaned_sales.xlsx",
        "rb"
    ) as file:

        d1.download_button(

            label="⬇ Download Cleaned Excel",

            data=file,

            file_name="cleaned_sales.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )

except:

    d1.info("Excel file not available.")

try:

    with open(
        "reports/sales_report.pdf",
        "rb"
    ) as file:

        d2.download_button(

            label="⬇ Download PDF Report",

            data=file,

            file_name="sales_report.pdf",

            mime="application/pdf"

        )

except:

    d2.info("PDF report not available.")

# ==========================================================
# DATASET INFORMATION
# ==========================================================

with st.expander("📋 Dataset Information"):

    st.write("Dataset Type :", dataset_type)

    st.write("Rows :", len(df))

    st.write("Columns :", len(df.columns))

    st.write("Numeric Columns")

    st.write(numeric_columns)

    st.write("Text Columns")

    st.write(text_columns)

    st.write("Date Columns")

    st.write(date_columns)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
"""
### 🚀 Excel Automation Suite Pro

Automatically Clean • Analyze • Visualize • Generate Insights

**Built with**

- Python
- Pandas
- Streamlit
- Plotly
- AI Based Dataset Detection
"""
)    