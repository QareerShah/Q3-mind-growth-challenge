# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our app 
st.set_page_config(page_title="🌐Data Sweeper", layout="wide")
st.title("🌐Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your file (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")  # Ensure openpyxl is used
        else:  
            st.error(f"Unsupported file type: {file_ext}")
            continue  

        # Display file info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show first 5 rows of the dataframe
        st.write("🔎 Preview of the DataFrame")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader(f"🛠Data Cleaning Options for {file.name}")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed")

            with col2:
                if st.button(f"Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled!")

        # Select columns to keep or convert
        st.subheader("🎯Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            numeric_columns = df[columns].select_dtypes(include=["number"])
            if not numeric_columns.empty:
                st.bar_chart(numeric_columns.iloc[:, :2])
            else:
                st.warning("No numeric columns available for visualization.")

        # File Conversion
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()  # Reset buffer
            
            base_name, ext = os.path.splitext(file.name)  # Extract name and extension
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = f"{base_name}.csv"
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = f"{base_name}.xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Move pointer back to the start

            # Download button
            st.download_button(
                label=f"🔽 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name= file_name,
                mime= mime_type
            )



st.success("🎉 {file.name} Processed Successfully!")
      
