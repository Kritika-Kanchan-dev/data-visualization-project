# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Title & Description
st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")
st.title("📊 Data Visualization Dashboard")
st.write("Upload a CSV file and explore your data with interactive visualizations.")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Load Data
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Auto-detect column types
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Sidebar: auto-suggest chart types
    st.sidebar.header("Visualization Settings")

    if len(numeric_cols) > 0 and len(categorical_cols) > 0:
        default_chart = "Bar Chart"
    elif len(numeric_cols) > 1:
        default_chart = "Scatter Plot"
    elif len(numeric_cols) == 1:
        default_chart = "Histogram"
    else:
        default_chart = "Pie Chart"

    chart_type = st.sidebar.selectbox(
        "Choose a chart type:",
        [
            "Line Chart",
            "Bar Chart",
            "Scatter Plot",
            "Pie Chart",
            "Heatmap",
            "Histogram",
            "Box Plot",
            "Area Chart",
            "Violin Plot",
            "Pair Plot"
        ],
        index=[
            "Line Chart",
            "Bar Chart",
            "Scatter Plot",
            "Pie Chart",
            "Heatmap",
            "Histogram",
            "Box Plot",
            "Area Chart",
            "Violin Plot",
            "Pair Plot"
        ].index(default_chart)
    )

    # Select X & Y columns dynamically
    columns = df.columns.tolist()
    x_axis = st.sidebar.selectbox("Select X-axis:", options=columns)
    y_axis = st.sidebar.selectbox("Select Y-axis:", options=columns)

    # Generate charts
    st.subheader(f"📈 {chart_type}")

    if chart_type == "Line Chart":
        fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Chart":
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot":
        # Only color if a categorical column exists
        if categorical_cols:
            fig = px.scatter(df, x=x_axis, y=y_axis, color=categorical_cols[0], title=f"{y_axis} vs {x_axis}")
        else:
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie Chart":
        if y_axis in numeric_cols:
            fig = px.pie(df, names=x_axis, values=y_axis, title=f"Pie Chart of {y_axis} by {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pie chart requires numeric values for 'values' (Y-axis).")

    elif chart_type == "Heatmap":
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    elif chart_type == "Histogram":
        fig = px.histogram(df, x=x_axis, title=f"Histogram of {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        fig = px.box(df, x=x_axis, y=y_axis, title=f"Box Plot of {y_axis} by {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Area Chart":
        fig = px.area(df, x=x_axis, y=y_axis, title=f"Area Chart of {y_axis} vs {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Violin Plot":
        fig = px.violin(df, x=x_axis, y=y_axis, box=True, points="all", title=f"Violin Plot of {y_axis} by {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pair Plot":
        fig = sns.pairplot(df[numeric_cols[:4]])  # only numeric, limit to 4 cols
        st.pyplot(fig)

else:
    st.info("👆 Please upload a CSV file to begin.")
