import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="TXT to Excel Converter",
    layout="centered"
)

st.title("TXT to Excel Converter")
st.write("Upload your tab-separated TXT file, select columns, and download as Excel.")


@st.cache_data
def read_txt(file_bytes):
    return pd.read_csv(
        io.BytesIO(file_bytes),
        sep="\t",
        header=0
    )


@st.cache_data
def convert_to_excel(df):
    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Selected Data"
        )

    return excel_buffer.getvalue()


uploaded_file = st.file_uploader(
    "Pilih file TXT",
    type="txt"
)


if uploaded_file is not None:

    try:
        # Baca file hanya sekali dan gunakan cache
        file_bytes = uploaded_file.getvalue()

        with st.spinner("Membaca file TXT..."):
            df = read_txt(file_bytes)

        st.success(
            f"File berhasil dibaca! "
            f"{len(df):,} baris × {len(df.columns)} kolom"
        )

        st.write("### Pratinjau Data Asli")
        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        # Daftar kolom
        all_columns = df.columns.tolist()

        default_columns = [
            "Age",
            "Gender",
            "Credit_Score",
            "Loan_Term_Months",
            "Interest_Rate",
            "Marital_Status"
        ]

        default_selected_columns = [
            col for col in default_columns
            if col in all_columns
        ]

        if not default_selected_columns:
            default_selected_columns = all_columns[
                :min(6, len(all_columns))
            ]

        selected_columns = st.multiselect(
            "Pilih kolom yang ingin disertakan:",
            options=all_columns,
            default=default_selected_columns
        )

        if selected_columns:

            df_selected = df[selected_columns]

            st.write("### Pratinjau Data Terpilih")

            st.dataframe(
                df_selected.head(10),
                use_container_width=True
            )

            # Convert Excel
            with st.spinner("Membuat file Excel..."):
                excel_data = convert_to_excel(
                    df_selected
                )

            st.download_button(
                label="⬇️ Download Excel File",
                data=excel_data,
                file_name="selected_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.success("File Excel siap diunduh!")

        else:
            st.warning(
                "Mohon pilih setidaknya satu kolom."
            )

    except Exception as e:

        st.error(
            f"Terjadi kesalahan saat memproses file: {e}"
        )

        st.warning(
            "Pastikan file berformat TXT dengan "
            "pemisah tab dan memiliki header."
        )

else:

    st.info(
        "Silakan unggah file .txt untuk memulai."
    )
