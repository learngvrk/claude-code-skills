# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python utilities repository focused on:
1. **PDF Manipulation** - Tools for merging, extracting pages, and repairing PDFs
2. **Claude Skills** - Anthropic Skills format for AI-assisted PDF operations and Handwritten OCR

## Project Structure

```
/Users/ranjithgonugunta/Documents/Python/
├── python_tools/                     # Standalone PDF utilities
│   └── pdf.py                        # Core PDF functions (merge, extract, repair)
├── claude-skills/                    # Anthropic Skills format (SKILL.md based)
│   ├── pdf-skills/                   # AI-loadable PDF skill (merge, extract, repair)
│   │   └── SKILL.md
│   └── handwritten-ocr/             # Handwritten PDF → Word skill + Flask web app
│       ├── SKILL.md
│       ├── skills-scripts/           # Launcher scripts (CLI + web UI)
│       ├── app.py                    # Flask web server
│       ├── config.py
│       ├── core/                     # OCR pipeline (PyMuPDF, Claude Vision, docx)
│       ├── templates/                # Web UI
│       └── requirements.txt
└── python_framework_implementation/ # Python skills registry system
    ├── skill_manager.py              # get_skill('pdf') interface
    └── pdf/                          # PDFSkill class wrapper
```

## Common Commands

### PDF Skill

```bash
# Install dependencies
pip install PyPDF2 pikepdf
brew install ghostscript qpdf

# Register skill with Claude Code
cp -r claude-skills/pdf-skills ~/.claude/skills/
```

### Handwritten OCR Skill

```bash
# Install dependencies
cd claude-skills/handwritten-ocr
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-YOUR_KEY" > .env

# Register skill with Claude Code
mkdir -p ~/.claude/skills/handwritten-ocr/scripts
cp claude-skills/handwritten-ocr/SKILL.md ~/.claude/skills/handwritten-ocr/
cp claude-skills/handwritten-ocr/skills-scripts/*.py ~/.claude/skills/handwritten-ocr/scripts/
```

### Python Framework (no Claude required)

```bash
python -c "from python_framework_implementation.skill_manager import get_skill; pdf = get_skill('pdf')"
```

## Architecture

### Two Skills Systems

This repo has two parallel approaches to skills:

1. **Anthropic Skills** (`claude-skills/`): Uses `SKILL.md` files with YAML frontmatter that Claude automatically loads. Triggered by natural language prompts in Claude Code.

2. **Python Skills Registry** (`python_framework_implementation/`): A programmatic approach using `SkillManager` and a registry pattern. Importable in any Python script without Claude.

Both wrap the same underlying functionality from `python_tools/pdf.py`.

### PDF Processing Flow

```
Input PDF → PyPDF2.PdfReader → [Repair if needed] → PyPDF2.PdfWriter → Output PDF
                                    ↓
                            pikepdf (try first)
                                    ↓
                            Ghostscript (fallback)
```

### Handwritten OCR Flow

```
Scanned PDF
    → PyMuPDF renders each page → PNG (150 DPI)
    → Claude Vision API transcribes handwriting
    → python-docx assembles output with page breaks
    → output.docx
```

### Page Numbering Convention

- **0-indexed internally**: Page 7 in a PDF viewer = index 6 in code
- `extract_pages(path, out, start_page=6, end_page=7)` extracts pages 7-8 (viewer numbering)

## Key Files

- `python_tools/pdf.py` - Core PDF functions (merge, extract, repair)
- `python_framework_implementation/skill_manager.py` - `get_skill()` convenience function
- `claude-skills/pdf-skills/SKILL.md` - PDF manipulation skill definition
- `claude-skills/handwritten-ocr/SKILL.md` - Handwritten OCR skill definition
- `claude-skills/handwritten-ocr/skills-scripts/run_ocr.py` - CLI launcher
- `claude-skills/handwritten-ocr/skills-scripts/launch_webapp.py` - Web UI launcher
- `claude-skills/handwritten-ocr/core/` - OCR pipeline modules

## Dependencies

### PDF Processing
- PyPDF2 >= 3.0.0
- pikepdf >= 8.0.0 (optional, for repair)
- Ghostscript (system package, `brew install ghostscript`)
- qpdf (system package, `brew install qpdf`)

### Handwritten OCR
- PyMuPDF >= 1.24.0 (PDF to image rendering)
- anthropic >= 0.34.0 (Claude Vision API)
- python-docx >= 1.1.0 (Word document assembly)
- flask >= 3.0.0 (web UI)
- python-dotenv >= 1.0.0
