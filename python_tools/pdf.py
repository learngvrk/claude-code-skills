import PyPDF2
import subprocess
import shutil
from PyPDF2.errors import PdfReadError


def repair_with_pikepdf(input_path, repaired_path):
    """Try to repair a PDF using pikepdf (requires qpdf installed).

    Returns True on success, False otherwise.
    """
    try:
        import pikepdf
    except Exception:
        return False

    try:
        with pikepdf.open(input_path) as pdf:
            pdf.save(repaired_path)
        return True
    except Exception:
        return False


def repair_with_ghostscript(input_path, repaired_path):
    """Attempt to repair using Ghostscript (gs). Returns True on success."""
    gs = shutil.which('gs')
    if not gs:
        return False

    try:
        subprocess.run([
            gs,
            '-o', repaired_path,
            '-sDEVICE=pdfwrite',
            '-dPDFSETTINGS=/prepress',
            input_path
        ], check=True)
        return True
    except Exception:
        return False


def _open_pdf_reader(path):
    """Try opening a PDF with PyPDF2. Return PdfReader or raise."""
    with open(path, 'rb') as f:
        return PyPDF2.PdfReader(f)


def extract_pages(input_path, output_path, start_page, end_page):
    """Extract pages from a PDF to a new PDF with simple repair-and-retry logic.

    If reading fails, attempt repair with pikepdf, then Ghostscript, and retry.
    """
    # First try to read normally (allow PyPDF2 to be strict=False by reopening with file)
    try:
        pdf_reader = PyPDF2.PdfReader(open(input_path, 'rb'))
    except (OSError, PdfReadError, ValueError) as e:
        # Attempt repairs
        repaired = input_path.rstrip('.pdf') + '_repaired.pdf'
        repaired_done = False

        if repair_with_pikepdf(input_path, repaired):
            repaired_done = True
        else:
            if repair_with_ghostscript(input_path, repaired):
                repaired_done = True

        if not repaired_done:
            raise RuntimeError(f"Failed to read PDF and repair attempts failed: {e}")

        # Try reading the repaired file
        try:
            pdf_reader = PyPDF2.PdfReader(open(repaired, 'rb'))
        except Exception as e2:
            raise RuntimeError(f"Reading repaired PDF failed: {e2}")

    # Ensure the start_page and end_page are within the valid range
    start_page = max(0, min(start_page, len(pdf_reader.pages) - 1))
    end_page = min(end_page, len(pdf_reader.pages) - 1)

    # Create a new PDF writer and add the selected pages
    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(start_page, end_page + 1):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    # Write the new PDF to the output file
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)


def merge_pdfs(input_paths, output_path):
    pdf_writer = PyPDF2.PdfWriter()

    for path in input_paths:
        pdf_reader = PyPDF2.PdfReader(path)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)


# Example usage
# input_files = ['Document_2024-02-13_224105.pdf', 'Srinika_Artwork_file.pdf']  # List of PDF files to merge
# output_file = 'Srinika_Artwork_final.pdf'  # Output file name

# merge_pdfs(input_files, output_file)

base_location = '/Users/username/Documents/Contracts'
input_file = 'Contract_Bundle_2025.pdf'
output_file = 'Signed_Agreement.pdf'
# Example usage
input_file_path = base_location+'/'+ input_file
output_file_path = base_location+'/'+ output_file
start_page_number = 6
end_page_number = 7

file_1 = 'IMG_0002.pdf'
file_2 = 'IMG_0003.pdf'
input_file_path_1 = base_location+'/'+ file_1
input_file_path_2 = base_location+'/'+ file_2
extract_pages(input_file_path, output_file_path, start_page_number, end_page_number)
# input_paths = [input_file_path_1, input_file_path_2]  # List of PDF files to merge
# merge_pdfs(input_paths, output_file_path)

