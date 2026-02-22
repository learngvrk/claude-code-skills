# Claude Code Skills — PDF & Handwritten OCR

> **Teach Claude a skill once. Use it forever — in plain English or through a web interface.**

This repository shows how to build **Claude Code Skills** for real, recurring tasks: PDF manipulation and converting handwritten scanned documents into editable Word files. Each skill can be triggered by a simple natural language prompt in the Claude Code terminal *or* through a full drag-and-drop web UI — same code underneath, two completely different user experiences.

---

## What's Inside

```
claude-code-skills/
│
├── claude-skills/
│   ├── pdf-skills/            ← Skill 1: Merge, extract & repair PDFs
│   └── handwritten-ocr/       ← Skill 2: Handwritten PDF → Word (.docx)
│                                  + full Flask web app with drag-and-drop UI
│
├── python_framework_implementation/  ← Reusable Python PDFSkill class & registry
└── python_tools/              ← Original standalone PDF utility scripts
```

---

## Skill 1 — PDF Manipulation (`claude-skills/pdf-skills/`)

A `SKILL.md` that teaches Claude how to:

| Capability | Example prompt |
|---|---|
| **Merge PDFs** | *"Merge these three scanned PDFs into one document"* |
| **Extract pages** | *"Extract pages 7–10 from this file and save as output.pdf"* |
| **Repair corrupted PDFs** | *"This PDF is broken, can you fix it?"* |

Claude handles the code, the edge cases, and the 0-indexed page math. You just describe what you want.

**Repair strategy** (automatic fallback):
```
pikepdf  →  Ghostscript  →  Error with clear message
```

### Install

```bash
# Copy to Claude's skills directory
cp -r claude-skills/pdf-skills ~/.claude/skills/

# Install dependencies
pip install PyPDF2>=3.0.0 pikepdf>=8.0.0
brew install qpdf ghostscript   # macOS
```

### Use

Just ask Claude Code in plain English:
```
> merge doc1.pdf and doc2.pdf into combined.pdf
> extract pages 3 to 7 from report.pdf
> repair this corrupted PDF: broken.pdf
```

---

## Skill 2 — Handwritten OCR (`claude-skills/handwritten-ocr/`)

Converts scanned handwritten PDFs into editable Word (`.docx`) documents using **Claude's Vision API**. Each page is rendered as an image, sent to Claude for transcription, and assembled into a Word document with matching page breaks.

This skill works in **two modes** — same underlying code, different interfaces:

---

### Mode A — Claude Code Terminal (CLI)

Type a natural language prompt. Claude renders pages, calls Vision API page by page, and saves the `.docx` next to your original file — all with live progress printed in the terminal.

```
> convert my handwritten notes at ~/Desktop/lecture.pdf to Word
```

**Terminal output:**
```
Handwritten OCR — CLI Mode
──────────────────────────────────────────────────
Input:  /Users/you/Desktop/lecture.pdf
Output: /Users/you/Desktop/lecture.docx
Model:  claude-sonnet-4-6
──────────────────────────────────────────────────

Step 1/3  Rendering PDF pages to images...
          4 page(s) found.

Step 2/3  Extracting handwritten text with Claude Vision...
          Page 1/4... done  [Dear John, I wanted to write to you...]
          Page 2/4... done  [The meeting was rescheduled for Monday...]
          Page 3/4... done  [Please find enclosed the signed agreement...]
          Page 4/4... done  [Regards, Ranjith]

Step 3/3  Building Word document...

──────────────────────────────────────────────────
Done!  Output saved to:
  /Users/you/Desktop/lecture.docx
──────────────────────────────────────────────────
```

---

### Mode B — Web Interface (Browser UI)

Say *"open the OCR web app"* and Claude starts the Flask server in the background and opens your browser automatically. From there it's point-and-click: drag, drop, watch progress, download.

```
> open the handwritten OCR web app
```

![Web UI: drag-and-drop upload → page-by-page progress bar → download button]

**Features:**
- Drag-and-drop PDF upload (up to 50 MB)
- Animated page-by-page progress bar
- One-click `.docx` download
- Works entirely locally — no data leaves your machine except the API call to Claude

---

### How it works (under the hood)

```
Uploaded PDF
    │
    ▼
PyMuPDF renders each page → PNG image (150 DPI)
    │
    ▼
Claude Vision API (claude-sonnet-4-6)
    │   base64 PNG → extracted handwritten text
    ▼
python-docx assembles pages
    │   with hard page breaks between each original page
    ▼
  output.docx
```

---

### Install

```bash
# Copy skill to Claude's skills directory
cp -r claude-skills/handwritten-ocr ~/.claude/skills/

# Set up the web app
cd claude-skills/handwritten-ocr
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Add your Anthropic API key
echo "ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE" > .env
```

### Use

**CLI mode** — ask Claude Code:
```
> convert ~/Desktop/notes.pdf to Word
> transcribe my handwritten PDF at ~/Documents/lecture.pdf
```

**Web UI mode** — ask Claude Code:
```
> open the OCR web app
> launch the handwritten OCR interface
```
Or start the server directly:
```bash
source claude-skills/handwritten-ocr/.venv/bin/activate
python claude-skills/handwritten-ocr/app.py
# → open http://127.0.0.1:5001 in your browser
```

---

## Python Framework (`python_framework_implementation/`)

A programmatic Python registry for the same PDF capabilities — importable in any Python script, no Claude required.

```python
from python_framework_implementation.skill_manager import get_skill

pdf = get_skill('pdf')

pdf.merge_pdfs(['doc1.pdf', 'doc2.pdf'], 'merged.pdf')
pdf.extract_pages('report.pdf', 'pages_3_to_7.pdf', start_page=2, end_page=6)

info = pdf.get_info('document.pdf')
print(f"Pages: {info['total_pages']}")
```

The handwritten OCR web app imports this directly for PDF pre-flight validation and auto-repair — so the Claude Skill and the Flask web app share real code underneath.

---

## Two Skill Systems Explained

This repo deliberately shows **two parallel approaches** to skills — a distinction worth understanding:

| | `claude-skills/` SKILL.md | `python_framework_implementation/` |
|---|---|---|
| **What it is** | Markdown instructions Claude reads | Real executable Python class |
| **Runs in** | Claude's language model context | Python interpreter |
| **Triggered by** | Natural language prompt | `import` / `get_skill('pdf')` |
| **Works without Claude?** | ❌ No | ✅ Yes |
| **Best for** | Teaching Claude how to reason and act | Code reuse across apps and scripts |

---

## Requirements

### System (macOS)
```bash
brew install ghostscript qpdf
```

### Python
```bash
# PDF skills
pip install PyPDF2>=3.0.0 pikepdf>=8.0.0

# Handwritten OCR web app
pip install flask python-dotenv PyMuPDF anthropic python-docx PyPDF2 pikepdf
```

### API Key
An **Anthropic API key** is required for the handwritten OCR skill (Claude Vision).
Get one at [console.anthropic.com](https://console.anthropic.com).

```bash
echo "ANTHROPIC_API_KEY=sk-ant-YOUR_KEY" > claude-skills/handwritten-ocr/.env
```

---

## Quick Start (5 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/learngvrk/claude-code-skills.git
cd claude-code-skills

# 2. Install the PDF skill
cp -r claude-skills/pdf-skills ~/.claude/skills/
pip install PyPDF2 pikepdf

# 3. Install the OCR skill + web app
cp -r claude-skills/handwritten-ocr ~/.claude/skills/
cd claude-skills/handwritten-ocr
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-YOUR_KEY" > .env

# 4. Open Claude Code and try it
# > merge doc1.pdf and doc2.pdf into one
# > convert my handwritten notes at ~/Desktop/scan.pdf to Word
# > open the OCR web app
```

---

## The Architecture Insight

The most interesting thing about this repo isn't any individual skill — it's the **layered architecture** that emerges:

```
Plain English prompt (Claude Code terminal)
        ↓
   SKILL.md — Claude reads this, decides what to do
        ↓
   Python scripts — Claude runs these, or they run standalone
        ↓
   PDFSkill class — shared by both the skill and the web app
        ↓
   Web UI — same pipeline, browser interface for non-technical users
```

One skill, built once, usable by developers in the terminal and by anyone else in a browser.

---

## Blog Post

Full story on how this was built, the architecture decisions, and what I'd do differently:

- 📝 **Medium** *(coming soon)*
- 💼 **LinkedIn** *(coming soon)*

---

## License

MIT — use, modify, and share freely.
