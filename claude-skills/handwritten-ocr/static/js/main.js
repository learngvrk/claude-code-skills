'use strict';

// ── Element references ─────────────────────────────────────────────────────────
const uploadForm     = document.getElementById('upload-form');
const fileInput      = document.getElementById('file-input');
const chooseBtn      = document.getElementById('choose-btn');
const submitBtn      = document.getElementById('submit-btn');
const dropZone       = document.getElementById('drop-zone');
const fileInfo       = document.getElementById('file-info');
const uploadError    = document.getElementById('upload-error');

const uploadSection   = document.getElementById('upload-section');
const progressSection = document.getElementById('progress-section');
const downloadSection = document.getElementById('download-section');
const errorSection    = document.getElementById('error-section');

const statusLabel     = document.getElementById('status-label');
const progressBar     = document.getElementById('progress-bar');
const progressText    = document.getElementById('progress-text');
const downloadLink    = document.getElementById('download-link');
const processingError = document.getElementById('processing-error');

let pollingTimer = null;

// ── File selection ─────────────────────────────────────────────────────────────

chooseBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        applyFile(fileInput.files[0]);
    }
});

// Drag and drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showUploadError('Please drop a PDF file.');
            return;
        }
        // Assign dropped file to the input element
        const dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;
        applyFile(file);
    }
});

// Clicking the drop zone opens the file picker
dropZone.addEventListener('click', (e) => {
    // Avoid double-trigger when the choose button itself is clicked
    if (e.target !== chooseBtn) {
        fileInput.click();
    }
});

function applyFile(file) {
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    fileInfo.textContent = `Selected: ${file.name} (${sizeMB} MB)`;
    fileInfo.classList.remove('hidden');
    uploadError.classList.add('hidden');
    submitBtn.disabled = false;
}

// ── Form submission ────────────────────────────────────────────────────────────

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!fileInput.files.length) return;

    submitBtn.disabled = true;
    uploadError.classList.add('hidden');
    showSection('progress');
    updateProgress('Uploading PDF...', 0, 0);

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `Upload failed (HTTP ${response.status})`);
        }

        startPolling(data.job_id);

    } catch (err) {
        showSection('upload');
        showUploadError(err.message);
        submitBtn.disabled = false;
    }
});

// ── Status polling ─────────────────────────────────────────────────────────────

const STATUS_LABELS = {
    queued:           'Queued, waiting to start...',
    rendering_pages:  'Rendering PDF pages to images...',
    running_ocr:      'Extracting handwritten text with Claude AI...',
    building_docx:    'Building Word document...',
    complete:         'Conversion complete!',
    error:            'An error occurred.',
};

function startPolling(jobId) {
    if (pollingTimer) clearInterval(pollingTimer);

    pollingTimer = setInterval(async () => {
        try {
            const response = await fetch(`/status/${encodeURIComponent(jobId)}`);
            const job = await response.json();

            if (!response.ok) {
                clearInterval(pollingTimer);
                showSection('error');
                processingError.textContent = job.error || 'Unknown error.';
                return;
            }

            const label = STATUS_LABELS[job.status] || job.status;
            updateProgress(label, job.progress, job.total);

            if (job.status === 'complete') {
                clearInterval(pollingTimer);
                downloadLink.href = `/download/${encodeURIComponent(job.output_filename)}`;
                downloadLink.setAttribute('download', job.output_filename);
                showSection('download');

            } else if (job.status === 'error') {
                clearInterval(pollingTimer);
                showSection('error');
                processingError.textContent = job.error || 'Processing failed. Please try again.';
            }

        } catch (networkErr) {
            // Network blip — keep polling, do not abort
            console.warn('Polling request failed:', networkErr);
        }
    }, 2000);
}

// ── UI helpers ─────────────────────────────────────────────────────────────────

function updateProgress(label, progress, total) {
    statusLabel.textContent = label;
    const pct = total > 0 ? Math.min(100, Math.round((progress / total) * 100)) : 0;
    progressBar.style.width = `${pct}%`;
    progressText.textContent = total > 0
        ? `${progress} of ${total} pages processed`
        : 'Preparing...';
}

function showSection(name) {
    uploadSection.classList.add('hidden');
    progressSection.classList.add('hidden');
    downloadSection.classList.add('hidden');
    errorSection.classList.add('hidden');

    switch (name) {
        case 'upload':   uploadSection.classList.remove('hidden');   break;
        case 'progress': progressSection.classList.remove('hidden'); break;
        case 'download': downloadSection.classList.remove('hidden'); break;
        case 'error':    errorSection.classList.remove('hidden');    break;
    }
}

function showUploadError(msg) {
    uploadError.textContent = msg;
    uploadError.classList.remove('hidden');
}

// ── Convert Another / Retry ────────────────────────────────────────────────────

document.getElementById('convert-another-btn').addEventListener('click', resetForm);
document.getElementById('retry-btn').addEventListener('click', resetForm);

function resetForm() {
    if (pollingTimer) {
        clearInterval(pollingTimer);
        pollingTimer = null;
    }
    fileInput.value = '';
    fileInfo.textContent = '';
    fileInfo.classList.add('hidden');
    uploadError.classList.add('hidden');
    submitBtn.disabled = true;
    progressBar.style.width = '0%';
    showSection('upload');
}
