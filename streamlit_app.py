# streamlit_app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

# Set page layout
st.set_page_config(page_title="📸 Attendance Dashboard", layout="wide")

st.title("📸 Smart Attendance System Dashboard")

csv_file = "attendance.csv"

# Load CSV
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Name", "Time", "Location"])
    df.to_csv(csv_file, index=False)

# Filter by date or name
with st.sidebar:
    st.header("🔍 Filters")
    names = st.multiselect("Filter by Name", options=df["Name"].unique())
    date_range = st.date_input("Date Range", [])

filtered_df = df.copy()

if names:
    filtered_df = filtered_df[filtered_df["Name"].isin(names)]

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    filtered_df["Time"] = pd.to_datetime(filtered_df["Time"])
    filtered_df = filtered_df[(filtered_df["Time"] >= start_date) & (filtered_df["Time"] <= end_date)]

st.dataframe(filtered_df, use_container_width=True)

# Export buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Export as Excel"):
        filtered_df.to_excel("filtered_attendance.xlsx", index=False)
        with open("filtered_attendance.xlsx", "rb") as f:
            st.download_button("Download Excel", data=f, file_name="attendance.xlsx")

with col2:
    if st.button("📝 Export as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Attendance Report", ln=True, align='C')
        pdf.ln(10)
        for index, row in filtered_df.iterrows():
            line = f"{row['Name']} | {row['Time']} | {row['Location']}"
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output("attendance_report.pdf")
        with open("attendance_report.pdf", "rb") as f:
            st.download_button("Download PDF", data=f, file_name="attendance.pdf")

st.success("📊 Dashboard ready!")
