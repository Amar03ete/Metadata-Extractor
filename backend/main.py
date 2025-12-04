"""
FastAPI backend server for metadata analysis web application.
"""
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import shutil
import importlib
import platform

from metadata_core import extract_all_metadata
from forensic_analysis import analyze_single_metadata

app = FastAPI(
    title="Metadata Analyzer API",
    description="Forensic metadata extraction and analysis tool",
    version="1.0.0"
)

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "Metadata Analyzer API is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    # Run quick health checks and return detailed status
    def check_module(name):
        try:
            importlib.import_module(name)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    checks = {}
    # Python runtime
    checks['python_version'] = {"version": platform.python_version(), "ok": True}

    # Important optional modules
    module_names = {
        'PyPDF2': 'PyPDF2',
        'pikepdf': 'pikepdf',
        'python-docx': 'docx',
        'openpyxl': 'openpyxl',
        'python-pptx': 'pptx',
        'psutil': 'psutil',
        'pandas': 'pandas'
    }

    for friendly, mod in module_names.items():
        checks[friendly] = check_module(mod)

    # Disk usage
    try:
        total, used, free = shutil.disk_usage(os.getcwd())
        checks['disk_usage'] = {"total": total, "used": used, "free": free}
    except Exception as e:
        checks['disk_usage'] = {"error": str(e)}

    # Temp file write test
    tmp_ok = True
    tmp_error = None
    try:
        with tempfile.NamedTemporaryFile(delete=True) as t:
            t.write(b"healthcheck")
            t.flush()
    except Exception as e:
        tmp_ok = False
        tmp_error = str(e)
    checks['temp_write'] = {"ok": tmp_ok, "error": tmp_error}

    # Uptime (approx)
    checks['server_time'] = {"now": time.time()}

    # Overall status
    overall_ok = all(v.get('ok', True) for k, v in checks.items() if isinstance(v, dict) and 'ok' in v)
    status = "healthy" if overall_ok else "degraded"

    return {"status": status, "checks": checks}


@app.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    """
    Analyze uploaded file for metadata extraction and forensic analysis.
    
    Returns:
    - filename: Original filename
    - filesystem_metadata: OS-level file metadata
    - document_metadata: Internal document metadata
    - cross_check: Comparison between filesystem and document dates
    - forensic_flags: Analysis results with flags and risk scores
    - raw_metadata: Complete raw metadata dictionary
    """
    tmp_path = None
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Save temporarily
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Empty file")
            tmp.write(content)
            tmp_path = tmp.name
        
        # Extract metadata with timeout in a thread to avoid blocking the event loop
        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        try:
            base_metadata = await asyncio.wait_for(
                loop.run_in_executor(executor, lambda: extract_all_metadata(tmp_path)),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Metadata extraction timed out")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Metadata extraction failed: {str(e)}"
            )

        # Forensic analysis with short timeout
        try:
            flags = await asyncio.wait_for(
                loop.run_in_executor(executor, lambda: analyze_single_metadata(base_metadata)),
                timeout=10.0
            )
        except asyncio.TimeoutError:
            # Return partial results with timeout flag
            flags = {
                "error": "forensic_analysis_timeout",
                "total_flags": 0,
                "risk_score": 0,
                "flags": [],
                "summary": {"status": "error", "message": "Forensic analysis timed out"}
            }
        except Exception as e:
            flags = {
                "error": str(e),
                "total_flags": 0,
                "risk_score": 0,
                "flags": [],
                "summary": {"status": "error", "message": f"Forensic analysis failed: {str(e)}"}
            }
        finally:
            try:
                executor.shutdown(wait=False)
            except Exception:
                pass
        
        # Organize response
        response = {
            "filename": file.filename,
            "file_size": len(content),
            "file_type": suffix.lower() if suffix else "unknown",
            "os_hardware_metadata": base_metadata.get("os_hardware_metadata", {}),
            "timezone_metadata": base_metadata.get("timezone_metadata", {}),
            "file_identity": {
                "filename": base_metadata.get("filename"),
                "file_extension": base_metadata.get("file_extension"),
                "mime_type": base_metadata.get("mime_type"),
                "file_size": base_metadata.get("size_formatted"),
                "file_size_bytes": base_metadata.get("size_bytes"),
            },
            "file_hashes": {
                "md5": base_metadata.get("file_hash_md5"),
                "sha1": base_metadata.get("file_hash_sha1"),
                "sha256": base_metadata.get("file_hash_sha256"),
            },
            "timestamps": {
                "created": {
                    "datetime": base_metadata.get("fs_created"),
                    "timezone": base_metadata.get("timezone_name"),
                    "utc_offset": base_metadata.get("timezone_offset"),
                },
                "modified": {
                    "datetime": base_metadata.get("fs_modified"),
                    "timezone": base_metadata.get("timezone_name"),
                    "utc_offset": base_metadata.get("timezone_offset"),
                },
                "accessed": {
                    "datetime": base_metadata.get("fs_accessed"),
                    "timezone": base_metadata.get("timezone_name"),
                    "utc_offset": base_metadata.get("timezone_offset"),
                },
            },
            "provenance_authorship": {
                "docx_author": base_metadata.get("docx_author"),
                "docx_last_modified_by": base_metadata.get("docx_last_modified_by"),
                "xlsx_author": base_metadata.get("xlsx_author"),
                "xlsx_last_modified_by": base_metadata.get("xlsx_last_modified_by"),
                "pptx_author": base_metadata.get("pptx_author"),
                "pptx_last_modified_by": base_metadata.get("pptx_last_modified_by"),
                "pdf_author": base_metadata.get("pdf_author"),
                "pdf_creator": base_metadata.get("pdf_creator"),
                "pdf_producer": base_metadata.get("pdf_producer"),
            },
            "storage_access": {
                "file_path": base_metadata.get("file_path"),
                "permissions": base_metadata.get("file_permissions"),
                "permissions_octal": base_metadata.get("file_permissions_octal"),
                "owner": base_metadata.get("owner_name"),
                "owner_uid": base_metadata.get("owner_uid"),
                "group": base_metadata.get("group_name"),
                "group_gid": base_metadata.get("group_gid"),
                "inode": base_metadata.get("inode"),
                "hard_links": base_metadata.get("hard_links"),
            },
            "document_metadata": {
                k: v for k, v in base_metadata.items()
                if (k.startswith("pdf_") or k.startswith("docx_") or 
                    k.startswith("xlsx_") or k.startswith("pptx_")) and not k.endswith("_error")
            },
            "filesystem_metadata": {
                "created": base_metadata.get("fs_created"),
                "modified": base_metadata.get("fs_modified"),
                "accessed": base_metadata.get("fs_accessed"),
                "size_bytes": base_metadata.get("size_bytes"),
            },
            "cross_check": {
                "fs_created_vs_doc_created": {
                    "filesystem": base_metadata.get("fs_created"),
                    "document": (
                        base_metadata.get("docx_created") or 
                        base_metadata.get("xlsx_created") or
                        base_metadata.get("pptx_created") or 
                        base_metadata.get("pdf_creationdate")
                    ),
                },
                "fs_modified_vs_doc_modified": {
                    "filesystem": base_metadata.get("fs_modified"),
                    "document": (
                        base_metadata.get("docx_modified") or 
                        base_metadata.get("xlsx_modified") or
                        base_metadata.get("pptx_modified") or 
                        base_metadata.get("pdf_moddate")
                    ),
                }
            },
            "forensic_flags": flags,
            "raw_metadata": base_metadata,
            "errors": {
                k: v for k, v in base_metadata.items() if k.endswith("_error")
            }
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        error_detail = {
            "error": str(e),
            "traceback": traceback.format_exc() if app.debug else None
        }
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "details": error_detail}
        )
    finally:
        # Clean up temporary file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass  # Best effort cleanup


@app.post("/analyze-multiple")
async def analyze_multiple(files: list[UploadFile] = File(...)):
    """
    Analyze multiple files at once.
    Returns a list of analysis results.
    """
    results = []
    errors = []
    
    for file in files:
        try:
            result = await analyze_file(file)
            results.append(result)
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "total_files": len(files),
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

