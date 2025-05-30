 OCR-Based Bill Processing API (Backend Only)

This is a backend-only project built with FastAPI that allows users to upload scanned or photographed bills (in `.jpg`, `.png`, `.pdf` formats), performs OCR (Optical Character Recognition) using Tesseract, and returns structured JSON data containing:

- Purchase Date
- Total Amount
- List of Items
- Category (e.g., Grocery, Travel)

---

  Features

 Upload multiple image/PDF bills
 Perform OCR using Tesseract
 Extract key data using regex parsing
 Return structured JSON response
 Built with FastAPI, runs locally

---

 Tech Stack

Python
FastAPI
Tesseract OCR (`pytesseract`)
PyMuPDF (`fitz`)
Pillow (PIL)

---

 Installation & Setup

Clone the repository

```bash
git clone https://github.com/your-username/ocr-bill-processing-api.git
cd ocr-bill-processing-api

3)Install dependencies
pip install -r requirements.txt

4)Run the FastAPI server
uvicorn main:app --reload
Open Swagger UI at:
http://127.0.0.1:8000/docs

5) API Endpoints
POST /upload-bills/
Upload one or more .jpg, .png, or .pdf files

Returns parsed data in JSON format

GET /get-bill/{bill_id}
Fetches the parsed result using a unique bill ID

6)📄 Sample Output
json
Copy
Edit
{
  "bill_id": "a3f9bcd2-1234-4567-89ef-abcd1234efgh",
  "filename": "bill_01.pdf",
  "data": {
    "purchase_date": "28/05/2025",
    "total_amount": "129.99",
    "items": [
      { "name": "Milk 2 x 25", "price": null },
      { "name": "Bread 1 x 29.99", "price": null }
    ],
    "category": "Grocery"
  }
}
7) Notes
OCR accuracy depends on image clarity and format.

Currently uses simple keyword-based category inference.

Files are processed temporarily and deleted after extraction.




