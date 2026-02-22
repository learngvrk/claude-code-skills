# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python utilities repository focused on:
1. **PDF Manipulation** - Tools for merging, extracting pages, and repairing PDFs
2. **Claude Skills** - Anthropic Skills format for AI-assisted PDF operations
3. **Call Analytics** - Audio transcription (Whisper) and text summarization (NLTK)

## Project Structure

```
/Users/ranjithgonugunta/Documents/Python/
├── tools/                    # Standalone PDF utilities
│   └── pdf.py               # Core PDF functions (merge, extract, repair)
├── claude-skills/           # Anthropic Skills format (SKILL.md based)
│   └── pdf-manipulation/    # AI-loadable PDF skill
├── skills/                  # Python skills registry system
│   ├── skill_manager.py     # get_skill('pdf') interface
│   └── pdf_skill/           # PDFSkill class wrapper
└── Call_Analytics/          # Audio processing utilities
    ├── whisper_m4a.py       # Whisper transcription
    └── summarize.py         # NLTK extractive summarization
```

## Common Commands

### PDF Operations

```bash
# Install dependencies
pip install PyPDF2 pikepdf

# Using skills system
python -c "from skills.skill_manager import get_skill; pdf = get_skill('pdf')"

# Direct script usage
python tools/pdf.py
```

### Call Analytics

```bash
# Install dependencies
pip install openai-whisper nltk

# Transcribe audio
python Call_Analytics/whisper_m4a.py

# Summarize transcript
python Call_Analytics/summarize.py
```

## Architecture

### Two Skills Systems

This repo has two parallel approaches to skills:

1. **Anthropic Skills** (`claude-skills/`): Uses `SKILL.md` files with YAML frontmatter that Claude automatically loads. The pdf-manipulation skill lives here.

2. **Python Skills Registry** (`skills/`): A programmatic approach using `SkillManager` and a registry pattern. Access via `get_skill('pdf')`.

Both wrap the same underlying functionality from `tools/pdf.py`.

### PDF Processing Flow

```
Input PDF → PyPDF2.PdfReader → [Repair if needed] → PyPDF2.PdfWriter → Output PDF
                                    ↓
                            pikepdf (try first)
                                    ↓
                            Ghostscript (fallback)
```

### Page Numbering Convention

- **0-indexed internally**: Page 7 in a PDF viewer = index 6 in code
- `extract_pages(path, out, start_page=6, end_page=7)` extracts pages 7-8 (viewer numbering)

## Key Files

- `tools/pdf.py:50` - `extract_pages()` with auto-repair
- `tools/pdf.py:92` - `merge_pdfs()` function
- `skills/skill_manager.py:83` - `get_skill()` convenience function
- `claude-skills/pdf-manipulation/SKILL.md` - Anthropic skill definition

## Dependencies

### PDF Processing
- PyPDF2 >= 3.0.0
- pikepdf >= 8.0.0 (optional, for repair)
- Ghostscript (system package, `brew install ghostscript`)
- qpdf (system package, `brew install qpdf`)

### Call Analytics
- openai-whisper
- nltk (with stopwords and punkt tokenizer)
