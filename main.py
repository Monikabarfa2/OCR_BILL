from fastapi import FastAPI, UploadFile, File
from typing import List
import shutil
import uuid
import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import re

# Set path if Tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()
data_store = {}

@app.post("/upload-bills/")
async def upload_bills(files: List[UploadFile] = File(...)):
    results = []
    
    for file in files:
        try:
            file_id = str(uuid.uuid4())
            file_path = f"temp_{file_id}_{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Extract text via OCR
            if file.filename.lower().endswith(".pdf"):
                extracted_text = ""
                pdf_doc = fitz.open(file_path)
                for page in pdf_doc:
                    pix = page.get_pixmap()
                    img_path = f"{file_id}_page.png"
                    pix.save(img_path)
                    extracted_text += pytesseract.image_to_string(Image.open(img_path))
                    os.remove(img_path)
                pdf_doc.close()
            else:
                extracted_text = pytesseract.image_to_string(Image.open(file_path))

            os.remove(file_path)

            # Parse structured bill data
            structured_data = parse_bill_data(extracted_text)

            # Save in memory
            data_store[file_id] = {
                "filename": file.filename,
                "structured_data": structured_data
            }

            # Prepare output
            results.append({
                "bill_id": file_id,
                "filename": file.filename,
                "data": structured_data
            })

        except Exception as e:
            return {"error": str(e)}

    return {"processed": results}


def parse_bill_data(text):
    date_match = re.search(r"\d{2}/\d{2}/\d{4}", text)
    total_match = re.search(r"(?i)total\s*[:\-]?\s*₹?\s*(\d+[\.,]?\d{0,2})", text)
    lines = text.split('\n')
    items = [{"name": line.strip(), "price": None} for line in lines if re.search(r"\d+\.\d{2}", line)]

    if any(kw in text.lower() for kw in ["grocery", "milk", "bread"]):
        category = "Grocery"
    elif any(kw in text.lower() for kw in ["travel", "uber", "driver"]):
        category = "Travel"
    else:
        category = "Others"

    return {
        "purchase_date": date_match.group() if date_match else None,
        "total_amount": total_match.group(1) if total_match else None,
        "items": items,
        "category": category
    }
