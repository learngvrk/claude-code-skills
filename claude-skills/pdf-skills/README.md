# PDF Manipulation Skill

An Anthropic Skill for expert PDF manipulation including merging, extracting pages, and repairing corrupted PDFs.

## What is This?

This is an **Anthropic Skill** that you can add to Claude to give it expert PDF manipulation capabilities. When you install this skill, Claude will automatically use it whenever you need to work with PDF files.

## Installation

### For Claude Desktop

1. Copy this entire `pdf-manipulation` folder to your Claude skills directory:
   ```bash
   cp -r pdf-manipulation ~/.claude/skills/
   ```

2. Install Python dependencies:
   ```bash
   pip install PyPDF2>=3.0.0 pikepdf>=8.0.0
   ```

3. (Optional) Install system tools for PDF repair:
   ```bash
   # macOS
   brew install qpdf ghostscript

   # Ubuntu/Debian
   sudo apt-get install qpdf ghostscript

   # Windows
   # Download from: https://www.ghostscript.com/
   ```

4. Restart Claude Desktop

### For Claude API

Upload the skill using the Skills API:

```python
import anthropic

client = anthropic.Anthropic()

# Upload the skill
with open('pdf-manipulation/SKILL.md', 'r') as f:
    skill_content = f.read()

# Use in your API calls with skills parameter
```

## Capabilities

### 1. Merge PDFs
Combine multiple PDF files into one document.

**Example prompt:**
> "Merge these three PDF files into one: file1.pdf, file2.pdf, file3.pdf"

### 2. Extract Pages
Extract specific page ranges from PDFs.

**Example prompts:**
> "Extract pages 7-8 from the document packet"
> "Get just the first page from this document"
> "Extract pages 10 through 20 from the report"

### 3. Repair Corrupted PDFs
Automatically detect and repair corrupted PDF files.

**Example prompt:**
> "This PDF won't open, can you repair it?"

## Usage Examples

### Example 1: Extract Signed Agreement from Contract Bundle

**Your prompt:**
```
Extract pages 7-8 from this contract bundle:
/Users/username/Documents/Contracts/Contract_Bundle_2025.pdf

Save it as:
/Users/username/Documents/Contracts/Signed_Agreement.pdf
```

**What Claude will do:**
- Open the PDF (repairing if needed)
- Extract pages at indices 6-7 (pages 7-8 in viewer)
- Save to the specified location
- Report success with page counts

### Example 2: Merge Scanned Documents

**Your prompt:**
```
Merge these scanned pages into one PDF:
- scan_page1.pdf
- scan_page2.pdf
- scan_page3.pdf

Output: complete_scan.pdf
```

**What Claude will do:**
- Read all input PDFs
- Combine them in order
- Report total page count
- Confirm output location

### Example 3: Batch Page Extraction

**Your prompt:**
```
Extract the first page from all PDFs in this directory:
/Users/username/Documents/reports/
```

**What Claude will do:**
- Find all PDFs in the directory
- Extract page 1 from each
- Save as filename_page1.pdf
- Report summary

## Command-Line Usage

You can also use the included script directly:

```bash
# Extract pages
python scripts/pdf_operations.py extract input.pdf 0 5 -o output.pdf

# Merge PDFs
python scripts/pdf_operations.py merge file1.pdf file2.pdf file3.pdf -o merged.pdf

# Get PDF info
python scripts/pdf_operations.py info document.pdf

# Repair PDF
python scripts/pdf_operations.py repair corrupted.pdf -o repaired.pdf
```

## File Structure

```
pdf-manipulation/
├── SKILL.md                    # Skill instructions for Claude
├── README.md                   # This file
├── scripts/
│   └── pdf_operations.py       # Complete implementation
└── examples/
    └── usage_examples.md       # More detailed examples
```

## How It Works

1. **Discovery**: When you chat with Claude, it scans the skill's name and description
2. **Activation**: If your request involves PDF manipulation, Claude loads this skill
3. **Execution**: Claude follows the instructions in SKILL.md to help you
4. **Scripts**: Claude can run the included Python scripts for actual operations

## Requirements

### Required
- Python 3.7+
- PyPDF2 3.0.0+

### Optional (for PDF repair)
- pikepdf 8.0.0+ (requires qpdf system package)
- Ghostscript (system package)

## Important Notes

### Page Numbering
- **In prompts**: Use human-readable page numbers (1, 2, 3...)
- **In code**: Pages are 0-indexed (0, 1, 2...)
- Claude handles the conversion automatically

Example:
- "Extract page 7" → Claude uses index 6
- "Pages 1-5" → Claude uses indices 0-4

### File Paths
- Use absolute paths for reliability
- Paths with spaces work fine
- Check that input files exist
- Ensure output directories exist

### Repair Capabilities
- **pikepdf**: Best for structure issues, requires qpdf
- **Ghostscript**: Good fallback, may modify formatting
- Not all PDFs can be repaired
- Encrypted PDFs need password first

## Troubleshooting

### "Module not found: PyPDF2"
```bash
pip install PyPDF2 pikepdf
```

### "qpdf not found"
```bash
# macOS
brew install qpdf

# Linux
sudo apt-get install qpdf
```

### "Ghostscript not found"
```bash
# macOS
brew install ghostscript

# Linux
sudo apt-get install ghostscript
```

### "Page out of range"
The PDF has fewer pages than requested. Claude will adjust the range automatically.

### "Cannot open PDF"
The PDF may be corrupted. Claude will attempt repair automatically.

## Contributing

To improve this skill:

1. Edit `SKILL.md` to add better instructions
2. Update `scripts/pdf_operations.py` to add features
3. Add examples to `examples/usage_examples.md`
4. Test thoroughly before using in production

## License

This skill is provided as-is for use with Claude. Modify as needed for your use case.

## Related Skills

- **document-processing**: For converting between document formats
- **file-management**: For organizing files and directories
- **data-extraction**: For extracting structured data from PDFs

## Version

**Version**: 1.0.0
**Last Updated**: 2025
**Anthropic Skills Format**: v1

---

## Quick Reference

**Skill Name**: `pdf-manipulation`

**Key Commands for Claude**:
- "Merge these PDFs: ..."
- "Extract pages X-Y from ..."
- "Repair this corrupted PDF: ..."
- "Get info about this PDF: ..."
- "Extract all pages from X to Y..."

**Dependencies**:
- PyPDF2 (required)
- pikepdf (optional, for repair)
- Ghostscript (optional, for repair)
