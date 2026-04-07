import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
prompt = st.text_area("Describe the chart you want")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    if st.button("Generate") and prompt:
        try:
            spec = get_chart_spec(df, prompt)
            validate_chart_spec(spec, df)

            st.subheader("Generated chart spec")
            st.json(spec)

            fig = build_chart(df, spec)   # your Plotly builder
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Could not generate chart: {e}")
