```python
import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="TXT to Excel Converter",
    layout="centered"
)

st.title("TXT to Excel Converter")
st.write(
    "Upload multiple tab-separated TXT files, "
    "select columns, and download them as one Excel file."
)


@st.cache_data
def read_txt(file_bytes):
    return pd.read_csv(
        io.BytesIO(file_bytes),
        sep="\t",
        header=0
    )


def convert_multiple_to_excel(dataframes):
    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        for sheet_name, df in dataframes.items():
            df.to_excel(
                writer,
                index=False,
                sheet_name=sheet_name[:31]
            )

    return excel_buffer.getvalue()


# ==========================================
# UPLOAD MULTIPLE FILE
# ==========================================

uploaded_files = st.file_uploader(
    "Pilih file TXT",
    type="txt",
    accept_multiple_files=True
)


if uploaded_files:

    st.success(
        f"{len(uploaded_files)} file berhasil dipilih."
    )

    processed_data = {}

    # ==========================================
    # PROSES SETIAP FILE
    # ==========================================

    for uploaded_file in uploaded_files:

        st.divider()

        st.subheader(
            f"📄 {uploaded_file.name}"
        )

        try:

            file_bytes = uploaded_file.getvalue()

            with st.spinner(
                f"Membaca {uploaded_file.name}..."
            ):

                df = read_txt(file_bytes)

            st.success(
                f"Berhasil dibaca: "
                f"{len(df):,} baris × "
                f"{len(df.columns)} kolom"
            )

            # ==========================================
            # PREVIEW
            # ==========================================

            st.write("**Pratinjau Data**")

            st.dataframe(
                df.head(10),
                use_container_width=True
            )

            # ==========================================
            # PILIH KOLOM
            # ==========================================

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
                col
                for col in default_columns
                if col in all_columns
            ]

            if not default_selected_columns:

                default_selected_columns = all_columns[
                    :min(6, len(all_columns))
                ]

            selected_columns = st.multiselect(
                f"Pilih kolom untuk {uploaded_file.name}:",
                options=all_columns,
                default=default_selected_columns,
                key=f"columns_{uploaded_file.name}"
            )

            if selected_columns:

                df_selected = df[selected_columns]

                st.write(
                    "**Pratinjau Data Terpilih**"
                )

                st.dataframe(
                    df_selected.head(10),
                    use_container_width=True
                )

                # Nama sheet berdasarkan nama file
                sheet_name = uploaded_file.name.rsplit(
                    ".", 1
                )[0]

                # Bersihkan karakter yang tidak boleh
                # digunakan pada nama sheet Excel
                invalid_chars = [
                    "\\", "/", "*", "[", "]", ":", "?"
                ]

                for char in invalid_chars:
                    sheet_name = sheet_name.replace(
                        char, "_"
                    )

                sheet_name = sheet_name[:31]

                processed_data[sheet_name] = df_selected

            else:

                st.warning(
                    f"Belum ada kolom yang dipilih "
                    f"untuk {uploaded_file.name}."
                )

        except Exception as e:

            st.error(
                f"Gagal memproses "
                f"{uploaded_file.name}: {e}"
            )

            st.warning(
                "Pastikan file TXT menggunakan "
                "pemisah TAB dan memiliki header."
            )


    # ==========================================
    # DOWNLOAD EXCEL
    # ==========================================

    if processed_data:

        st.divider()

        st.subheader("📊 Hasil Konversi")

        st.write(
            f"{len(processed_data)} file siap "
            "dikonversi ke Excel."
        )

        with st.spinner(
            "Membuat file Excel..."
        ):

            excel_data = convert_multiple_to_excel(
                processed_data
            )

        st.download_button(
            label="⬇️ Download Semua File ke Excel",
            data=excel_data,
            file_name="converted_data.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

        st.success(
            "File Excel berhasil dibuat dan siap diunduh!"
        )

else:

    st.info(
        "Silakan unggah satu atau beberapa file .txt "
        "untuk memulai."
    )
```
