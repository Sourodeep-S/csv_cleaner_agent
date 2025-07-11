import streamlit as st
import pandas as pd
import os
from agents.detection_agent import detect_issues
from agents.correction_agent import correct_data
from agents.enrichment_agent import enrich_data
from utils import clear_logs

st.set_page_config(page_title="Mini Data Fixer", layout="centered")

st.title("🛠️ Mini Agent-Based Data Fixer")
st.markdown("Upload a messy CSV file and let the agents clean and enrich it!")

uploaded_file = st.file_uploader("📤 Upload CSV", type=["csv"])

if uploaded_file:
    # Save uploaded file to /data/input.csv
    with open("data/input.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded!")

    if st.button("🚀 Run Agents"):
        clear_logs()

        with st.spinner("Running Detection..."):
            detect_issues()
        with st.spinner("Running Correction..."):
            correct_data()
        with st.spinner("Running Enrichment..."):
            final_df = enrich_data()

        st.success("✅ All agents completed!")

        st.subheader("🧼 Cleaned & Enriched Data")
        st.dataframe(final_df)

        csv = final_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Cleaned CSV",
            data=csv,
            file_name="output_enriched.csv",
            mime='text/csv'
        )

        # ✅ Simple working log viewer using expander
        with st.expander("📄 View Logs"):

            def show_log_section(title, filepath):
                st.markdown(f"### {title}")
                try:
                    with open(filepath, 'r') as f:
                        lines = f.readlines()
                        preview = ''.join(lines[:5]) if len(lines) > 5 else ''.join(lines)
                        st.text_area(
                            label='',
                            value=''.join(lines),
                            height=200,
                            key=title
                        )
                except FileNotFoundError:
                    st.warning(f"{title} file not found.")

            show_log_section("🕵️ Detection Log", "logs/detection_log.txt")
            show_log_section("🛠 Correction Log", "logs/correction_log.txt")
            show_log_section("✨ Enrichment Log", "logs/enrichment_log.txt")
