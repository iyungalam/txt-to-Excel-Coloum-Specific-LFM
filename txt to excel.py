%%writefile app.py
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="TXT to Excel Converter", layout="centered")
st.title("TXT to Excel Converter")
st.write("Upload your tab-separated TXT file, select columns, and download as Excel.")

uploaded_file = st.file_uploader("Pilih file TXT", type="txt")

if uploaded_file is not None:
    # Read the text file into a pandas DataFrame
    try:
        # Assuming tab-separated values and a header row
        df = pd.read_csv(uploaded_file, sep='\t', header=0)
        st.success("File TXT berhasil dibaca!")
        st.write("**Pratinjau Data Asli:**")
        st.dataframe(df.head())

        # Allow user to select columns
        all_columns = df.columns.tolist()
        default_selected_columns = [col for col in ['Age', 'Gender', 'Credit_Score', 'Loan_Term_Months', 'Interest_Rate', 'Marital_Status'] if col in all_columns]

        # If default columns are not found, pre-select the first few available columns
        if not default_selected_columns and len(all_columns) > 0:
            default_selected_columns = all_columns[:min(6, len(all_columns))]

        selected_columns = st.multiselect(
            "Pilih kolom yang ingin disertakan dalam file Excel:",
            options=all_columns,
            default=default_selected_columns
        )

        if selected_columns:
            df_selected = df[selected_columns]
            st.write("**Pratinjau Data Terpilih:**")
            st.dataframe(df_selected.head())

            # Convert DataFrame to Excel in-memory
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df_selected.to_excel(writer, index=False, sheet_name='Selected Data')
            excel_buffer.seek(0)

            st.download_button(
                label="Download Excel File",
                data=excel_buffer,
                file_name="selected_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("File Excel Anda siap untuk diunduh!")
        else:
            st.warning("Mohon pilih setidaknya satu kolom.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
        st.warning("Pastikan file Anda berformat TXT yang dipisahkan oleh tab dan memiliki baris header.")
else:
    st.info("Silakan unggah file .txt Anda untuk memulai.")