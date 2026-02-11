🚀 Smart Receipt Planner

A complete end-to-end ML + OCR + NLP system for automated receipt processing and expense analytics.

📌 Overview

Smart Receipt Planner is a production-ready pipeline that:

Validates whether an uploaded image is a receipt or non-receipt

Extracts text using OCR

Normalizes and cleans raw text

Extracts key fields (vendor, date, total)

Classifies expenses using a DistilBERT transformer

Stores structured receipts in PostgreSQL

Provides detailed spend analytics (category, month, week)

This project is built with a backend-first approach using FastAPI, PostgreSQL, PyTorch, and HuggingFace Transformers.

🧠 Core Features
🔍 1. Receipt Detection (CNN)

Custom-trained ResNet18 classifier

Differentiates receipts vs non-receipts

90–95% accuracy on validation data

📝 2. OCR & Text Processing

Uses EasyOCR for multilingual text extraction

Cleans/normalizes text (case, punctuation, spacing)

Extracts key entities using regex + heuristics

💳 3. Expense Categorization (NLP)

Fine-tuned DistilBERT model

Seven categories:

food

groceries

travel

shopping

utilities

healthcare

misc

🗄️ 4. Database Storage

PostgreSQL + SQLAlchemy

Stores structured receipts:

vendor

date

total

category

raw_text

normalized_text

processed_at

📊 5. Analytics Engine

Endpoints provide:

Category-wise spend

Monthly summary

Weekly spending breakdown

📁 Project Structure
smart-receipt-planner/
│
├── app/
│   ├── api/
│   │   ├── receipts.py              # Receipt processing API
│   │   └── analytics.py             # Analytics API
│   ├── core/
│   │   └── model_loader.py          # ML model loading utilities
│   ├── db/
│   │   ├── models.py                # SQLAlchemy ORM models
│   │   ├── session.py               # DB connection
│   │   └── crud.py                  # DB operations
│   ├── schemas/
│   │   └── receipt.py               # Pydantic schemas
│   ├── services/
│   │   ├── receipt_services.py      # Receipt service layer
│   │   └── receipt_processing.py    # Full pipeline orchestration
│   ├── ml/
│   │   ├── receipt_validator.py     # CNN model + inference logic
│   │   ├── ocr/                     # OCR + text normalization
│   │   │   ├── ocr_reader.py
│   │   │   ├── text_cleaning.py
│   │   │   └── extract_entities.py
│   │   └── expense_classifier/      # DistilBERT classifier
│   │       ├── inference.py
│   │       ├── config.json
│   │       ├── model.safetensors
│   │       ├── tokenizer.json
│   │       └── label_map.json
│   ├── utils/
│   │   └── analytics.py             # Weekly/monthly/category summary
│   └── main.py                      # FastAPI application entrypoint
│
├── models/
│   └── receipt_validator_resnet18.pth
│
├── notebooks/
│   ├── analytics_testing.ipynb
│   ├── expense_categorization.ipynb
│   ├── experiments.ipynb
│   └── ocr_text_structuring.ipynb
│
├── data/
│   └── dataset.csv                  # Expense classifier dataset
│
├── temp/                            # Temporary files
├── requirements.txt
├── Dockerfile                       # (phase 6)
└── README.md

⚙️ Tech Stack

Backend: FastAPI, Uvicorn

ML: PyTorch, ResNet18, DistilBERT

OCR: EasyOCR

Database: PostgreSQL, SQLAlchemy

Other: Pandas, NumPy, Regex, Docker

🚀 How It Works (Pipeline)
 Image Upload
      ↓
 Receipt Detector (ResNet18)
      ↓
      If receipt:
          ↓
          OCR (EasyOCR)
          ↓
          Text Cleaning
          ↓
          Entity Extraction (Vendor, Date, Total)
          ↓
          BERT Expense Classifier
          ↓
      Save to PostgreSQL
      ↓
      Analytics Endpoints

🔌 API Endpoints
🧾 Process Receipt

POST /receipt/process

Uploads image → full pipeline → returns:

{
  "receipt_id": "...",
  "vendor": "dominos",
  "date": "2024-12-06",
  "total": 620.0,
  "category": "food",
  "raw_text": [...],
  "normalized_text": [...],
  "category_confidence": 0.78
}

📊 Analytics Endpoints
Category Breakdown

GET /analytics/category

Monthly Summary

GET /analytics/monthly?month=YYYY-MM

Weekly Spending

GET /analytics/weekly

🛢️ Setup & Installation
1. Clone Repo
git clone <repo-url>
cd smart-receipt-planner

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate
# or venv\Scripts\activate on Windows

3. Install Requirements
pip install -r requirements.txt

4. Run PostgreSQL

Install PostgreSQL and create database:

CREATE DATABASE receipt_db;


Set environment variable (optional):

DATABASE_URL=postgresql://postgres:password@localhost:5432/receipt_db

5. Start FastAPI Server
uvicorn app.main:app --reload

🧪 Model Training & Notebooks

Development notebooks are included under notebooks/:

- `analytics_testing.ipynb` - Testing analytics endpoints and queries
- `expense_categorization.ipynb` - Expense classifier training/testing
- `experiments.ipynb` - General experiments and prototyping
- `ocr_text_structuring.ipynb` - OCR pipeline development

Models are saved in:
- `models/` - Receipt validator (ResNet18)
- `app/ml/expense_classifier/` - DistilBERT model files