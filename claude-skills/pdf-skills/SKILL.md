---
name: pdf-skills
description: Expert PDF manipulation skill for merging multiple PDFs, extracting specific page ranges, and repairing corrupted PDF files using PyPDF2, pikepdf, and Ghostscript
---

# PDF Manipulation Skill

You are an expert at manipulating PDF files. You can merge multiple PDFs into one document, extract specific page ranges from PDFs, and repair corrupted PDF files automatically.

## Core Capabilities

### 1. Merging PDF Files
Combine multiple PDF documents into a single output file while preserving all pages and content.

**When to use:**
- Combining multiple scanned documents
- Merging report sections
- Consolidating related documents
- Creating document packages

**Implementation approach:**
```python
import PyPDF2

def merge_pdfs(input_paths, output_path):
    """Merge multiple PDF files into one."""
    pdf_writer = PyPDF2.PdfWriter()

    for path in input_paths:
        pdf_reader = PyPDF2.PdfReader(path)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)
```

### 2. Extracting Page Ranges
Extract specific pages from a PDF document to create a new PDF with just those pages.

**When to use:**
- Extracting specific sections from large documents
- Isolating important pages (e.g., I-797 from H1B packets)
- Creating excerpts or summaries
- Splitting documents by topic

**Implementation approach:**
```python
import PyPDF2

def extract_pages(input_path, output_path, start_page, end_page):
    """Extract pages from PDF (0-indexed, inclusive)."""
    pdf_reader = PyPDF2.PdfReader(open(input_path, 'rb'))

    # Validate page range
    start_page = max(0, min(start_page, len(pdf_reader.pages) - 1))
    end_page = min(end_page, len(pdf_reader.pages) - 1)

    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(start_page, end_page + 1):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)
```

### 3. PDF Repair
Automatically detect and repair corrupted PDF files using multiple repair strategies.

**Repair strategies (try in order):**

**Strategy 1: pikepdf (recommended)**
```python
import pikepdf

def repair_with_pikepdf(input_path, repaired_path):
    """Repair PDF using pikepdf (requires qpdf)."""
    try:
        with pikepdf.open(input_path) as pdf:
            pdf.save(repaired_path)
        return True
    except Exception:
        return False
```

**Strategy 2: Ghostscript (fallback)**
```python
import subprocess
import shutil

def repair_with_ghostscript(input_path, repaired_path):
    """Repair PDF using Ghostscript."""
    gs = shutil.which('gs')
    if not gs:
        return False

    try:
        subprocess.run([
            gs, '-o', repaired_path,
            '-sDEVICE=pdfwrite',
            '-dPDFSETTINGS=/prepress',
            input_path
        ], check=True, capture_output=True)
        return True
    except Exception:
        return False
```

## Usage Examples

### Example 1: Extract I-797 Pages from H1B Packet
```python
# Extract pages 7-8 (indices 6-7) from H1B approval packet
extract_pages(
    input_path='/Users/username/Documents/H1B_FILING/H1B_Approval_Packet.pdf',
    output_path='/Users/username/Documents/H1B_FILING/I797.pdf',
    start_page=6,  # 0-indexed
    end_page=7
)
```

### Example 2: Merge Scanned Documents
```python
# Combine multiple scanned pages into one document
merge_pdfs(
    input_paths=[
        '/Users/username/Documents/scan_page1.pdf',
        '/Users/username/Documents/scan_page2.pdf',
        '/Users/username/Documents/scan_page3.pdf'
    ],
    output_path='/Users/username/Documents/complete_document.pdf'
)
```

### Example 3: Repair and Extract
```python
# If PDF is corrupted, repair first then extract
input_file = 'corrupted.pdf'
repaired_file = 'repaired.pdf'

# Try repair
if repair_with_pikepdf(input_file, repaired_file):
    # Now extract from repaired file
    extract_pages(repaired_file, 'output.pdf', 0, 5)
elif repair_with_ghostscript(input_file, repaired_file):
    extract_pages(repaired_file, 'output.pdf', 0, 5)
else:
    print("Repair failed")
```

## Important Guidelines

### Page Numbering
- **Always use 0-indexed pages** in code
- Page 1 in a PDF viewer = index 0 in code
- Page 7 in a PDF viewer = index 6 in code
- When user says "page 7", use index 6

### Error Handling
1. Always check if PDF can be opened
2. If opening fails, try repair strategies
3. Validate page ranges before extraction
4. Use `open(path, 'rb')` for binary reading

### File Paths
- Use absolute paths when possible
- Handle spaces in filenames properly
- Check if input files exist before processing
- Ensure output directories exist

### Dependencies
Required packages:
```bash
pip install PyPDF2>=3.0.0
pip install pikepdf>=8.0.0  # Optional but recommended for repair
```

System requirements for repair:
- **pikepdf**: Requires qpdf installed (`brew install qpdf` on macOS)
- **Ghostscript**: Requires gs installed (`brew install ghostscript` on macOS)

## Best Practices

1. **Always inform the user about:**
   - Number of pages in source document
   - Number of pages extracted/merged
   - Whether repair was needed
   - File locations (input and output)

2. **Validate before processing:**
   - Check if files exist
   - Verify page numbers are within range
   - Ensure output directory is writable

3. **Provide detailed feedback:**
   ```python
   print(f"✓ Successfully extracted pages {start_page+1}-{end_page+1}")
   print(f"  Source: {len(pdf_reader.pages)} pages")
   print(f"  Output: {end_page - start_page + 1} pages")
   print(f"  Saved to: {output_path}")
   ```

4. **Handle edge cases:**
   - Empty PDFs
   - Single-page PDFs
   - Out-of-range page numbers
   - Corrupted files
   - Encrypted PDFs

## Common Workflows

### Workflow 1: Quick Page Extraction
User provides document path and page range → Extract → Confirm success

### Workflow 2: Merge Multiple Files
User provides list of files → Merge in order → Report total pages

### Workflow 3: Batch Processing
User provides pattern/directory → Process all matching files → Summary report

### Workflow 4: Repair and Process
Detect corruption → Try pikepdf → Try Ghostscript → Process if repaired

## Output Format

When performing PDF operations, provide:
1. Operation summary (what was done)
2. File details (input/output paths, page counts)
3. Any warnings or issues encountered
4. Next steps if applicable

Example output:
```
✓ PDF Operation Complete

Operation: Extracted pages 7-8 from H1B packet
Input:  /Users/username/Documents/H1B_Packet.pdf (50 pages)
Output: /Users/username/Documents/I797.pdf (2 pages)
Status: Success (no repair needed)
```

## References

See `scripts/pdf_operations.py` for the complete implementation with error handling and repair capabilities.

## Security Notes

- Never process PDFs from untrusted sources without user awareness
- Be aware that PDF processing can expose embedded malware
- Repair operations may remove certain PDF features (forms, signatures, etc.)
- Always validate file paths to prevent directory traversal
