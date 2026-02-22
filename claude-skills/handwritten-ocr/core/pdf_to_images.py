"""
PDF to PNG image pipeline.

Renders each page of a PDF to PNG bytes using PyMuPDF (fitz).
No poppler/pdftoppm dependency needed — PyMuPDF bundles its own renderer.

For pre-flight PDF validation and auto-repair, reuses the existing
PDFSkill from the parent repository.
"""

import sys
from pathlib import Path
from typing import List

import fitz  # PyMuPDF

# Allow importing the existing PDFSkill from the parent repo
# File now lives at: claude-skills/handwritten-ocr/core/pdf_to_images.py
# PDFSkill lives at: skills/pdf_skill/pdf_skill.py (4 levels up from here)
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
try:
    from skills.pdf_skill.pdf_skill import PDFSkill
    _pdf_skill_available = True
except ImportError:
    _pdf_skill_available = False


def _validate_and_repair(pdf_path: str) -> None:
    """
    Use PDFSkill to validate the PDF and trigger auto-repair if needed.
    Silently skips if PDFSkill is unavailable.
    """
    if not _pdf_skill_available:
        return
    skill = PDFSkill()
    result = skill.get_info(pdf_path)
    if result.get("status") == "error":
        raise RuntimeError(f"PDF validation failed: {result.get('message')}")


def pdf_to_png_bytes_list(pdf_path: str, dpi: int = 150) -> List[bytes]:
    """
    Render all pages of a PDF to a list of PNG byte strings.

    Args:
        pdf_path: Absolute path to the PDF file
        dpi:      Rendering resolution (default 150 DPI)

    Returns:
        List of PNG bytes, one per page, in page order

    Raises:
        RuntimeError: If PDF validation/repair fails
        fitz.FileDataError: If PyMuPDF cannot parse the PDF
    """
    _validate_and_repair(pdf_path)

    doc = fitz.open(pdf_path)
    pages_png: List[bytes] = []
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    for page in doc:
        pixmap = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB)
        pages_png.append(pixmap.tobytes("png"))

    doc.close()
    return pages_png
