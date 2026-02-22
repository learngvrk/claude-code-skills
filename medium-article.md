# Teaching Claude a Skill: How I Built PDF Manipulation and Handwriting OCR as Reusable AI Skills (With a Web UI Too)

*A practical walkthrough of Claude Code Skills — what they are, how they work, and what I got wrong along the way*

---

## The Saturday Morning Problem

I had two recurring frustrations.

The first was PDF wrangling. Every few days I'd need to merge a set of scanned documents, extract a specific page range from a large file, or deal with a corrupted PDF that refused to open. Each time I'd either write a quick Python script from scratch, paste code from Stack Overflow, or just ask Claude to write something in the chat. Each solution worked exactly once. Nothing carried over.

The second was worse. I had a stack of handwritten notes — lecture notes, meeting summaries, personal documents — as scanned PDFs. Every time I needed to reference or edit them, I was retyping page by page. By hand. In 2025.

Both felt like problems that *should* be solved. So I decided to solve them properly — not just with a one-off script, but in a way that would make them permanently available with a simple ask.

That's when I discovered Claude Code Skills.

---

## What Are Claude Code Skills?

Most people use Claude the same way they use a search engine: ask a question, get an answer, move on. The answer lives in the chat and nowhere else.

**Skills are different.** A Skill is a folder containing a special file called `SKILL.md` — a markdown document that teaches Claude *how* to perform a category of work. Not just what to do once, but the patterns, the edge cases, the exact tools and commands to use, and when to apply each approach.

Once a skill is installed in `~/.claude/skills/`, Claude scans its name and description at startup. When you make a request that matches, Claude automatically loads the full skill and applies that expertise — generating and running code guided by everything you've documented.

The mental model that clicked for me: **a SKILL.md is institutional knowledge, not a script.** You're not writing code for Claude to execute. You're writing a knowledge base that shapes how Claude reasons and what code it produces.

A minimal skill looks like this:

```
---
name: pdf-skills
description: Use when merging PDFs, extracting pages, or repairing corrupted files.
---

# PDF Skills

## Merging PDFs
Use PyPDF2.PdfWriter. Loop through each input file...
```

That's genuinely it. The YAML frontmatter at the top is what Claude reads at startup to decide whether to load the skill. Everything below it is the expertise Claude consults when it does.

---

## Skill #1 — PDF Manipulation

The first skill I built covers three capabilities:

- **Merge** — combine multiple PDFs preserving all pages and content
- **Extract** — pull out a specific page range into a new file
- **Repair** — automatically fix corrupted PDFs using a two-stage fallback strategy

The repair logic is the most interesting part. PDFs can be corrupted in different ways, and no single tool handles everything. So the skill teaches Claude a cascade:

```
Try pikepdf first  →  Try Ghostscript as fallback  →  Surface clear error if both fail
```

The skill also permanently captures one of those details that always trips people up: **page indexing**. PDF viewers show page 1, but the code uses index 0. Page 7 in the viewer is index 6 in code. Every time I wrote a PDF script without a skill, I had to remember this. Now it's documented once in the SKILL.md:

```
### Page Numbering
- Always use 0-indexed pages in code
- Page 1 in a PDF viewer = index 0 in code
- When user says "page 7", use index 6
```

Now when I ask *"extract pages 7 to 10 from this file"*, Claude applies the right indices automatically. The knowledge lives in the skill, not in my head.

**Using it is just plain English:**

```
> merge doc1.pdf and doc2.pdf into combined.pdf
> extract pages 3 to 7 from report.pdf
> this PDF is corrupted, can you repair it?
```

---

## Skill #2 — Handwritten OCR

This one is more ambitious. The goal: upload a scanned handwritten PDF, get back an editable Word document with the text faithfully transcribed, page by page.

The engine is **Claude's Vision API** — the same model, reading images. Each page of the PDF is rendered as a PNG, sent to Claude with a transcription prompt, and the extracted text is assembled into a `.docx` file with hard page breaks matching the original PDF layout.

The pipeline:

```
PDF
 → PyMuPDF renders each page as PNG (150 DPI)
 → Base64 encode each image
 → Claude Vision API: "Transcribe all handwritten text exactly as written"
 → python-docx assembles text with page breaks between each original page
 → output.docx
```

I chose PyMuPDF over the more common `pdf2image` library deliberately — `pdf2image` requires poppler to be installed as a system binary, which is one more dependency to document and manage. PyMuPDF bundles its own rendering engine, so it's a pure pip install with no system dependencies.

---

## The Twist: Two Interfaces, One Skill

Here's where it gets interesting. The OCR skill works in **two completely different ways** — same core code underneath, two entirely different user experiences.

### Interface 1 — The Claude Code Terminal

Just describe what you want in plain English. Claude runs the whole pipeline, prints page-by-page progress directly in the terminal, and saves the `.docx` file next to your original PDF. No browser, no setup.

```
> convert my handwritten notes at ~/Desktop/lecture.pdf to Word
```

Terminal output:

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
Done!  Output: /Users/you/Desktop/lecture.docx
──────────────────────────────────────────────────
```

### Interface 2 — A Full Web UI

Say *"open the OCR web app"* and Claude starts a Flask server in the background and opens your browser automatically. You get a drag-and-drop interface, an animated page-by-page progress bar, and a download button — no terminal knowledge required.

```
> open the OCR web app
```

The skill's launcher script checks if the server is already running on port 5001, starts it if not, waits for it to be ready, then calls `webbrowser.open()`. The whole thing happens in a few seconds.

This dual-interface design was a deliberate choice. **Developers comfortable in the terminal get a frictionless CLI experience. Everyone else gets a point-and-click UI.** Neither group has to compromise — and both are triggered by a natural language prompt in the same Claude Code terminal.

---

## The Two Skills Systems — A Confession

Here's something I didn't plan: this repository ended up with **three separate implementations** of the same PDF logic.

1. **`python_tools/pdf.py`** — the original standalone functions I wrote first
2. **`python_framework_implementation/pdf/pdf_class.py`** — a `PDFSkill` Python class wrapping the same logic, importable from any Python script
3. **`claude-skills/pdf-skills/SKILL.md`** — the same logic written a third time as inline code snippets for Claude to read

I only noticed this when I started thinking about maintenance. If I find a bug in the repair logic, I need to fix it in three places. That's a real problem.

But it also surfaced something worth understanding clearly: **these three things serve completely different purposes.**

SKILL.md is Claude's knowledge. The Python class is reusable executable code. They happen to describe the same domain but live in completely different worlds — one is read by a language model at runtime, the other is imported by the Python interpreter.

What I didn't expect: the OCR web app **imports the PDFSkill class directly** for PDF pre-flight validation and auto-repair. So the Claude Skill and the Flask web app actually share real code underneath. The SKILL.md teaches Claude how to reason about PDFs. The Python class does the actual work at runtime. Both exist, both are useful, and now they're properly connected.

The lesson I'd apply going forward: write the core logic once in the Python class, have the SKILL.md reference and guide Claude toward using it, rather than duplicating the implementation as inline markdown snippets.

---

## What I'd Do Differently

**1. Design the architecture before writing the first line of code.**
I wrote `pdf.py` as a quick script, then wrapped it in a class, then documented it for Claude. That order created the duplication problem. Starting with the Python class as the single source of truth would have been cleaner from the start.

**2. The SKILL.md description field deserves more attention than it gets.**
This single field determines whether Claude loads your skill at all. A vague description means your skill sits unused. Be specific about trigger phrases — the more concrete, the more reliably it activates.

**3. Plan the dual-interface pattern from day one.**
Knowing I'd want both a CLI and a web UI, I would have designed the core modules as a clean library first, rather than building the CLI mode and then retrofitting Flask on top. The architecture worked out, but it would have been cleaner with upfront planning.

---

## The Stack

- **Claude Code Skills** (SKILL.md format — Anthropic)
- **Python** · **Flask** (web UI)
- **PyMuPDF** (PDF to PNG rendering — no system binary dependencies)
- **Anthropic SDK** (Claude Vision API for handwriting extraction)
- **python-docx** (Word document assembly with page breaks)
- **PyPDF2** · **pikepdf** (PDF manipulation and auto-repair)

---

## Try It Yourself

Everything is on GitHub: **https://github.com/learngvrk/claude-code-skills**

```bash
# Clone
git clone https://github.com/learngvrk/claude-code-skills.git
cd claude-code-skills

# Install the PDF skill
cp -r claude-skills/pdf-skills ~/.claude/skills/
pip install PyPDF2 pikepdf

# Install the OCR skill + web app
cp -r claude-skills/handwritten-ocr ~/.claude/skills/
cd claude-skills/handwritten-ocr
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-YOUR_KEY" > .env
```

Then open Claude Code and try:

```
> merge these PDFs into one
> extract pages 5 to 10 from this document
> convert my handwritten notes to Word
> open the OCR web app
```

---

## Closing Thought

The best thing about building a skill isn't the first time it saves you five minutes. It's the tenth time — when you've completely forgotten how the underlying code works, and you don't need to remember.

You just ask.

---

*If you found this useful, the GitHub repo is at https://github.com/learngvrk/claude-code-skills — feel free to fork it, extend it, or build your own skills on top of it.*
