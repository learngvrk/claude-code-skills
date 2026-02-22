"""
Orchestration layer for the handwritten PDF to Word conversion pipeline.

Manages per-job state using an in-memory dict protected by a threading.Lock.
Each conversion runs in a background daemon thread so Flask stays responsive.

Job lifecycle:
    queued → rendering_pages → running_ocr → building_docx → complete | error
"""

import threading
import uuid
from pathlib import Path
from typing import Dict, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from core.pdf_to_images import pdf_to_png_bytes_list
from core.claude_ocr import extract_text_from_all_pages
from core.docx_builder import build_docx


# In-memory job store (sufficient for local single-user deployment)
_jobs: Dict[str, dict] = {}
_jobs_lock = threading.Lock()


def create_job() -> str:
    """Create a new job entry and return its UUID."""
    job_id = str(uuid.uuid4())
    with _jobs_lock:
        _jobs[job_id] = {
            "status": "queued",
            "progress": 0,
            "total": 0,
            "output_filename": None,
            "error": None,
        }
    return job_id


def get_job_status(job_id: str) -> Optional[dict]:
    """Return a copy of the job status dict, or None if not found."""
    with _jobs_lock:
        job = _jobs.get(job_id)
        return dict(job) if job else None


def _update_job(job_id: str, **kwargs) -> None:
    with _jobs_lock:
        if job_id in _jobs:
            _jobs[job_id].update(kwargs)


def _run_pipeline(
    job_id: str,
    pdf_path: str,
    output_filename: str,
    original_filename: str,
) -> None:
    """
    Full conversion pipeline. Runs in a background thread.

    Steps:
        1. Render PDF pages to PNG bytes (PyMuPDF)
        2. Extract text from each page via Claude Vision (sequential)
        3. Assemble .docx with page breaks
        4. Delete the uploaded temp PDF
    """
    try:
        _update_job(job_id, status="rendering_pages")

        pages_png = pdf_to_png_bytes_list(pdf_path, dpi=config.PDF_RENDER_DPI)
        total_pages = len(pages_png)
        _update_job(job_id, total=total_pages, status="running_ocr")

        def on_page_done(page_idx: int, total: int) -> None:
            _update_job(job_id, progress=page_idx)

        page_texts = extract_text_from_all_pages(
            png_bytes_list=pages_png,
            api_key=config.ANTHROPIC_API_KEY,
            model=config.CLAUDE_MODEL,
            prompt=config.CLAUDE_PROMPT,
            progress_callback=on_page_done,
        )

        _update_job(job_id, progress=total_pages, status="building_docx")

        output_path = str(config.OUTPUT_DIR / output_filename)
        build_docx(
            page_texts=page_texts,
            output_path=output_path,
            source_filename=original_filename,
        )

        _update_job(job_id, status="complete", output_filename=output_filename)

    except Exception as exc:
        _update_job(job_id, status="error", error=str(exc))

    finally:
        # Clean up uploaded PDF regardless of success/failure
        try:
            Path(pdf_path).unlink(missing_ok=True)
        except Exception:
            pass


def start_processing_in_background(
    pdf_path: str,
    output_filename: str,
    original_filename: str,
) -> str:
    """
    Create a job, start the background conversion thread, and return the job_id.

    Args:
        pdf_path:          Absolute path to the saved upload PDF
        output_filename:   Target .docx filename (stored in outputs/)
        original_filename: User's original filename (for docx metadata)

    Returns:
        job_id (str) — poll /status/<job_id> to track progress
    """
    job_id = create_job()
    thread = threading.Thread(
        target=_run_pipeline,
        args=(job_id, pdf_path, output_filename, original_filename),
        daemon=True,
    )
    thread.start()
    return job_id
