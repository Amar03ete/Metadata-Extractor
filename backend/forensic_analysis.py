"""
Forensic analysis engine for metadata.
Detects anomalies, inconsistencies, and potential tampering indicators.
"""
from typing import Dict, Any, List
from datetime import datetime
import re


def parse_date(date_str: Any) -> datetime:
    """Attempt to parse various date formats."""
    if date_str is None:
        return None
    
    if isinstance(date_str, datetime):
        return date_str
    
    if isinstance(date_str, str):
        # Common ISO formats
        for fmt in [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]:
            try:
                return datetime.strptime(date_str[:19], fmt)
            except (ValueError, IndexError):
                continue
        
        # PDF date format: D:YYYYMMDDHHmmSSOHH'mm
        pdf_match = re.match(r'D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})', date_str)
        if pdf_match:
            try:
                return datetime(
                    int(pdf_match.group(1)),
                    int(pdf_match.group(2)),
                    int(pdf_match.group(3)),
                    int(pdf_match.group(4)),
                    int(pdf_match.group(5)),
                    int(pdf_match.group(6))
                )
            except ValueError:
                pass
    
    return None


def compare_dates(date1: Any, date2: Any, tolerance_seconds: int = 60) -> Dict[str, Any]:
    """
    Compare two dates and return analysis.
    tolerance_seconds: Allowable difference in seconds (for clock skew).
    """
    parsed1 = parse_date(date1)
    parsed2 = parse_date(date2)
    
    if parsed1 is None or parsed2 is None:
        return {
            "status": "incomplete",
            "message": "One or both dates could not be parsed",
            "date1": str(date1),
            "date2": str(date2)
        }
    
    diff = abs((parsed1 - parsed2).total_seconds())
    
    if diff <= tolerance_seconds:
        return {
            "status": "consistent",
            "message": "Dates are within acceptable tolerance",
            "difference_seconds": diff
        }
    elif parsed1 > parsed2:
        return {
            "status": "anomaly",
            "message": f"Date1 is {diff:.0f} seconds later than Date2 (possible backdating)",
            "difference_seconds": diff,
            "warning": "File system date is newer than document creation date"
        }
    else:
        return {
            "status": "anomaly",
            "message": f"Date2 is {diff:.0f} seconds later than Date1",
            "difference_seconds": diff
        }


def check_metadata_removal(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check if metadata appears to have been stripped."""
    flags = []
    
    # Check for missing common metadata fields
    file_ext = metadata.get("file_extension", "").lower()
    
    if file_ext == ".pdf":
        if not metadata.get("pdf_author") and not metadata.get("pdf_title"):
            flags.append({
                "severity": "medium",
                "flag": "metadata_stripping",
                "message": "PDF appears to have minimal or no metadata (author/title missing)"
            })
    
    elif file_ext in [".docx", ".xlsx", ".pptx"]:
        prefix = file_ext[1:4]  # doc, xls, ppt
        if not metadata.get(f"{prefix}x_author") and not metadata.get(f"{prefix}x_title"):
            flags.append({
                "severity": "medium",
                "flag": "metadata_stripping",
                "message": f"{file_ext.upper()} appears to have minimal or no metadata"
            })
    
    return flags


def check_date_anomalies(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check for suspicious date patterns."""
    flags = []
    
    fs_created = metadata.get("fs_created")
    fs_modified = metadata.get("fs_modified")
    
    # Check if creation is after modification (impossible)
    if fs_created and fs_modified:
        created_dt = parse_date(fs_created)
        modified_dt = parse_date(fs_modified)
        
        if created_dt and modified_dt and created_dt > modified_dt:
            flags.append({
                "severity": "high",
                "flag": "date_anomaly",
                "message": "File creation date is AFTER modification date (impossible)",
                "fs_created": fs_created,
                "fs_modified": fs_modified
            })
    
    # Check for future dates
    now = datetime.now()
    for key, value in metadata.items():
        if "date" in key.lower() or "created" in key.lower() or "modified" in key.lower():
            dt = parse_date(value)
            if dt and dt > now:
                flags.append({
                    "severity": "high",
                    "flag": "future_date",
                    "message": f"Date in future: {key} = {value}",
                    "field": key,
                    "value": str(value)
                })
    
    # Cross-check filesystem vs document dates
    file_ext = metadata.get("file_extension", "").lower()
    
    if file_ext == ".pdf":
        doc_created = metadata.get("pdf_creationdate")
        doc_modified = metadata.get("pdf_moddate")
        
        if doc_created:
            comp = compare_dates(fs_created, doc_created, tolerance_seconds=300)
            if comp["status"] == "anomaly":
                flags.append({
                    "severity": "medium",
                    "flag": "date_mismatch",
                    "message": comp["message"],
                    "comparison": "fs_created vs pdf_creationdate",
                    "details": comp
                })
        
        if doc_modified:
            comp = compare_dates(fs_modified, doc_modified, tolerance_seconds=300)
            if comp["status"] == "anomaly":
                flags.append({
                    "severity": "medium",
                    "flag": "date_mismatch",
                    "message": comp["message"],
                    "comparison": "fs_modified vs pdf_moddate",
                    "details": comp
                })
    
    elif file_ext == ".docx":
        doc_created = metadata.get("docx_created")
        doc_modified = metadata.get("docx_modified")
        
        if doc_created:
            comp = compare_dates(fs_created, doc_created, tolerance_seconds=300)
            if comp["status"] == "anomaly":
                flags.append({
                    "severity": "medium",
                    "flag": "date_mismatch",
                    "message": comp["message"],
                    "comparison": "fs_created vs docx_created",
                    "details": comp
                })
        
        if doc_modified:
            comp = compare_dates(fs_modified, doc_modified, tolerance_seconds=300)
            if comp["status"] == "anomaly":
                flags.append({
                    "severity": "medium",
                    "flag": "date_mismatch",
                    "message": comp["message"],
                    "comparison": "fs_modified vs docx_modified",
                    "details": comp
                })
    
    elif file_ext == ".xlsx":
        doc_created = metadata.get("xlsx_created")
        doc_modified = metadata.get("xlsx_modified")
        
        if doc_created:
            comp = compare_dates(fs_created, doc_created, tolerance_seconds=300)
            if comp["status"] == "anomaly":
                flags.append({
                    "severity": "medium",
                    "flag": "date_mismatch",
                    "message": comp["message"],
                    "comparison": "fs_created vs xlsx_created",
                    "details": comp
                })
        
        if doc_modified:
            comp = compare_dates(fs_modified, doc_modified, tolerance_seconds=300)
            if comp["status"] == "anomaly":
                flags.append({
                    "severity": "medium",
                    "flag": "date_mismatch",
                    "message": comp["message"],
                    "comparison": "fs_modified vs xlsx_modified",
                    "details": comp
                })
    
    elif file_ext == ".pptx":
        doc_created = metadata.get("pptx_created")
        doc_modified = metadata.get("pptx_modified")
        
        if doc_created:
            comp = compare_dates(fs_created, doc_created, tolerance_seconds=300)
            if comp["status"] == "anomaly":
                flags.append({
                    "severity": "medium",
                    "flag": "date_mismatch",
                    "message": comp["message"],
                    "comparison": "fs_created vs pptx_created",
                    "details": comp
                })
        
        if doc_modified:
            comp = compare_dates(fs_modified, doc_modified, tolerance_seconds=300)
            if comp["status"] == "anomaly":
                flags.append({
                    "severity": "medium",
                    "flag": "date_mismatch",
                    "message": comp["message"],
                    "comparison": "fs_modified vs pptx_modified",
                    "details": comp
                })
    
    return flags


def check_suspicious_metadata(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check for suspicious metadata content."""
    flags = []
    
    # Check for test/dummy data
    suspicious_patterns = [
        ("author", ["test", "admin", "user", "unknown", "sample"]),
        ("title", ["untitled", "test", "sample", "document"]),
    ]
    
    for field_pattern, suspicious_values in suspicious_patterns:
        for key, value in metadata.items():
            if field_pattern in key.lower() and isinstance(value, str):
                value_lower = value.lower().strip()
                if value_lower in suspicious_values or not value_lower:
                    flags.append({
                        "severity": "low",
                        "flag": "generic_metadata",
                        "message": f"Suspicious or generic value in {key}: '{value}'",
                        "field": key,
                        "value": value
                    })
    
    return flags


def analyze_single_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main forensic analysis function.
    Returns a dictionary with flags, severity levels, and explanations.
    """
    all_flags = []
    
    # Run all checks
    all_flags.extend(check_date_anomalies(metadata))
    all_flags.extend(check_metadata_removal(metadata))
    all_flags.extend(check_suspicious_metadata(metadata))
    
    # Calculate risk score
    severity_scores = {"high": 3, "medium": 2, "low": 1}
    risk_score = sum(severity_scores.get(flag.get("severity", "low"), 0) for flag in all_flags)
    
    # Categorize by severity
    high_severity = [f for f in all_flags if f.get("severity") == "high"]
    medium_severity = [f for f in all_flags if f.get("severity") == "medium"]
    low_severity = [f for f in all_flags if f.get("severity") == "low"]
    
    return {
        "total_flags": len(all_flags),
        "risk_score": risk_score,
        "severity_breakdown": {
            "high": len(high_severity),
            "medium": len(medium_severity),
            "low": len(low_severity)
        },
        "flags": all_flags,
        "summary": {
            "status": "suspicious" if risk_score >= 5 else ("caution" if risk_score >= 2 else "clean"),
            "message": f"Found {len(all_flags)} potential issues with risk score {risk_score}"
        }
    }

