#!/usr/bin/env python3
"""
CLI runner for handwritten PDF to Word conversion.

Usage:
    python run_ocr.py /path/to/input.pdf
    python run_ocr.py /path/to/input.pdf /path/to/output.docx

The script reuses the full handwritten_ocr app stack directly:
    - core/pdf_to_images.py  → render pages via PyMuPDF
    - core/claude_ocr.py     → extract text via Claude Vision
    - core/docx_builder.py   → assemble .docx with page breaks

Progress is printed to the terminal line by line.
"""

import sys
import os
from pathlib import Path

# Point to the handwritten_ocr app directory
APP_DIR = Path("/Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr")
sys.path.insert(0, str(APP_DIR))

# --- Validate arguments ---
if len(sys.argv) < 2:
    print("Usage: python run_ocr.py <input.pdf> [output.docx]")
    print("Example: python run_ocr.py ~/Desktop/notes.pdf")
    sys.exit(1)

input_path = Path(sys.argv[1]).expanduser().resolve()

if not input_path.exists():
    print(f"Error: File not found: {input_path}")
    sys.exit(1)

if input_path.suffix.lower() != ".pdf":
    print(f"Error: Input must be a PDF file, got: {input_path.suffix}")
    sys.exit(1)

# Determine output path
if len(sys.argv) >= 3:
    output_path = Path(sys.argv[2]).expanduser().resolve()
else:
    output_path = input_path.with_suffix(".docx")

# --- Load config (reads .env for ANTHROPIC_API_KEY) ---
import config

if not config.ANTHROPIC_API_KEY or config.ANTHROPIC_API_KEY.startswith("sk-ant-YOUR"):
    print("Error: ANTHROPIC_API_KEY is not set.")
    print(f"Add it to: {APP_DIR}/.env")
    print('Format: ANTHROPIC_API_KEY=sk-ant-...')
    sys.exit(1)

# --- Import core modules ---
from core.pdf_to_images import pdf_to_png_bytes_list
from core.claude_ocr import extract_text_from_image
from core.docx_builder import build_docx

# --- Run conversion ---
print(f"\nHandwritten OCR — CLI Mode")
print(f"{'─' * 50}")
print(f"Input:  {input_path}")
print(f"Output: {output_path}")
print(f"Model:  {config.CLAUDE_MODEL}")
print(f"{'─' * 50}\n")

print("Step 1/3  Rendering PDF pages to images...")
try:
    pages_png = pdf_to_png_bytes_list(str(input_path), dpi=config.PDF_RENDER_DPI)
except Exception as e:
    print(f"Error rendering PDF: {e}")
    sys.exit(1)

total = len(pages_png)
print(f"          {total} page(s) found.\n")

print("Step 2/3  Extracting handwritten text with Claude Vision...")
page_texts = []
for i, png_bytes in enumerate(pages_png, start=1):
    print(f"          Page {i}/{total}...", end=" ", flush=True)
    try:
        text = extract_text_from_image(
            png_bytes=png_bytes,
            api_key=config.ANTHROPIC_API_KEY,
            model=config.CLAUDE_MODEL,
            prompt=config.CLAUDE_PROMPT,
        )
        page_texts.append(text)
        # Show a short preview (first 60 chars) of what was extracted
        preview = text.replace("\n", " ").strip()[:60]
        print(f"done  [{preview}{'...' if len(text) > 60 else ''}]")
    except Exception as e:
        print(f"failed — {e}")
        page_texts.append("")   # keep page count aligned; blank page in docx

print(f"\nStep 3/3  Building Word document...")
try:
    build_docx(
        page_texts=page_texts,
        output_path=str(output_path),
        source_filename=input_path.name,
    )
except Exception as e:
    print(f"Error building .docx: {e}")
    sys.exit(1)

print(f"\n{'─' * 50}")
print(f"Done!  Output saved to:")
print(f"  {output_path}")
print(f"{'─' * 50}\n")
