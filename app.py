import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_titl:any == "DATA SWEEPER" ,layout='centered') # type: ignore

#customcss
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white ;
        }
        </style>
    
    """
    unsafe_allow_html=True
)
 
#title and decsription
st.title("Data Sweeper Sterling Integrator")
st.write("Transfrom your files between CSV and Excel formats wityh built-in data cleaning and visualization creating the project for quarter 3! ")

#file uploader
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx" ],accept_multiple_files=(True))

if uploaded_file :
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"File type not supported: {file_ext}")
            continue
        
        #file details  
        st.write("Previex the head of the Data Frame")
        st.dataframe(df.head())

        #data cleaning options
        st.subheader("Dta Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
           col1, col2 = st.columns(2)
            
           with col1:
                if st.button(f"Remove duplicates from the file; {file.name}"):
                    df = df.drop_duplicates(inplace=True)
                    st.write("Duplicates removd!")
           with col2:
                if st.button(f"Missing values from the file; {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled!")

        st.subheader("Select columns to keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visuailization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='numbers').iloc[:, :2])

        #convversion options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Covert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name=file.name.replace(file_ext, ".csv")
                mime_type= "text/csv"
            elif conversion_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name=file.name.replace(file_ext, ".xlsx")
                mime_type= "application/vnd.openxmlformats-officedocuments.spreadsheetml.sheet"
            buffer.seek(0)  

            st.download_button(
                label=f"Download {file_name}",
                data=buffer, 
                file_name=file_name,
                mime=mime_type
            )

st.success("all files processed successfully!")    
    



 
