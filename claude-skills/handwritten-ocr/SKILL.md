---
name: handwritten-ocr
description: This skill should be used when the user wants to convert a scanned handwritten PDF into a Word document, or wants to launch the handwritten OCR web interface. Trigger phrases include "convert this handwritten PDF", "transcribe my handwritten notes", "OCR this scanned PDF", "extract text from handwritten PDF", "open the OCR web app", "launch handwritten OCR", "convert handwritten to Word", or "read my handwritten document".
---

# Handwritten OCR Skill

This skill converts scanned handwritten PDF files into editable Word (.docx) documents using Claude's Vision API. It supports two modes:

1. **CLI Mode** — Convert a PDF directly from the terminal. Progress is shown page by page. Output `.docx` is saved alongside the input file (or to a path you specify).
2. **Web App Mode** — Launch the full browser-based web interface with drag-and-drop upload, progress bar, and download button.

## App Location

The web app and all supporting code lives at:
```
/Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr/
```

The skill's own scripts live at:
```
~/.claude/skills/handwritten-ocr/scripts/
```

## Virtual Environment

Always use the app's isolated venv:
```bash
source /Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr/.venv/bin/activate
```

## Mode 1: CLI Conversion

Use this when the user provides a file path and wants the conversion done directly in the terminal without a browser.

### Trigger examples
- "Convert `/path/to/notes.pdf` to Word"
- "Transcribe my handwritten PDF at `~/Desktop/lecture.pdf`"
- "OCR this file: `/Users/ranjithgonugunta/Documents/notes.pdf`"

### How to run

```bash
source /Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr/.venv/bin/activate && \
python ~/.claude/skills/handwritten-ocr/scripts/run_ocr.py "/absolute/path/to/input.pdf"
```

With a custom output path:
```bash
source /Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr/.venv/bin/activate && \
python ~/.claude/skills/handwritten-ocr/scripts/run_ocr.py "/path/to/input.pdf" "/path/to/output.docx"
```

### What happens
1. PDF is validated and auto-repaired if needed (using existing PDFSkill)
2. Each page is rendered to a PNG image at 150 DPI
3. Each image is sent to Claude Vision API — text is extracted page by page
4. A `.docx` file is built with page breaks matching the original PDF
5. Output path is printed when complete

### Output
- Default output: same directory as input, with `.docx` extension
  - e.g. `/path/to/notes.pdf` → `/path/to/notes.docx`
- Custom output: whatever path is specified as the second argument

---

## Mode 2: Launch Web App

Use this when the user wants to use the browser UI — drag and drop upload, visual progress bar, download button.

### Trigger examples
- "Open the handwritten OCR web app"
- "Launch the OCR interface"
- "Start the OCR web server"
- "I want to use the web interface for OCR"

### How to run

```bash
python ~/.claude/skills/handwritten-ocr/scripts/launch_webapp.py
```

### What happens
1. Checks if the Flask server is already running on port 5001
2. If not running: starts it in the background using the app's venv
3. Opens `http://127.0.0.1:5001` in the default browser automatically
4. Prints the URL for reference

### Stopping the web app
```bash
lsof -ti:5001 | xargs kill -9
```

---

## Environment Variables

The ANTHROPIC_API_KEY must be set. It is loaded from:
```
/Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr/.env
```

If the key is missing, both modes will fail with a clear error message. To set it:
```bash
echo "ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE" > /Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr/.env
```

---

## Architecture (for reference)

```
claude-skills/handwritten-ocr/
├── app.py                  # Flask web server
├── config.py               # Loads .env, defines constants
├── core/
│   ├── pdf_to_images.py    # PDF → PNG bytes (PyMuPDF); reuses PDFSkill for repair
│   ├── claude_ocr.py       # Claude Vision API → extracted text per page
│   ├── docx_builder.py     # Assembles text into .docx with page breaks
│   └── processor.py        # Orchestrator (background thread + job store)
├── templates/index.html    # Web UI (drag/drop, progress bar, download)
├── static/                 # CSS + JS for web UI
├── uploads/                # Temp uploaded PDFs (auto-deleted after processing)
└── outputs/                # Generated .docx files
```

---

## Troubleshooting

### "ANTHROPIC_API_KEY is not configured"
→ Add your key to `/Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr/.env`

### "ModuleNotFoundError"
→ Ensure you activated the correct venv:
```bash
source /Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr/.venv/bin/activate
```

### "Port 5001 already in use"
→ Stop the existing server:
```bash
lsof -ti:5001 | xargs kill -9
```

### PDF fails to open
→ The skill uses PDFSkill's auto-repair (pikepdf → Ghostscript). If both fail, the PDF may be severely corrupted or encrypted.

### Poor OCR accuracy
→ Try scanning at higher DPI (300+). The skill renders at 150 DPI by default — to change this, edit `PDF_RENDER_DPI` in `config.py`.
