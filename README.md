# MetaForensic
## Advanced Metadata Analysis & Forensic Intelligence

Professional-grade forensic metadata extraction tool with sophisticated black and grey design.

---

## 🎨 DESIGN

**Clean, Professional Black & Grey Theme:**
- Pure black background (#000000)
- Dark grey sections (#1a1a1a, #2d2d2d)
- Light grey text (#e0e0e0, #cccccc)
- Muted alerts (soft red #cc6666, soft orange #ccaa66)
- No animations, no glow effects - clean and professional
- Standard system fonts for readability

---

## ✨ FEATURES

### 📊 Advanced Metadata Extraction
- **Filesystem Level**: File size, timestamps, timezone, system info, permissions, inode
- **PDF**: Pages, encryption, version, linearization status
- **DOCX**: Content stats, author, company, timestamps
- **XLSX**: Sheet info, author, company
- **PPTX**: Slide count, company, timestamps

### 🔍 Forensic Analysis
- Date anomaly detection
- Metadata stripping indicators
- Suspicious pattern detection
- Risk scoring (0-10)
- Severity classification (HIGH/MEDIUM/LOW)

### 🎯 Professional Features
- Drag-and-drop file upload
- Real-time analysis
- JSON report download
- Batch file processing
- Cross-verification analysis
- Mobile responsive design

---

## 🚀 QUICK START

### 1. Install & Setup
```powershell
cd "d:\python projects\meta data"
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

### 2. Start Backend
```powershell
python backend/main.py
# Backend on: http://localhost:8000
```

### 3. Start Frontend (new terminal)
```powershell
cd frontend
python -m http.server 3000
# Frontend on: http://localhost:3000
```

### 4. Use the Application
Open `http://localhost:3000` and start analyzing files!

---

## 📁 PROJECT STRUCTURE

```
backend/
├── main.py              # FastAPI server
├── metadata_core.py     # Metadata extraction
├── forensic_analysis.py # Forensic detection
└── requirements.txt

frontend/
└── index.html          # Professional black & grey UI
```

---

## 📈 SUPPORTED FORMATS

| Format | Features |
|--------|----------|
| PDF | Pages, Encryption, Version, Linearization |
| DOCX | Paragraphs, Tables, Company, Manager, Author |
| XLSX | Sheet count, names, Company, Manager |
| PPTX | Slide count, Company, Timestamps |

---

## 🔒 FORENSIC FLAGS

**HIGH**: Date anomalies, metadata stripping  
**MEDIUM**: Blank fields, inconsistent dates  
**LOW**: Generic metadata, encoding info

---

## ✓ PROJECT STATUS: COMPLETE

- [x] Backend with enhanced metadata extraction
- [x] Frontend with professional black & grey theme
- [x] Timezone & system information support
- [x] Advanced forensic analysis
- [x] Batch file processing
- [x] JSON report generation
- [x] Mobile responsive design
- [x] Clean, professional UI/UX

**Production ready!**

---

## 📈 SUPPORTED FORMATS

| Format | Features |
|--------|----------|
| PDF | Pages, Encryption, Version, Linearization |
| DOCX | Paragraphs, Tables, Company, Manager, Author |
| XLSX | Sheet count, names, Company, Manager |
| PPTX | Slide count, Company, Timestamps |

---

## 🔒 FORENSIC FLAGS

**HIGH**: Date anomalies, metadata stripping  
**MEDIUM**: Blank fields, inconsistent dates  
**LOW**: Generic metadata, encoding info

---

## ✓ PROJECT STATUS: COMPLETE

- [x] Backend with enhanced metadata extraction
- [x] Frontend with professional dark hacker aesthetic
- [x] Timezone & system information support
- [x] Advanced forensic analysis
- [x] Batch file processing
- [x] JSON report generation
- [x] Mobile responsive design
- [x] Professional UI/UX

**Ready for production use!**

## Project Structure

```
.
├── api/                          # Vercel serverless functions
│   ├── index.py                 # Main file upload handler
│   ├── health.py                # Health check endpoint
│   └── lib/
│       ├── metadata_core.py
│       └── forensic_analysis.py
├── backend/                      # FastAPI backend (local dev)
│   ├── main.py
│   ├── metadata_core.py
│   ├── forensic_analysis.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── vercel.json                   # Vercel config
└── README.md
```

## How It Works

1. **Upload a File** - Drag & drop or click to select PDF, DOCX, XLSX, or PPTX
2. **Extract Metadata** - System extracts:
   - OS timestamps (created, modified, accessed)
   - Document internal metadata (author, title, etc.)
3. **Forensic Analysis** - Detects:
   - Date anomalies (impossible dates, future timestamps)
   - Metadata stripping (missing author, title, etc.)
   - Date mismatches between filesystem and document
4. **Risk Scoring** - Calculates overall risk:
   - Clean (0-1): No issues
   - Caution (2-4): Minor issues
   - Suspicious (5+): Major issues
5. **Download Report** - Export full analysis as JSON

## Supported File Types

- **PDF** (.pdf)
- **Word** (.docx, .doc)
- **Excel** (.xlsx, .xls)
- **PowerPoint** (.pptx, .ppt)

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api` | POST | Analyze single file |
| `/analyze-multiple` | POST | Analyze multiple files |

### Example Request

```bash
curl -X POST http://localhost:8000/analyze-file \
  -F "file=@document.pdf"
```

## Requirements

- Python 3.9+
- pip/conda for package management
- Browser with fetch API support

### Python Packages

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
python-multipart>=0.0.5
PyPDF2>=3.0.0
pikepdf>=8.0.0
python-docx>=1.1.0
openpyxl>=3.1.0
python-pptx>=0.6.21
```

## Deployment Options

### Option 1: Vercel (Recommended - Serverless)

```bash
vercel --prod
```

**Advantages:**
- Free tier available
- Automatic HTTPS
- Serverless (no server to manage)
- Auto-scaling
- GitHub integration available

### Option 2: Local Development

```bash
cd backend
python main.py
```

Then open `frontend/index.html`

### Option 3: Heroku (Traditional Server)

```bash
git push heroku main
```

Requires `Procfile`: `web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

## Troubleshooting

### "Failed to fetch" Error

1. **Backend not running?** → Start with `python backend/main.py`
2. **CORS issue?** → Check firewall/proxy settings
3. **Wrong port?** → Verify port 8000 is available
4. **Missing python-multipart?** → Run `pip install python-multipart`

### Installation Issues

```bash
# Reinstall all dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# Verify installation
pip list | findstr fastapi
```

### File Upload Fails

- Check file size (shouldn't exceed 50MB locally)
- Ensure file is a supported format
- Try a different file to isolate the issue
- Check browser console (F12) for error details

## Development

### Add New File Type Support

Edit `api/lib/metadata_core.py`:

```python
def extract_newformat_metadata(file_path: str) -> Dict[str, Any]:
    """Extract metadata for new format."""
    # Implementation here
    return metadata
```

Then update `extract_all_metadata()` to call it.

### Modify Forensic Rules

Edit `api/lib/forensic_analysis.py` to add new detection rules:

```python
def check_new_anomaly(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check for new type of anomaly."""
    flags = []
    # Detection logic
    return flags
```

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Local: ~1-5s per file (depends on file size)
- Vercel: ~2-8s per file (includes network latency)

## License

This project is provided as-is for forensic analysis purposes.
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
   
   Or using Python directly:
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Open the frontend:**
   - Simply open `frontend/index.html` in a modern web browser
   - Or serve it using a local web server:
     
     **Python 3:**
     ```bash
     cd frontend
     python -m http.server 8080
     ```
     
     **Node.js (http-server):**
     ```bash
     npx http-server frontend -p 8080
     ```

2. **Access the application:**
   - Open `http://localhost:8080` in your browser
   - The frontend will connect to the backend at `http://localhost:8000`

## Usage

1. **Start the backend server** (see Backend Setup above)
2. **Open the frontend** in your browser
3. **Upload a file** by:
   - Dragging and dropping a file onto the upload area
   - Clicking the upload area to select a file
4. **View results:**
   - Forensic summary with risk score
   - OS-level metadata
   - Document metadata
   - Cross-verification results
   - Forensic flags and anomalies
   - Raw JSON metadata
5. **Download report** as JSON for archival or further analysis

## API Endpoints

### `GET /`
Health check endpoint.

### `GET /health`
Health check endpoint.

### `POST /analyze-file`
Analyze a single uploaded file.

**Request:**
- `file`: Multipart file upload

**Response:**
```json
{
  "filename": "document.pdf",
  "file_size": 12345,
  "file_type": ".pdf",
  "filesystem_metadata": {...},
  "document_metadata": {...},
  "cross_check": {...},
  "forensic_flags": {...},
  "raw_metadata": {...},
  "errors": {...}
}
```

### `POST /analyze-multiple`
Analyze multiple files at once.

**Request:**
- `files`: Multiple file uploads

**Response:**
```json
{
  "total_files": 2,
  "successful": 2,
  "failed": 0,
  "results": [...],
  "errors": []
}
```

## Supported File Types

- **PDF** - Using PyPDF2 and pikepdf
- **DOCX** - Using python-docx
- **XLSX** - Using openpyxl
- **PPTX** - Using python-pptx

## Forensic Analysis Features

The forensic analysis engine checks for:

1. **Date Anomalies:**
   - Future dates
   - Impossible timestamps (creation after modification)
   - Significant mismatches between filesystem and document dates

2. **Metadata Stripping:**
   - Missing common metadata fields
   - Minimal metadata presence

3. **Suspicious Metadata:**
   - Generic values (test, admin, unknown, etc.)
   - Empty or placeholder values

## Risk Scoring

- **High Severity**: 3 points (critical issues)
- **Medium Severity**: 2 points (potential issues)
- **Low Severity**: 1 point (minor concerns)

**Risk Levels:**
- **Clean**: Risk score < 2
- **Caution**: Risk score 2-4
- **Suspicious**: Risk score ≥ 5

## Development

### Adding New File Type Support

1. Add extraction function in `metadata_core.py`
2. Update `extract_all_metadata()` to handle new file type
3. Update forensic analysis if needed
4. Update frontend file accept attribute

### Extending Forensic Analysis

Add new check functions in `forensic_analysis.py` and call them from `analyze_single_metadata()`.

## Security Notes

- The CORS middleware currently allows all origins (`allow_origins=["*"]`). In production, specify your frontend domain.
- Temporary files are automatically cleaned up after processing.
- File size limits are not enforced by default - consider adding them for production.

## Troubleshooting

**Backend won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is already in use
- Verify Python version (3.8+ recommended)

**Frontend can't connect to backend:**
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify no firewall is blocking the connection

**Metadata extraction fails:**
- Check if the file type is supported
- Verify the file isn't corrupted
- Check backend logs for detailed error messages

## License

This project is provided as-is for educational and forensic analysis purposes.

