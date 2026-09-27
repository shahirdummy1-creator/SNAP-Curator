import re
import time
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

try:
    import pytesseract
    from PIL import Image
except Exception:
    pytesseract = None
    Image = None

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="SNAP Curator", page_icon="🖼️", layout="wide")


def ensure_time_columns(df):
    if "row_completion_time_sec" not in df.columns:
        df["row_completion_time_sec"] = pd.Series([None] * len(df), dtype="float64")
    else:
        df["row_completion_time_sec"] = pd.to_numeric(df["row_completion_time_sec"], errors="coerce")
    return df


@st.cache_data
def load_excel(file_bytes: bytes, filename: str):
    buffer = BytesIO(file_bytes)
    temp_df = pd.read_excel(buffer)
    temp_df = temp_df.fillna("")
    return ensure_time_columns(temp_df)


def clean_ocr_text(text):
    if not text:
        return ""
    return " ".join(str(text).replace("\r", "\n").split())


def extract_ocr_text(image_url):
    if not image_url:
        return ""
    try:
        response = requests.get(image_url, timeout=20)
        response.raise_for_status()
    except Exception:
        return ""

    if Image is None or pytesseract is None:
        return ""

    try:
        image = Image.open(BytesIO(response.content)).convert("RGB")
        return clean_ocr_text(pytesseract.image_to_string(image))
    except Exception:
        return ""


def suggest_attribute_value(attribute_name, ocr_text):
    cleaned = clean_ocr_text(ocr_text)
    lowered = str(attribute_name).lower()

    if "raw" in lowered and "text" in lowered:
        return cleaned

    if "value" in lowered:
        match = re.search(r"([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", cleaned)
        if match:
            return match.group(1)
        return ""

    if "unit" in lowered:
        match = re.search(r"(?:\d+\.?\d*\s*)([A-Za-z%/µ°]+)", cleaned)
        if match:
            return match.group(1)
        return ""

    if "text" in lowered:
        return cleaned

    match = re.search(r"([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*([A-Za-z%/µ°]+)?", cleaned)
    if match:
        if match.group(2):
            return f"{match.group(1)} {match.group(2)}".strip()
        return match.group(1)
    return cleaned


def get_image_column(columns):
    for col in columns:
        if col.lower() == "image_url":
            return col
    lowered = [col.lower() for col in columns]
    for index, col_name in enumerate(columns):
        if "image" in lowered[index] and "url" in lowered[index]:
            return col_name
    for col_name in columns:
        if "url" in col_name.lower():
            return col_name
    return None


def get_effective_attributes(columns, image_col):
    hidden_names = {"wpid", "item id", "item_id", "product_type", "product type", "row_completion_time_sec"}
    filtered = [
        col for col in columns
        if col != image_col and str(col).strip().lower() not in hidden_names
    ]

    ops_first = []
    remaining = []
    for col in filtered:
        lowered = str(col).lower()
        if "ops" in lowered and "flag" in lowered:
            ops_first.append(col)
        else:
            remaining.append(col)

    return ops_first + remaining


st.title("SNAP Productivity Curator")
st.caption("Upload an Excel file, review each image, and fill in the missing attribute data.")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

if uploaded_file is None:
    st.info("Please upload an Excel file to begin.")
    st.stop()

uploaded_name = uploaded_file.name
excel_bytes = uploaded_file.getvalue()

if "excel_df" not in st.session_state or st.session_state.get("uploaded_name") != uploaded_name:
    st.session_state.excel_df = load_excel(excel_bytes, uploaded_name)
    st.session_state.uploaded_name = uploaded_name
    st.session_state.current_row = 0
    st.session_state.completed_rows = set()
    st.session_state.row_started_at = time.time()
    st.session_state.last_row_index = None


df = st.session_state.excel_df

if df.empty:
    st.warning("The uploaded file is empty. Please upload a file with at least one row.")
    st.stop()

all_columns = list(df.columns)
image_col = get_image_column(all_columns)

if image_col is None:
    st.error("No image URL column was detected. Please make sure your file contains a column named 'image_url'.")
    st.stop()

attribute_columns = get_effective_attributes(all_columns, image_col)

if not attribute_columns:
    st.warning("No editable attribute columns are available after hiding fixed metadata fields.")
    st.stop()

if "attribute_index" not in st.session_state:
    st.session_state.attribute_index = 0

row_count = len(df)
current_row = st.session_state.current_row

if st.session_state.get("last_row_index") != current_row:
    st.session_state.row_started_at = time.time()
    st.session_state.last_row_index = current_row

row_data = df.iloc[current_row].to_dict()
image_url = str(row_data.get(image_col, "")).strip()
ocr_text = extract_ocr_text(image_url)

prev_col, next_col = st.columns([1, 1])
with prev_col:
    if st.button("Previous row", disabled=current_row == 0):
        if current_row > 0:
            st.session_state.current_row = current_row - 1
            st.session_state.attribute_index = 0
            st.rerun()

with next_col:
    if st.button("Next row", disabled=current_row >= row_count - 1):
        if current_row < row_count - 1:
            st.session_state.current_row = current_row + 1
            st.session_state.attribute_index = 0
            st.rerun()

st.caption(f"Row {current_row + 1} of {row_count}")

left_col, right_col = st.columns([1.1, 1.5])

with left_col:
    st.subheader(f"Image for row {current_row + 1}")
    if image_url:
        st.image(image_url, use_container_width=True)
    else:
        st.info("No image URL found for this row.")

with right_col:
    st.subheader("Manual attribute review")
    current_attr = attribute_columns[st.session_state.attribute_index]
    current_value = row_data.get(current_attr, "")
    default_value = "" if pd.isna(current_value) else str(current_value)
    suggested_value = suggest_attribute_value(current_attr, ocr_text)
    if not default_value and suggested_value:
        default_value = suggested_value

    with st.form(key=f"curation_form_{current_row}_{current_attr}"):
        value_input = st.text_input(current_attr, value=default_value)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            prev_attr = st.form_submit_button("Previous attribute")
        with col2:
            next_attr = st.form_submit_button("Next attribute")
        with col3:
            complete_row = st.form_submit_button("Complete row")

    if prev_attr or next_attr or complete_row:
        df[current_attr] = df[current_attr].astype("object")
        cleaned_value = str(value_input).strip()
        df.at[current_row, current_attr] = cleaned_value if cleaned_value else pd.NA
        st.session_state.excel_df = df

        if prev_attr:
            if st.session_state.attribute_index > 0:
                st.session_state.attribute_index -= 1
            else:
                st.session_state.attribute_index = max(len(attribute_columns) - 1, 0)
            st.rerun()

        if next_attr:
            if st.session_state.attribute_index < len(attribute_columns) - 1:
                st.session_state.attribute_index += 1
            else:
                st.session_state.attribute_index = 0
            st.rerun()

        if complete_row:
            row_elapsed = time.time() - st.session_state.row_started_at
            df["row_completion_time_sec"] = pd.to_numeric(df["row_completion_time_sec"], errors="coerce")
            df.at[current_row, "row_completion_time_sec"] = round(float(row_elapsed), 2)
            st.session_state.completed_rows.add(current_row)
            st.session_state.excel_df = df

            if current_row < row_count - 1:
                st.session_state.current_row = current_row + 1
                st.session_state.attribute_index = 0
                st.session_state.row_started_at = time.time()
                st.session_state.last_row_index = current_row + 1
                st.rerun()

    if current_row in st.session_state.completed_rows:
        st.info(f"Completed: {df.at[current_row, 'row_completion_time_sec']} seconds")

    if ocr_text:
        st.caption(f"Suggested OCR text: {ocr_text[:200]}{'...' if len(ocr_text) > 200 else ''}")

    st.caption(f"Attribute {st.session_state.attribute_index + 1} of {len(attribute_columns)}")

st.markdown("---")

if st.button("Save finished file locally"):
    export_df = df.copy()
    if "row_completion_time_sec" in export_df.columns:
        export_df["row_completion_time_sec"] = pd.to_numeric(export_df["row_completion_time_sec"], errors="coerce")
    output_path = OUTPUT_DIR / f"{uploaded_name.rsplit('.', 1)[0]}_curated.xlsx"
    export_df.to_excel(output_path, index=False)
    st.success(f"Saved locally to: {output_path}")

    with open(output_path, "rb") as file:
        st.download_button(
            label="Download completed Excel file",
            data=file.read(),
            file_name=output_path.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
