# MetaForensic  
Advanced Metadata & Forensic Analysis Tool
Filed named as MetaForensic - Advanced Metadata Analysis demo.pdf contains the preview of the output ...

---

## ✨ Features
- **Metadata Extraction**: Filesystem timestamps, permissions, PDF/DOCX/XLSX/PPTX metadata  
- **Forensic Checks**: Date anomalies, metadata stripping, suspicious patterns  
- **Risk Score**: 0–10 with High/Medium/Low severity  
- **UI**: Drag–drop upload, real-time analysis, JSON export, batch processing  

---

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
# Runs on: http://localhost:8000
```

### Frontend

```bash
cd frontend
python -m http.server 3000
# Runs on: http://localhost:3000
```

---

## 📁 Project Structure

```
backend/
  main.py
  metadata_core.py
  forensic_analysis.py
  requirements.txt

frontend/
  index.html
```

---

## 📈 Supported Formats

PDF · DOCX · XLSX · PPTX

---

## 🔍 Forensic Flags

* **High**: Date mismatches, stripped metadata
* **Medium**: Missing fields
* **Low**: Generic metadata

---

## 🧠 How It Works

1. Upload file
2. Extract filesystem + document metadata
3. Perform forensic checks
4. Compute risk score
5. Download JSON report

---

## 🔌 API Endpoints

| Endpoint            | Method | Description            |
| ------------------- | ------ | ---------------------- |
| `/health`           | GET    | Server check           |
| `/analyze-file`     | POST   | Analyze one file       |
| `/analyze-multiple` | POST   | Analyze multiple files |

**Example:**

```bash
curl -X POST http://localhost:8000/analyze-file -F "file=@doc.pdf"
```

---

## 📦 Requirements

Python 3.9+
Key packages:

```
fastapi
uvicorn
python-multipart
PyPDF2
pikepdf
python-docx
openpyxl
python-pptx
```

---

## 🚀 Deployment

**Vercel (recommended):**

```bash
vercel --prod
```

**Local:**

```bash
python backend/main.py
```

---

## 🔧 Troubleshooting

* Backend not running → start `main.py`
* Upload errors → check file type/size
* CORS issues → adjust allowed origins

---

## 🛠 Development

* Add file type → edit `metadata_core.py`
* Add forensic rule → update `forensic_analysis.py`

```

---

If you want this **even shorter**, or want a **header with a logo + badges**, say the word.
