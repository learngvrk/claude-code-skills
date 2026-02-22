# Claude Skills

This folder contains **Claude Code Skills** — markdown-based knowledge packages that teach Claude how to perform specific tasks when you ask in plain English.

## Available Skills

### 📄 `pdf-skills/` — PDF Manipulation

Merge, extract pages, and repair corrupted PDFs.

**Install:**
```bash
cp -r pdf-skills ~/.claude/skills/
pip install PyPDF2 pikepdf
```

**Use** (in Claude Code):
```
> merge doc1.pdf and doc2.pdf into combined.pdf
> extract pages 3 to 7 from report.pdf
> repair this corrupted PDF: broken.pdf
```

---

### ✍️ `handwritten-ocr/` — Handwritten PDF to Word

Convert scanned handwritten PDFs into editable `.docx` files using Claude Vision API. Works via terminal prompt **or** a full browser-based web UI.

**Install:**
```bash
cp -r handwritten-ocr ~/.claude/skills/
cd handwritten-ocr
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-YOUR_KEY" > .env
```

**Use** (in Claude Code):
```
> convert ~/Desktop/notes.pdf to Word        ← CLI mode, terminal progress
> open the OCR web app                        ← launches browser UI automatically
```

---

## How Skills Work

A skill is a folder with a `SKILL.md` file. Claude reads it automatically when your request matches the skill's description, then uses the guidance inside to act — writing and running code on your behalf.

```
Your prompt → Claude matches skill → Loads SKILL.md → Executes
```

See the root [README.md](../README.md) for the full architecture explanation.
