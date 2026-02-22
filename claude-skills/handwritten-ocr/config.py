import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file
load_dotenv(Path(__file__).parent / ".env")

BASE_DIR = Path(__file__).parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-6"

MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50 MB

PDF_RENDER_DPI = 150

CLAUDE_PROMPT = (
    "This is a scanned image of a handwritten page. "
    "Please transcribe ALL handwritten text exactly as written, preserving line breaks. "
    "Do not add any commentary, formatting, or interpretation. "
    "Output only the transcribed text."
)
