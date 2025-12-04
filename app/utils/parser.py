import os
import subprocess
from typing import Optional

def extract_text_from_file(path: str, content_type: Optional[str] = None) -> str:
    """
    Try to extract text from PDF or text files.
    Requires 'pdftotext' to be installed for PDF parsing (poppler-utils).
    """
    _, ext = os.path.splitext(path.lower())
    try:
        if ext in [".pdf"]:
            # Use pdftotext which comes from poppler-utils
            txt_path = path + ".txt"
            cmd = ["pdftotext", path, txt_path]
            subprocess.run(cmd, check=True)
            with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            # cleanup
            try:
                os.remove(txt_path)
            except Exception:
                pass
            return text
        else:
            # fallback: read as text file
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    except Exception as e:
        print("extract_text_from_file error:", e)
        return ""
