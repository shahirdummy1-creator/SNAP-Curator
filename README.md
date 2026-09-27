# SNAP Productivity Curator

A small local Python tool for reviewing product rows from an Excel file.

## Features
- Upload Excel file and read the headers automatically.
- Detect the `image_url` column and display the image on one side.
- Show all remaining attribute columns as editable inputs for manual agent curation.
- Save the updated rows locally.
- Download the finished Excel file from the app.

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal after startup.
