# Python Skills Framework

A modular registry system for organizing reusable Python functionality. Each skill is a self-contained class that can be registered and discovered through a central manager.

## Structure

```
python_framework_implementation/
├── __init__.py          # SkillRegistry class + @skill decorator
├── skill_manager.py     # SkillManager class + get_skill() convenience function
├── requirements.txt     # Dependencies
├── pdf/
│   ├── __init__.py      # Exports PDFSkill + metadata
│   └── pdf_class.py     # PDFSkill implementation (merge, extract, repair)
└── examples/
    └── pdf_examples.py  # Usage examples
```

## Quick Start

```python
from python_framework_implementation.skill_manager import get_skill

pdf = get_skill('pdf')

# Merge PDFs
pdf.merge_pdfs(['doc1.pdf', 'doc2.pdf'], 'merged.pdf')

# Extract pages (0-indexed)
pdf.extract_pages('document.pdf', 'output.pdf', start_page=0, end_page=4)

# Get PDF info
info = pdf.get_info('document.pdf')
print(f"Pages: {info['total_pages']}")
```

## PDF Skill Methods

| Method | Description |
|--------|-------------|
| `merge_pdfs(input_paths, output_path)` | Merge a list of PDFs into one |
| `extract_pages(input, output, start, end)` | Extract page range (0-indexed, inclusive) |
| `get_info(pdf_path)` | Returns page count and metadata |
| `repair_with_pikepdf(input, output)` | Repair using pikepdf (requires qpdf) |
| `repair_with_ghostscript(input, output)` | Repair using Ghostscript fallback |

Repair is attempted automatically — if a PDF fails to open, pikepdf is tried first, then Ghostscript.

## Adding a New Skill

**1. Create the skill class** in a new subfolder:

```python
# python_framework_implementation/my_skill/my_skill.py
class MySkill:
    """Description of what this skill does."""

    def __init__(self):
        self.name = "My Skill"
        self.version = "1.0.0"

    def do_something(self, input_data: str) -> dict:
        return {'status': 'success', 'result': input_data}
```

**2. Create the package `__init__.py`:**

```python
# python_framework_implementation/my_skill/__init__.py
from .my_skill import MySkill

SKILL_NAME = 'my_skill'
SKILL_VERSION = '1.0.0'
SKILL_DESCRIPTION = 'What this skill does'
skill_class = MySkill

__all__ = ['MySkill', 'SKILL_NAME', 'SKILL_VERSION', 'SKILL_DESCRIPTION']
```

**3. Register it in `skill_manager.py`:**

```python
from .my_skill import MySkill
self.registry.register('my_skill', MySkill())
```

## Dependencies

Install via:
```bash
pip install -r python_framework_implementation/requirements.txt
```

| Package | Required | Purpose |
|---------|----------|---------|
| PyPDF2 | Yes | PDF read/write |
| pikepdf | Optional | PDF repair (needs `brew install qpdf`) |
| Ghostscript | Optional | PDF repair fallback (`brew install ghostscript`) |
