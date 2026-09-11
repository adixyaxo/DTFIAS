import pandas as pd
from docx import Document
import sys
import json
import traceback

def extract_excel(filepath):
    try:
        # Load the excel file, extracting all sheets
        xls = pd.ExcelFile(filepath)
        data = {}
        for sheet in xls.sheet_names:
            df = pd.read_excel(filepath, sheet_name=sheet)
            # convert dataframe to a string or dict
            data[sheet] = df.to_dict(orient='records')
        return data
    except Exception as e:
        return f"Error reading excel: {e}\n{traceback.format_exc()}"

def extract_docx(filepath):
    try:
        doc = Document(filepath)
        text = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(text)
    except Exception as e:
        return f"Error reading docx: {e}\n{traceback.format_exc()}"

if __name__ == "__main__":
    excel_file = "docs/data/Bharati_Research_Station_Technical_Numerical_Data_Repository.xlsx"
    docx_file = "docs/data/Untitled document.docx"
    
    res = {
        "docx": extract_docx(docx_file),
        "excel": extract_excel(excel_file)
    }
    
    with open("scratch/data_dump.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, default=str)
    print("Extraction saved to scratch/data_dump.json")
