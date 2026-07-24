import streamlit as st
import pandas as pd
import plotly.express as px

from modules.cleaner import clean_dataframe
from modules.dataset_detector import detect_dataset
from modules.insights import generate_insights
from modules.advanced_analysis import advanced_analysis
from modules.pdf_generator import generate_pdf_report
from modules.excel_export import export_excel_report

from modules.database import (
    create_database,
    save_upload,
    load_history
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Excel Automation Suite Pro",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Excel Automation Suite Pro")
create_database()
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

# ==========================================================
# SAVE HISTORY
# ==========================================================

file_name = (
    uploaded_file.name
    if uploaded_file
    else "cleaned_sales.xlsx"
)

save_upload(

    filename=file_name,

    dataset_type=dataset_type,

    rows=len(df),

    columns=len(df.columns),

    missing=int(df.isnull().sum().sum()),

    duplicates=int(df.duplicated().sum())

)

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


if product_column and value_column:

    insights = generate_insights(
        df,
        value_column,
        product_column
    )

else:

    insights = None

generate_pdf_report(

    output_path="reports/sales_report.pdf",

    dataset_type=dataset_type,

    rows=len(df),

    columns=len(df.columns),

    missing=missing_values,

    duplicates=duplicate_rows,

    insights=insights

)    

analysis = advanced_analysis(df)


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
# ADVANCED VISUAL ANALYTICS
# ==========================================================

st.subheader("📊 Advanced Visual Analytics")

if value_column:

    tab1, tab2, tab3 = st.tabs(
        [
            "📈 Line Chart",
            "📦 Box Plot",
            "📉 Distribution"
        ]
    )

    # -----------------------------
    # Line Chart
    # -----------------------------

    with tab1:

        line_chart = px.line(
            df,
            x=df.index,
            y=value_column,
            markers=True,
            title=f"{value_column} Trend"
        )

        st.plotly_chart(
            line_chart,
            use_container_width=True
        )

    # -----------------------------
    # Box Plot
    # -----------------------------

    with tab2:

        box_chart = px.box(
            df,
            y=value_column,
            points="outliers",
            title=f"{value_column} Outlier Detection"
        )

        st.plotly_chart(
            box_chart,
            use_container_width=True
        )

    # -----------------------------
    # Histogram
    # -----------------------------

    with tab3:

        histogram = px.histogram(
            df,
            x=value_column,
            nbins=30,
            title=f"{value_column} Distribution"
        )

        st.plotly_chart(
            histogram,
            use_container_width=True
        )

# ==========================================================
# ADVANCED DATA QUALITY ANALYSIS
# ==========================================================

st.subheader("🧠 Data Quality Analysis")

c1, c2 = st.columns(2)

# ----------------------------------
# Missing Values
# ----------------------------------

with c1:

    missing_df = (
        df.isnull()
        .sum()
        .reset_index()
    )

    missing_df.columns = [
        "Column",
        "Missing"
    ]

    missing_df = missing_df[
        missing_df["Missing"] > 0
    ]

    if len(missing_df):

        fig = px.bar(
            missing_df,
            x="Column",
            y="Missing",
            color="Missing",
            title="Missing Values by Column"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.success("✅ No Missing Values Found")


# ----------------------------------
# Duplicate Information
# ----------------------------------

with c2:

    duplicate_count = int(df.duplicated().sum())

    st.metric(
        "Duplicate Rows",
        duplicate_count
    )

    st.metric(
        "Duplicate Percentage",
        f"{duplicate_count/max(len(df),1)*100:.2f}%"
    )

    st.metric(
        "Unique Rows",
        len(df)-duplicate_count
    )


# ==========================================================
# OUTLIER DETECTION
# ==========================================================

if value_column:

    st.subheader("🚨 Outlier Detection")

    q1 = df[value_column].quantile(0.25)
    q3 = df[value_column].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[
        (df[value_column] < lower)
        |
        (df[value_column] > upper)
    ]

    st.metric(
        "Outliers Found",
        len(outliers)
    )

    if len(outliers):

        st.dataframe(
            outliers,
            width="stretch"
        )

    else:

        st.success("✅ No Outliers Detected")


# ==========================================================
# COLUMN INFORMATION
# ==========================================================

st.subheader("📑 Dataset Schema")

schema = pd.DataFrame({

    "Column": df.columns,

    "Data Type":
    [
        str(df[col].dtype)
        for col in df.columns
    ],

    "Unique Values":
    [
        df[col].nunique()
        for col in df.columns
    ],

    "Missing":
    [
        df[col].isna().sum()
        for col in df.columns
    ]

})

st.dataframe(
    schema,
    width="stretch"
)        

# ==========================================================
# EXECUTIVE BUSINESS DASHBOARD
# ==========================================================

st.subheader("📈 Executive Business Dashboard")

k1, k2, k3, k4 = st.columns(4)

memory_usage = (
    df.memory_usage(deep=True).sum()
    / 1024
)

numeric_count = len(
    df.select_dtypes(include="number").columns
)

text_count = len(
    df.select_dtypes(include="object").columns
)

quality_score = round(
    (
        1
        -
        (
            missing_values
            /
            max(df.size, 1)
        )
    )
    * 100,
    2
)

k1.metric(
    "Dataset Size",
    f"{memory_usage:.1f} KB"
)

k2.metric(
    "Numeric Columns",
    numeric_count
)

k3.metric(
    "Text Columns",
    text_count
)

k4.metric(
    "Data Quality",
    f"{quality_score}%"
)

# ==========================================================
# COLUMN SUMMARY
# ==========================================================

st.subheader("📋 Column Summary")

summary = pd.DataFrame({

    "Column": df.columns,

    "Datatype":
    [
        str(df[c].dtype)
        for c in df.columns
    ],

    "Missing":
    [
        int(df[c].isna().sum())
        for c in df.columns
    ],

    "Unique":
    [
        int(df[c].nunique())
        for c in df.columns
    ]

})

st.dataframe(
    summary,
    width="stretch"
)

# ==========================================================
# MEMORY ANALYSIS
# ==========================================================

st.subheader("💾 Memory Usage")

memory_df = pd.DataFrame({

    "Column": df.columns,

    "Memory (KB)":
    [
        df[c].memory_usage(deep=True)/1024
        for c in df.columns
    ]

})

fig = px.bar(

    memory_df,

    x="Column",

    y="Memory (KB)",

    color="Memory (KB)",

    title="Memory Used by Each Column"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# DATA HEALTH SCORE
# ==========================================================

st.subheader("🩺 Data Health Score")

health_score = 100

health_score -= duplicate_rows * 2

health_score -= missing_values

health_score = max(0, min(100, health_score))

h1, h2 = st.columns([1, 3])

with h1:

    st.metric(
        "Health Score",
        f"{health_score}%"
    )

with h2:

    st.progress(health_score / 100)

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.subheader("📝 Executive Summary")

summary = []

summary.append(f"Dataset Type : {dataset_type}")

summary.append(f"Rows : {len(df)}")

summary.append(f"Columns : {len(df.columns)}")

summary.append(f"Missing Values : {missing_values}")

summary.append(f"Duplicate Rows : {duplicate_rows}")

if value_column:

    summary.append(
        f"Maximum {value_column} : {df[value_column].max():,.2f}"
    )

    summary.append(
        f"Average {value_column} : {df[value_column].mean():,.2f}"
    )

st.info("\n".join(summary))

# ==========================================================
# BUSINESS RECOMMENDATIONS
# ==========================================================

st.subheader("💡 AI Business Recommendations")

recommendations = []

if missing_values > 0:
    recommendations.append(
        "• Clean missing values before reporting."
    )

if duplicate_rows > 0:
    recommendations.append(
        "• Remove duplicate rows to improve accuracy."
    )

if len(numeric_columns) > 5:
    recommendations.append(
        "• Perform correlation analysis for better insights."
    )

if value_column:

    if df[value_column].std() > df[value_column].mean():

        recommendations.append(
            "• High variation detected in numeric values."
        )

if not recommendations:

    st.success(
        "✅ Dataset quality looks excellent."
    )

else:

    for rec in recommendations:

        st.write(rec)

# ==========================================================
# EXPORT READY STATUS
# ==========================================================

st.subheader("📦 Export Status")

ready = (
    missing_values == 0
    and
    duplicate_rows == 0
)

if ready:

    st.success(
        "✅ Dataset is ready for reporting and export."
    )

else:

    st.warning(
        "⚠ Dataset should be cleaned before final reporting."
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
# GENERATE PROFESSIONAL EXCEL REPORT
# ==========================================================

excel_report_path = export_excel_report(

    df=df,

    cleaning_report=cleaning_report,

    insights=insights,

    output_path="reports/final_report.xlsx"

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
        "reports/final_report.xlsx",
        "rb"
    ) as file:

        d1.download_button(

            label="⬇ Download Cleaned Excel",

            data=file,

            file_name="cleaned_sales.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )

except FileNotFoundError:

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

except FileNotFoundError:

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

# ==========================================================
# UPLOAD HISTORY
# ==========================================================

st.divider()

st.subheader("🗄 Upload History")

history = load_history()

if history:

    history_df = pd.DataFrame(

        history,

        columns=[

            "ID",

            "Filename",

            "Upload Time",

            "Dataset",

            "Rows",

            "Columns",

            "Missing",

            "Duplicates"

        ]

    )

    st.dataframe(

        history_df,

        use_container_width=True,

        height=300

    )

else:

    st.info(
        "No Upload History Found."
    )