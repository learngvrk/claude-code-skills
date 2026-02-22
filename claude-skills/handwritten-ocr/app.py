"""
Flask web application for handwritten PDF to Word conversion.

Routes:
    GET  /                        Upload form
    POST /upload                  Accept PDF, start background job → { job_id }
    GET  /status/<job_id>         Poll job status → { status, progress, total, ... }
    GET  /download/<filename>     Download generated .docx file
"""

import uuid
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_from_directory

import config
from core.processor import get_job_status, start_processing_in_background

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = config.MAX_UPLOAD_BYTES


# ── Route: Upload Form ─────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ── Route: Upload and Process ──────────────────────────────────────────────────

@app.route("/upload", methods=["POST"])
def upload():
    """
    Accept a PDF upload, validate, start background processing.

    Returns:
        202 { "job_id": "<uuid>" }  on success
        400 { "error": "<msg>" }    on validation failure
        500 { "error": "<msg>" }    on server misconfiguration
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    suffix = Path(file.filename).suffix.lower()
    if suffix != ".pdf":
        return jsonify({"error": "Only PDF files are accepted"}), 400

    if not config.ANTHROPIC_API_KEY or config.ANTHROPIC_API_KEY.startswith("sk-ant-YOUR"):
        return jsonify({"error": "ANTHROPIC_API_KEY is not configured on the server"}), 500

    upload_id = str(uuid.uuid4())
    pdf_path = str(config.UPLOAD_DIR / f"{upload_id}.pdf")
    file.save(pdf_path)

    original_stem = Path(file.filename).stem
    output_filename = f"{upload_id}_{original_stem}.docx"

    job_id = start_processing_in_background(
        pdf_path=pdf_path,
        output_filename=output_filename,
        original_filename=file.filename,
    )

    return jsonify({"job_id": job_id}), 202


# ── Route: Job Status ──────────────────────────────────────────────────────────

@app.route("/status/<job_id>", methods=["GET"])
def status(job_id: str):
    """
    Return current processing status for a job.

    Returns JSON with keys: status, progress, total, output_filename, error
    """
    job = get_job_status(job_id)
    if job is None:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job), 200


# ── Route: Download ────────────────────────────────────────────────────────────

@app.route("/download/<filename>", methods=["GET"])
def download(filename: str):
    """
    Serve a generated .docx file. Only serves from outputs/ directory.
    """
    # Reject path traversal attempts
    if "/" in filename or "\\" in filename or ".." in filename:
        abort(400)
    if not filename.endswith(".docx"):
        abort(400)

    return send_from_directory(
        config.OUTPUT_DIR,
        filename,
        as_attachment=True,
        download_name=filename,
    )


# ── Error Handlers ─────────────────────────────────────────────────────────────

@app.errorhandler(413)
def request_entity_too_large(e):
    limit_mb = config.MAX_UPLOAD_BYTES // (1024 * 1024)
    return jsonify({"error": f"File too large. Maximum allowed size is {limit_mb} MB"}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
