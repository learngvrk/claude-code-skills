# How to Create Anthropic Skills - Complete Guide

This guide shows you exactly how to convert your code into Anthropic Skills that work with Claude.

## What is an Anthropic Skill?

An **Anthropic Skill** is a folder containing:
1. A `SKILL.md` file with instructions for Claude
2. (Optional) Scripts and supporting files

When you install skills, Claude automatically:
- Scans their names and descriptions
- Loads the relevant skill when you need it
- Follows the skill's instructions to help you

## Skills vs Regular Python Code

### Before (Regular Code)

```
tools/pdf.py - Your functions
├── You run the script manually
├── You remember how to use each function
└── Code is scattered and hard to reuse
```

### After (Anthropic Skill)

```
pdf-manipulation/ - Your skill
├── SKILL.md - Instructions for Claude
├── scripts/pdf_operations.py - Implementation
└── Claude uses it automatically when you need PDF help
```

---

## Step-by-Step: Creating a Skill

Let's convert your PDF code into a skill (which we already did!)

### Step 1: Create the Directory Structure

```bash
mkdir -p claude-skills/pdf-manipulation/scripts
mkdir -p claude-skills/pdf-manipulation/examples
```

**Directory naming:**
- Use lowercase
- Use hyphens (not underscores or spaces)
- Be descriptive: `pdf-manipulation` not just `pdf`

### Step 2: Create SKILL.md

This is the **ONLY required file**. It must have:

1. **YAML frontmatter** (metadata)
2. **Instructions** (what Claude should do)
3. **Examples** (how to use it)

**Template:**

```markdown
---
name: skill-name
description: Clear description of what this skill does and when Claude should use it
---

# Skill Name

[Instructions for Claude explaining how to accomplish tasks]

## Core Capabilities

### Capability 1
[Detailed explanation]

### Capability 2
[Detailed explanation]

## Usage Examples

### Example 1: [Scenario]
[Concrete example with code]

## Guidelines

- Guideline 1
- Guideline 2
```

**For your PDF skill:**

```markdown
---
name: pdf-manipulation
description: Expert PDF manipulation for merging PDFs, extracting page ranges, and repairing corrupted files using PyPDF2
---

# PDF Manipulation Skill

You are an expert at manipulating PDF files...

[Full instructions about merge, extract, repair capabilities]
```

### Step 3: Add Your Implementation Code

Put your actual Python code in `scripts/`:

```bash
scripts/
└── pdf_operations.py  # Your original code, cleaned up
```

**Convert your functions to a well-structured script:**

```python
#!/usr/bin/env python3
"""
PDF Operations - Implementation
"""

import PyPDF2

def merge_pdfs(input_paths, output_path):
    """Your merge function"""
    pass

def extract_pages(input_path, output_path, start, end):
    """Your extract function"""
    pass

# Add command-line interface
if __name__ == '__main__':
    # CLI code here
    pass
```

### Step 4: Add Examples (Optional but Recommended)

```bash
examples/
└── usage_examples.md  # Detailed usage examples
```

### Step 5: Add README (Optional)

```bash
README.md  # How to install and use the skill
```

---

## Anatomy of SKILL.md

Let's break down each part:

### Part 1: YAML Frontmatter (Required)

```yaml
---
name: pdf-manipulation
description: Expert PDF manipulation skill for merging multiple PDFs, extracting specific page ranges, and repairing corrupted PDF files using PyPDF2, pikepdf, and Ghostscript
---
```

**Rules:**
- `name`: Must match directory name (lowercase, hyphens)
- `description`: Complete sentence explaining when to use this skill
- Keep description under 1024 characters
- Be specific about capabilities

**Good descriptions:**
- ✅ "Expert PDF manipulation for merging PDFs, extracting page ranges, and repairing corrupted files"
- ✅ "Excel data processing including reading sheets, writing data, and creating charts"

**Bad descriptions:**
- ❌ "PDF stuff" (too vague)
- ❌ "A skill" (no useful information)

### Part 2: Main Instructions

```markdown
# PDF Manipulation Skill

You are an expert at manipulating PDF files. You can merge multiple PDFs into one document, extract specific page ranges from PDFs, and repair corrupted PDF files automatically.
```

**This tells Claude:**
- What role to take on
- What capabilities it has
- What types of tasks to expect

### Part 3: Core Capabilities

```markdown
## Core Capabilities

### 1. Merging PDF Files
Combine multiple PDF documents into a single output file while preserving all pages and content.

**When to use:**
- Combining multiple scanned documents
- Merging report sections

**Implementation approach:**
[Show code example]
```

**For each capability:**
- Clear heading
- What it does
- When to use it
- How to implement it (code examples)

### Part 4: Usage Examples

```markdown
## Usage Examples

### Example 1: Extract I-797 Pages from H1B Packet
[Complete example with actual paths and expected output]
```

**Show:**
- Real-world scenarios
- Actual code that works
- Expected input/output
- Common use cases

### Part 5: Guidelines

```markdown
## Important Guidelines

### Page Numbering
- Always use 0-indexed pages in code
- Page 1 in viewer = index 0 in code

### Error Handling
1. Check if PDF can be opened
2. Try repair if opening fails
3. Validate page ranges
```

**Include:**
- Important rules
- Common pitfalls
- Best practices
- Edge cases to handle

---

## Complete File Structure

Here's what we created for your PDF skill:

```
claude-skills/
└── pdf-manipulation/                    # Skill directory
    ├── SKILL.md                        # REQUIRED: Instructions for Claude
    ├── README.md                       # Optional: Installation guide
    ├── scripts/                        # Optional: Implementation code
    │   └── pdf_operations.py          # Your actual code
    └── examples/                       # Optional: Usage examples
        └── usage_examples.md          # Detailed examples
```

---

## How Claude Uses Your Skill

### 1. Startup (Progressive Disclosure)

When Claude starts, it reads:
```yaml
name: pdf-manipulation
description: Expert PDF manipulation for merging PDFs...
```

This is stored in Claude's system prompt. Claude now knows:
- A PDF skill exists
- What it can do
- When to use it

### 2. User Request

You say: *"Extract pages 7-8 from this PDF"*

Claude thinks:
- "This involves PDF manipulation"
- "I have a pdf-manipulation skill"
- "Let me load that skill"

### 3. Skill Loading

Claude loads the full SKILL.md and reads:
- Core capabilities
- Implementation examples
- Guidelines
- Best practices

### 4. Execution

Claude follows the instructions to:
1. Understand your specific request
2. Choose the right capability (extract_pages)
3. Write or run the code
4. Report results

---

## Best Practices for Skills

### 1. Single Responsibility

❌ **Bad**: One skill that does PDFs, Excel, and images
✅ **Good**: Separate skills for each capability

### 2. Clear Instructions

❌ **Bad**: "Use PyPDF2 to do stuff"
✅ **Good**: Step-by-step with code examples

### 3. Include Examples

❌ **Bad**: Just function signatures
✅ **Good**: Complete real-world examples

### 4. Handle Errors

❌ **Bad**: Assume everything works
✅ **Good**: Include repair/fallback strategies

### 5. Document Edge Cases

❌ **Bad**: Only show happy path
✅ **Good**: Explain corner cases (empty PDFs, corrupted files, etc.)

### 6. Provide Context

❌ **Bad**: "Use index 6"
✅ **Good**: "Page 7 in viewer = index 6 in code (0-indexed)"

---

## Testing Your Skill

### 1. Manual Testing with Claude

1. Install the skill in Claude
2. Try various prompts
3. Check if Claude understands and executes correctly

**Test prompts:**
- Simple case: "Extract page 1 from test.pdf"
- Complex case: "Merge these 5 PDFs and extract pages 10-20 from the result"
- Edge case: "Extract pages from corrupted.pdf"

### 2. Script Testing

```bash
# Test the script directly
python scripts/pdf_operations.py extract test.pdf 0 5 -o output.pdf
python scripts/pdf_operations.py merge file1.pdf file2.pdf -o merged.pdf
```

### 3. Check Against Examples

Verify all examples in `examples/usage_examples.md` work correctly.

---

## Adding Your Skill to Claude

### Option 1: Claude Desktop (Local)

```bash
# Copy to Claude's skills directory
cp -r pdf-manipulation ~/.claude/skills/

# Restart Claude Desktop
```

### Option 2: Claude API

```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

# Upload skill via API
# (See Anthropic's Skills API documentation)
```

### Option 3: Claude Code

Claude Code automatically scans for skills in your project directory.

---

## Creating More Skills

Now that you understand the pattern, create more skills!

### Excel Skill Example

```markdown
---
name: excel-manipulation
description: Expert Excel manipulation for reading sheets, writing data, creating charts, and processing spreadsheets using openpyxl
---

# Excel Manipulation Skill

You are an expert at working with Excel files...

## Core Capabilities

### 1. Reading Excel Files
[Instructions for reading]

### 2. Writing Excel Files
[Instructions for writing]

### 3. Creating Charts
[Instructions for charts]
```

### Image Processing Skill Example

```markdown
---
name: image-processing
description: Expert image processing for resizing, cropping, converting formats, and applying filters using Pillow
---

# Image Processing Skill

You are an expert at processing images...
```

---

## Skill Design Patterns

### Pattern 1: The Converter

**Purpose**: Convert between formats

**Structure**:
- Input format validation
- Conversion logic
- Output format options
- Error handling

**Examples**: PDF→Word, Excel→CSV, Image→PNG

### Pattern 2: The Analyzer

**Purpose**: Extract information

**Structure**:
- Data loading
- Analysis logic
- Results formatting
- Visualization options

**Examples**: PDF metadata, Excel statistics, Image properties

### Pattern 3: The Generator

**Purpose**: Create new content

**Structure**:
- Input parameters
- Generation logic
- Output customization
- Templates

**Examples**: Report generation, Chart creation, Image composites

### Pattern 4: The Transformer

**Purpose**: Modify existing content

**Structure**:
- Input validation
- Transformation operations
- Output options
- Batch processing

**Examples**: PDF page extraction, Excel column operations, Image filters

---

## Common Mistakes to Avoid

### 1. Too Generic

❌ **Wrong**: "A skill that helps with files"
✅ **Right**: "PDF manipulation: merge, extract pages, and repair"

### 2. Missing Examples

❌ **Wrong**: Only function signatures
✅ **Right**: Complete working examples

### 3. No Error Handling

❌ **Wrong**: Assume files always work
✅ **Right**: Include repair and fallback strategies

### 4. Unclear Instructions

❌ **Wrong**: "Use the library to process files"
✅ **Right**: "Use PyPDF2.PdfReader() to open files, then..."

### 5. Forgetting Dependencies

❌ **Wrong**: No mention of required packages
✅ **Right**: "Requires: pip install PyPDF2 pikepdf"

---

## Skill Repository Structure

For multiple skills:

```
claude-skills/
├── HOW_TO_CREATE_SKILLS.md       # This guide
├── pdf-manipulation/              # Skill 1
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/
│   └── examples/
├── excel-processing/              # Skill 2
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/
│   └── examples/
└── image-manipulation/            # Skill 3
    ├── SKILL.md
    ├── README.md
    ├── scripts/
    └── examples/
```

---

## Key Differences: Skills vs MCP vs Regular Code

### Regular Python Code
- You run it manually
- No AI assistance
- Functions scattered across files

### Anthropic Skills (What we created!)
- Claude uses automatically
- Simple: just SKILL.md + scripts
- Perfect for task-specific expertise

### MCP (Model Context Protocol)
- Complex client-server architecture
- For exposing external services
- Requires server implementation

**When to use Skills:**
- Task-specific expertise (PDF manipulation, Excel processing)
- Self-contained functionality
- Quick to create and deploy

**When to use MCP:**
- Need to expose external APIs
- Complex integrations
- Real-time data sources

---

## Next Steps

1. **Use the PDF skill** we created with Claude
2. **Create your own skill** for another task you do often
3. **Share your skills** with others or contribute to anthropics/skills
4. **Combine skills** for powerful workflows

---

## Resources

- **Official Skills Repo**: https://github.com/anthropics/skills
- **Skills Documentation**: https://www.anthropic.com/news/skills
- **Claude Cookbooks**: https://github.com/anthropics/claude-cookbooks
- **Your PDF Skill**: `/Users/ranjithgonugunta/Documents/Python/claude-skills/pdf-manipulation/`

---

## Summary

**Creating a skill:**
1. ✅ Create directory with hyphenated name
2. ✅ Write SKILL.md with YAML frontmatter + instructions
3. ✅ Add implementation scripts (optional)
4. ✅ Add examples and documentation (optional)
5. ✅ Install in Claude and test

**Your PDF skill has:**
- ✅ SKILL.md with complete instructions
- ✅ Implementation script with CLI
- ✅ Detailed examples
- ✅ README for installation
- ✅ Error handling and repair capabilities

**You now know how to:**
- ✅ Convert code to Anthropic Skills
- ✅ Structure SKILL.md properly
- ✅ Add supporting files
- ✅ Test and install skills
- ✅ Create more skills for other tasks

Enjoy creating skills! 🚀
