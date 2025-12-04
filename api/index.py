"""
Vercel Serverless API for MetaForensic metadata analysis.
Handles file uploads and returns forensic analysis results.
"""
import json
import os
import tempfile
from typing import Dict, Any
import sys
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import extraction and analysis modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from metadata_core import extract_all_metadata
    from forensic_analysis import analyze_single_metadata
except ImportError as e:
    print(f"Import error: {e}", file=sys.stderr)
    raise


def format_response(status_code: int, body: Dict[str, Any]):
    """Format response for Vercel."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(body) if isinstance(body, dict) else body
    }


def handler(request):
    """Main API handler for Vercel Functions."""
    
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return format_response(200, {"ok": True})
    
    # Health check endpoint
    if request.path == "/api/health" or request.path == "/api/":
        if request.method == "GET":
            return format_response(200, {
                "status": "healthy",
                "service": "MetaForensic API",
                "version": "1.0.0",
                "environment": "vercel"
            })
    
    # File analysis endpoint
    if request.path == "/api/analyze" and request.method == "POST":
        try:
            # Get file from multipart form data
            files = request.files
            if not files or "file" not in files:
                return format_response(400, {"error": "No file provided"})
            
            file = files["file"]
            if not file.filename:
                return format_response(400, {"error": "Empty filename"})
            
            # Save to temporary file
            tmp_path = None
            try:
                suffix = os.path.splitext(file.filename)[1]
                tmp_fd, tmp_path = tempfile.mkstemp(suffix=suffix)
                os.close(tmp_fd)
                
                file.save(tmp_path)
                
                # Extract metadata with timeout
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                executor = ThreadPoolExecutor(max_workers=1)
                
                try:
                    # Run extraction with timeout
                    base_metadata = loop.run_until_complete(
                        asyncio.wait_for(
                            loop.run_in_executor(executor, lambda: extract_all_metadata(tmp_path)),
                            timeout=30.0
                        )
                    )
                except asyncio.TimeoutError:
                    return format_response(504, {"error": "Metadata extraction timed out"})
                except Exception as e:
                    return format_response(500, {"error": f"Extraction failed: {str(e)}"})
                
                # Run forensic analysis
                try:
                    flags = loop.run_until_complete(
                        asyncio.wait_for(
                            loop.run_in_executor(executor, lambda: analyze_single_metadata(base_metadata)),
                            timeout=10.0
                        )
                    )
                except asyncio.TimeoutError:
                    flags = {
                        "error": "analysis_timeout",
                        "total_flags": 0,
                        "risk_score": 0,
                        "flags": [],
                        "summary": {"status": "error", "message": "Analysis timed out"}
                    }
                except Exception as e:
                    flags = {
                        "error": str(e),
                        "total_flags": 0,
                        "risk_score": 0,
                        "flags": [],
                        "summary": {"status": "error", "message": f"Analysis failed: {str(e)}"}
                    }
                finally:
                    try:
                        executor.shutdown(wait=False)
                    except:
                        pass
                    loop.close()
                
                # Build response
                response = {
                    "filename": file.filename,
                    "file_size": len(file.read()),
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
                    "forensic_flags": flags,
                    "raw_metadata": base_metadata,
                }
                
                return format_response(200, response)
                
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except:
                        pass
        
        except Exception as e:
            return format_response(500, {
                "error": "Internal server error",
                "details": str(e),
                "traceback": traceback.format_exc()
            })
    
    # Not found
    return format_response(404, {"error": "Endpoint not found"})
