# PDF Manipulation Skill - Usage Examples

This file contains detailed examples of how to use the PDF Manipulation skill with Claude.

## Example 1: Extract Specific Pages (Your Original Use Case)

### Scenario
You have an employment contract bundle PDF with 50 pages. You need to extract just pages 7-8 which contain the signed agreement summary.

### What to Say to Claude

```
I have an employment contract bundle and I need to extract the signed agreement pages.

File location: /Users/username/Documents/Contracts/Contract_Bundle_2025.pdf

Please extract pages 7-8 and save them as:
/Users/username/Documents/Contracts/Signed_Agreement.pdf
```

### What Claude Will Do

1. Open the PDF file
2. Check total page count
3. Extract pages at indices 6-7 (pages 7-8 in the viewer)
4. Save to the specified location
5. Report:
   - Total pages in source (50)
   - Pages extracted (2)
   - Output file location
   - Whether repair was needed

### Expected Output

```
✓ PDF Operation Complete

Operation: Extracted pages 7-8 from contract bundle
Input:  Contract_Bundle_2025.pdf (50 pages)
Output: Signed_Agreement.pdf (2 pages)
Status: Success (no repair needed)
```

---

## Example 2: Merge Scanned Documents

### Scenario
You scanned a document in multiple parts and have separate PDF files for each page.

### What to Say to Claude

```
I have three scanned PDFs that I need to merge into one document:

1. /Users/username/Documents/Scans/scan_page1.pdf
2. /Users/username/Documents/Scans/scan_page2.pdf
3. /Users/username/Documents/Scans/scan_page3.pdf

Please merge them in this order and save as:
/Users/username/Documents/Scans/Complete_Scan.pdf
```

### What Claude Will Do

1. Open each PDF in order
2. Combine all pages sequentially
3. Save merged result
4. Report total pages and files merged

### Code Claude Uses

```python
merge_pdfs(
    input_paths=[
        '/Users/username/Documents/Scans/scan_page1.pdf',
        '/Users/username/Documents/Scans/scan_page2.pdf',
        '/Users/username/Documents/Scans/scan_page3.pdf'
    ],
    output_path='/Users/username/Documents/Scans/Complete_Scan.pdf'
)
```

---

## Example 3: Extract First Page from Multiple PDFs

### Scenario
You have a directory with 10 PDF reports and need just the first page (cover page) from each.

### What to Say to Claude

```
I have multiple PDF reports in this directory:
/Users/ranjithgonugunta/Documents/Reports/

Please extract the first page from each PDF and save them as:
filename_cover.pdf
```

### What Claude Will Do

1. List all PDF files in the directory
2. For each PDF:
   - Extract page 1 (index 0)
   - Save as {original_name}_cover.pdf
3. Report summary of all files processed

### Batch Processing Code

```python
import os
from pathlib import Path

source_dir = Path('/Users/ranjithgonugunta/Documents/Reports/')

for pdf_file in source_dir.glob('*.pdf'):
    output_name = pdf_file.stem + '_cover.pdf'
    output_path = source_dir / output_name

    extract_pages(
        input_path=str(pdf_file),
        output_path=str(output_path),
        start_page=0,
        end_page=0
    )
```

---

## Example 4: Split PDF into Sections

### Scenario
You have a 100-page document that you want to split into four 25-page sections.

### What to Say to Claude

```
I have a 100-page PDF document at:
/Users/ranjithgonugunta/Documents/large_document.pdf

Please split it into 4 sections:
- Section 1: Pages 1-25
- Section 2: Pages 26-50
- Section 3: Pages 51-75
- Section 4: Pages 76-100

Save them as section_1.pdf, section_2.pdf, etc.
```

### What Claude Will Do

```python
# Section 1 (pages 1-25 = indices 0-24)
extract_pages('large_document.pdf', 'section_1.pdf', 0, 24)

# Section 2 (pages 26-50 = indices 25-49)
extract_pages('large_document.pdf', 'section_2.pdf', 25, 49)

# Section 3 (pages 51-75 = indices 50-74)
extract_pages('large_document.pdf', 'section_3.pdf', 50, 74)

# Section 4 (pages 76-100 = indices 75-99)
extract_pages('large_document.pdf', 'section_4.pdf', 75, 99)
```

---

## Example 5: Repair and Process Corrupted PDF

### Scenario
You have a PDF that won't open in your viewer. You need to repair it and then extract certain pages.

### What to Say to Claude

```
I have a corrupted PDF at:
/Users/ranjithgonugunta/Documents/corrupted.pdf

Please repair it and then extract pages 10-20.
```

### What Claude Will Do

1. Attempt to open the PDF
2. If it fails, try repair with pikepdf
3. If that fails, try repair with Ghostscript
4. Once repaired, extract the requested pages
5. Report which repair method worked

### Repair Process

```python
# Claude tries:
# 1. Direct open
try:
    pdf = PyPDF2.PdfReader('corrupted.pdf')
except:
    # 2. pikepdf repair
    if repair_with_pikepdf('corrupted.pdf', 'repaired.pdf'):
        pdf = PyPDF2.PdfReader('repaired.pdf')
    else:
        # 3. Ghostscript repair
        if repair_with_ghostscript('corrupted.pdf', 'repaired.pdf'):
            pdf = PyPDF2.PdfReader('repaired.pdf')
        else:
            raise Error("Cannot repair")

# Then extract
extract_pages('repaired.pdf', 'output.pdf', 9, 19)  # Pages 10-20
```

---

## Example 6: Remove Pages by Extracting Around Them

### Scenario
You have a 20-page document and want to remove pages 5-7.

### What to Say to Claude

```
I have a 20-page PDF and I need to remove pages 5-7.

Input: /Users/ranjithgonugunta/Documents/document.pdf
Output: /Users/ranjithgonugunta/Documents/document_edited.pdf
```

### What Claude Will Do

1. Extract pages 1-4 to temp1.pdf (indices 0-3)
2. Extract pages 8-20 to temp2.pdf (indices 7-19)
3. Merge temp1.pdf and temp2.pdf
4. Clean up temporary files

### Implementation

```python
# Extract before the removed section
extract_pages('document.pdf', 'temp_part1.pdf', 0, 3)  # Pages 1-4

# Extract after the removed section
extract_pages('document.pdf', 'temp_part2.pdf', 7, 19)  # Pages 8-20

# Merge the parts
merge_pdfs(['temp_part1.pdf', 'temp_part2.pdf'], 'document_edited.pdf')

# Clean up
os.remove('temp_part1.pdf')
os.remove('temp_part2.pdf')
```

---

## Example 7: Get PDF Information

### Scenario
You need to know how many pages a PDF has before processing it.

### What to Say to Claude

```
How many pages are in this PDF?
/Users/ranjithgonugunta/Documents/report.pdf

Also show me any metadata like title and author.
```

### What Claude Will Do

```python
info = get_pdf_info('/Users/ranjithgonugunta/Documents/report.pdf')
```

### Output

```
📄 PDF Information
   File: report.pdf
   Total pages: 45
   Title: Annual Report 2024
   Author: John Doe
   Creator: Microsoft Word
```

---

## Example 8: Merge PDFs from Different Directories

### Scenario
You need to combine PDFs from multiple locations into one final document.

### What to Say to Claude

```
Please merge these PDFs in this specific order:

1. /Users/ranjithgonugunta/Documents/Cover/cover.pdf
2. /Users/ranjithgonugunta/Documents/Sections/intro.pdf
3. /Users/ranjithgonugunta/Documents/Sections/chapter1.pdf
4. /Users/ranjithgonugunta/Documents/Sections/chapter2.pdf
5. /Users/ranjithgonugunta/Documents/Appendix/references.pdf

Output: /Users/ranjithgonugunta/Documents/Final/complete_book.pdf
```

### What Claude Will Do

Merge all files in the exact order specified, preserving all pages from each document.

---

## Example 9: Extract Last N Pages

### Scenario
You need the last 5 pages of a document but don't know the total page count.

### What to Say to Claude

```
Extract the last 5 pages from:
/Users/ranjithgonugunta/Documents/document.pdf
```

### What Claude Will Do

1. Get total page count (e.g., 50 pages)
2. Calculate: last 5 pages = pages 46-50 (indices 45-49)
3. Extract those pages

```python
info = get_pdf_info('document.pdf')
total = info['total_pages']  # 50
start = total - 5  # 45
end = total - 1    # 49

extract_pages('document.pdf', 'last_5_pages.pdf', start, end)
```

---

## Example 10: Create Custom Report by Merging Specific Pages

### Scenario
You have multiple source documents and need to create a custom report by extracting specific pages from each.

### What to Say to Claude

```
I need to create a custom report with these specific pages:

From document_A.pdf: pages 1, 3, 5
From document_B.pdf: pages 10-15
From document_C.pdf: page 1

Save the final report as: custom_report.pdf
```

### What Claude Will Do

```python
# Extract needed pages to temp files
extract_pages('document_A.pdf', 'temp_A.pdf', 0, 0)  # Page 1
extract_pages('document_A.pdf', 'temp_A2.pdf', 2, 2)  # Page 3
extract_pages('document_A.pdf', 'temp_A3.pdf', 4, 4)  # Page 5
extract_pages('document_B.pdf', 'temp_B.pdf', 9, 14)  # Pages 10-15
extract_pages('document_C.pdf', 'temp_C.pdf', 0, 0)  # Page 1

# Merge all extracted parts
merge_pdfs([
    'temp_A.pdf',
    'temp_A2.pdf',
    'temp_A3.pdf',
    'temp_B.pdf',
    'temp_C.pdf'
], 'custom_report.pdf')

# Clean up temp files
```

---

## Tips for Using This Skill

### 1. Be Specific with Page Numbers
- Always clarify if you mean viewer pages or indices
- Claude assumes viewer pages (human-readable)

### 2. Use Absolute Paths
- Full paths are more reliable: `/Users/username/Documents/file.pdf`
- Relative paths work but can be ambiguous

### 3. Check Output Directory Exists
Claude will create the output file but not the directory. Ensure the output directory exists.

### 4. Large Files
For very large PDFs (100+ MB), operations may take longer. Claude will keep you updated.

### 5. Encrypted PDFs
If a PDF is password-protected, you'll need to decrypt it first or provide the password.

### 6. Format Preservation
- Most formatting is preserved
- Some interactive features (forms, JavaScript) may not survive all operations
- Signatures will be invalidated

---

## Common Issues and Solutions

### Issue: "File not found"
**Solution**: Check the file path is correct and use absolute paths

### Issue: "Permission denied"
**Solution**: Ensure you have read access to input files and write access to output directory

### Issue: "Invalid page range"
**Solution**: Check the document's page count first with the info command

### Issue: "Cannot repair PDF"
**Solution**: The PDF may be too damaged or encrypted. Try decrypting first.

### Issue: "Module not found"
**Solution**: Install dependencies: `pip install PyPDF2 pikepdf`

---

## Advanced Patterns

### Pattern 1: Process All PDFs in Directory
```
Process all PDFs in /path/to/directory/ by extracting page 1 from each
```

### Pattern 2: Conditional Extraction
```
For each PDF in this directory, if it has more than 10 pages, extract the first and last page
```

### Pattern 3: Smart Merging
```
Merge all PDFs in this directory, sorted alphabetically by filename
```

### Pattern 4: Batch Repair
```
Try to repair all PDFs in this directory that won't open
```

---

## Next Steps

After using this skill, you might want to:

1. **Organize files**: Use file-management skill
2. **Extract text**: Use data-extraction skill
3. **Convert formats**: Use document-processing skill
4. **Analyze content**: Use text-analysis skill

---

**Skill Version**: 1.0.0
**Last Updated**: 2025
