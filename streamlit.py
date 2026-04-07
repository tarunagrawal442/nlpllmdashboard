import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title("NLP Data Dashboard")

uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])
user_prompt = st.text_area("What do you want to visualize?")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview")
    st.dataframe(df.head())

    st.subheader("Columns")
    st.write({col: str(df[col].dtype) for col in df.columns})

    if st.button("Generate Visualization") and user_prompt:
        # Replace this with actual LLM call
        mock_spec = {
            "chart_type": "bar",
            "x": df.columns[0],
            "y": df.columns[1] if len(df.columns) > 1 else None,
            "color": None,
            "aggregation": "sum",
            "filters": [],
            "title": user_prompt
        }

        fig = None

        if mock_spec["chart_type"] == "bar":
            temp = df.groupby(mock_spec["x"])[mock_spec["y"]].sum().reset_index()
            fig = px.bar(temp, x=mock_spec["x"], y=mock_spec["y"], title=mock_spec["title"])

        if fig:
            st.plotly_chart(fig, use_container_width=True)
            st.json(mock_spec)