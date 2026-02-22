# Anthropic Skills Repository

This repository contains **Anthropic Skills** for Claude - specialized expertise packages that give Claude enhanced capabilities for specific tasks.

## What Are Anthropic Skills?

**Anthropic Skills** are folders containing instructions and code that Claude can automatically use when relevant. When you install skills:

1. Claude scans their names and descriptions at startup
2. When you ask Claude for help, it loads relevant skills automatically
3. Claude follows the skill's instructions to help you complete tasks

**Key Benefits:**
- 🎯 **Automatic**: Claude loads skills when needed
- 📦 **Portable**: Copy skills between projects
- ⚡ **Efficient**: Only relevant skills are loaded
- 🔧 **Powerful**: Include executable code for complex tasks

## Available Skills

### 📄 PDF Manipulation

Expert PDF manipulation including merging, page extraction, and automatic repair.

**Location**: [pdf-manipulation/](pdf-manipulation/)

**Capabilities**:
- Merge multiple PDFs into one document
- Extract specific page ranges
- Repair corrupted PDF files automatically
- Get PDF metadata and information

**Quick Start**:
```bash
# Install dependencies
pip install PyPDF2 pikepdf

# Copy to Claude's skills directory
cp -r pdf-manipulation ~/.claude/skills/
```

**Usage with Claude**:
> "Extract pages 7-8 from the H1B approval packet and save as I797.pdf"

> "Merge these three scanned PDFs into one document"

> "This PDF is corrupted, can you repair it?"

**See**: [pdf-manipulation/README.md](pdf-manipulation/README.md) for detailed instructions

---

## Repository Structure

```
claude-skills/
├── README.md                       # This file
├── HOW_TO_CREATE_SKILLS.md        # Complete guide to creating skills
│
└── pdf-manipulation/               # PDF manipulation skill
    ├── SKILL.md                   # Skill instructions (REQUIRED)
    ├── README.md                  # Installation and usage guide
    ├── scripts/
    │   └── pdf_operations.py      # Implementation with CLI
    └── examples/
        └── usage_examples.md      # 10 detailed examples
```

## Getting Started

### For Users (Use existing skills)

1. **Choose a skill** from the list above
2. **Install dependencies** (see skill's README)
3. **Copy to Claude**:
   ```bash
   cp -r skill-name ~/.claude/skills/
   ```
4. **Restart Claude** (if using Claude Desktop)
5. **Use naturally**: Just ask Claude for what you need!

### For Developers (Create new skills)

1. **Read the guide**: [HOW_TO_CREATE_SKILLS.md](HOW_TO_CREATE_SKILLS.md)
2. **Study an example**: Check out [pdf-manipulation/](pdf-manipulation/)
3. **Create your skill**:
   ```bash
   mkdir -p claude-skills/my-skill
   # Create SKILL.md with frontmatter
   # Add implementation scripts
   # Add examples
   ```
4. **Test with Claude**
5. **Share** (optional)

## Creating New Skills

### Quick Template

```bash
# Create directory
mkdir -p my-skill/scripts my-skill/examples

# Create SKILL.md
cat > my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What this skill does and when to use it
---

# My Skill Name

[Instructions for Claude]

## Core Capabilities
[What it can do]

## Usage Examples
[How to use it]
EOF

# Add your implementation
# Add examples
# Test with Claude
```

See [HOW_TO_CREATE_SKILLS.md](HOW_TO_CREATE_SKILLS.md) for complete guide.

## Skill Requirements

### Minimal Skill (Just SKILL.md)

```
skill-name/
└── SKILL.md  # ONLY required file
```

### Complete Skill (Recommended)

```
skill-name/
├── SKILL.md              # Instructions for Claude (REQUIRED)
├── README.md             # How to install and use
├── scripts/              # Implementation code
│   └── implementation.py
└── examples/             # Usage examples
    └── examples.md
```

## How Skills Work

### 1. Progressive Disclosure

```
Startup → Claude loads skill names + descriptions
          ↓
User request → Claude identifies relevant skill
          ↓
Load skill → Claude reads full SKILL.md
          ↓
Execute → Claude follows instructions
```

### 2. Example Flow

**You say**: "Extract pages 7-8 from document.pdf"

**Claude thinks**:
1. "This involves PDF manipulation"
2. "I have a pdf-manipulation skill"
3. *Loads SKILL.md*
4. "I should use the extract_pages function"
5. *Executes and reports results*

## Installation

### Claude Desktop

```bash
# Copy all skills
cp -r claude-skills/* ~/.claude/skills/

# Or copy specific skill
cp -r claude-skills/pdf-manipulation ~/.claude/skills/

# Restart Claude Desktop
```

### Claude API

```python
import anthropic

client = anthropic.Anthropic()

# Use skills in API calls
# See: https://docs.anthropic.com/en/docs/build-with-claude/skills
```

### Claude Code

Claude Code automatically scans for skills in your project.

## Dependencies

Each skill lists its own dependencies. For the PDF skill:

```bash
pip install PyPDF2>=3.0.0
pip install pikepdf>=8.0.0  # Optional, for repair
brew install qpdf ghostscript  # System tools for repair
```

## Examples

### PDF Skill Examples

**Extract pages**:
> "Extract pages 7-8 from /Users/username/Documents/H1B_Packet.pdf and save as I797.pdf"

**Merge PDFs**:
> "Merge file1.pdf, file2.pdf, and file3.pdf into combined.pdf"

**Repair corrupted PDF**:
> "This PDF is corrupted: broken.pdf. Please repair it."

**Batch processing**:
> "Extract the first page from all PDFs in this directory"

See [pdf-manipulation/examples/usage_examples.md](pdf-manipulation/examples/usage_examples.md) for 10 detailed examples.

## Best Practices

### When Creating Skills

1. ✅ **Single responsibility**: One skill, one purpose
2. ✅ **Clear descriptions**: Help Claude know when to use it
3. ✅ **Include examples**: Show concrete usage
4. ✅ **Handle errors**: Include fallback strategies
5. ✅ **Document dependencies**: List all requirements

### When Using Skills

1. ✅ **Be specific**: Provide exact file paths and parameters
2. ✅ **Check output**: Verify results before using
3. ✅ **Report issues**: If a skill doesn't work as expected
4. ✅ **Combine skills**: Use multiple skills together for complex workflows

## Skills vs MCP vs Regular Code

### Regular Code
- You run manually
- No AI integration
- One-off scripts

### Anthropic Skills (This!)
- Claude uses automatically
- Simple structure (SKILL.md + scripts)
- Task-specific expertise

### MCP (Model Context Protocol)
- Complex client-server architecture
- For external service integration
- Requires server implementation

**Use Skills when**: You want Claude to help with specific tasks
**Use MCP when**: You need to expose external APIs or services

## Troubleshooting

### Skill not loading

1. Check SKILL.md has valid YAML frontmatter
2. Ensure skill directory name matches `name:` in frontmatter
3. Restart Claude Desktop
4. Check Claude's console for errors

### Dependencies not found

```bash
# Check Python packages
pip list | grep -i pypdf

# Check system tools
which qpdf gs

# Install if missing
pip install PyPDF2 pikepdf
brew install qpdf ghostscript
```

### Skill not activating

Make the description more specific about when to use it:

❌ "PDF skill"
✅ "Expert PDF manipulation for merging, extracting pages, and repairing"

## Contributing

To add skills to this repository:

1. Create your skill following [HOW_TO_CREATE_SKILLS.md](HOW_TO_CREATE_SKILLS.md)
2. Test thoroughly with Claude
3. Document clearly with examples
4. Submit a pull request

## Resources

### Official Documentation
- [Anthropic Skills Blog Post](https://www.anthropic.com/news/skills)
- [Official Skills Repository](https://github.com/anthropics/skills)
- [Claude Cookbooks](https://github.com/anthropics/claude-cookbooks)

### This Repository
- [How to Create Skills Guide](HOW_TO_CREATE_SKILLS.md)
- [PDF Manipulation Skill](pdf-manipulation/)
- [PDF Usage Examples](pdf-manipulation/examples/usage_examples.md)

## FAQ

**Q: What's the difference between a skill and an MCP server?**
A: Skills are simpler - just instructions in SKILL.md. MCP is a full protocol for exposing external services.

**Q: Can I use multiple skills together?**
A: Yes! Claude can load and use multiple relevant skills for complex tasks.

**Q: Do I need to write code in skills?**
A: No, you only need SKILL.md. But including scripts makes skills more powerful.

**Q: How does Claude know when to use a skill?**
A: From the skill's description. Be specific about what it does and when to use it.

**Q: Can I modify existing skills?**
A: Yes! Skills are just folders. Edit SKILL.md or add to the scripts.

**Q: How do I share my skills?**
A: Copy the skill folder, or contribute to github.com/anthropics/skills

## License

This repository and its skills are provided as-is for use with Claude. Modify as needed for your use case.

## Version

**Repository Version**: 1.0.0
**Skills Format**: Anthropic Skills v1
**Last Updated**: 2025

---

## Quick Links

- 📘 [Creating Skills Guide](HOW_TO_CREATE_SKILLS.md)
- 📄 [PDF Manipulation Skill](pdf-manipulation/)
- 📝 [PDF Examples](pdf-manipulation/examples/usage_examples.md)
- 🌐 [Official Skills Repo](https://github.com/anthropics/skills)

---

**Ready to start?**

1. Try the PDF skill: `cp -r pdf-manipulation ~/.claude/skills/`
2. Create your own: Read [HOW_TO_CREATE_SKILLS.md](HOW_TO_CREATE_SKILLS.md)
3. Share your skills with others!

🚀 **Happy skill building!**
