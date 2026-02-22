"""
PDF Skill - Core implementation for PDF manipulation operations.
"""

import PyPDF2
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional, Tuple
from PyPDF2.errors import PdfReadError


class PDFSkill:
    """
    A skill for manipulating PDF files.

    Capabilities:
    - Merge multiple PDFs into one
    - Extract specific page ranges
    - Repair corrupted PDFs using pikepdf or Ghostscript
    """

    def __init__(self):
        """Initialize the PDF skill."""
        self.name = "PDF Manipulation Skill"
        self.version = "1.0.0"

    def repair_with_pikepdf(self, input_path: str, repaired_path: str) -> bool:
        """
        Try to repair a PDF using pikepdf (requires qpdf installed).

        Args:
            input_path: Path to the corrupted PDF
            repaired_path: Path where repaired PDF should be saved

        Returns:
            True on success, False otherwise
        """
        try:
            import pikepdf
        except ImportError:
            return False

        try:
            with pikepdf.open(input_path) as pdf:
                pdf.save(repaired_path)
            return True
        except Exception:
            return False

    def repair_with_ghostscript(self, input_path: str, repaired_path: str) -> bool:
        """
        Attempt to repair using Ghostscript (gs).

        Args:
            input_path: Path to the corrupted PDF
            repaired_path: Path where repaired PDF should be saved

        Returns:
            True on success, False otherwise
        """
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
            ], check=True, capture_output=True)
            return True
        except Exception:
            return False

    def _open_pdf_with_repair(self, path: str) -> Tuple[PyPDF2.PdfReader, Optional[str]]:
        """
        Try opening a PDF with PyPDF2, attempting repair if needed.

        Args:
            path: Path to the PDF file

        Returns:
            Tuple of (PdfReader object, path to repaired file if repair was needed)

        Raises:
            RuntimeError: If PDF cannot be opened or repaired
        """
        # First try to read normally
        try:
            pdf_reader = PyPDF2.PdfReader(open(path, 'rb'))
            return pdf_reader, None
        except (OSError, PdfReadError, ValueError) as e:
            # Attempt repairs
            repaired = str(Path(path).with_suffix('')) + '_repaired.pdf'
            repaired_done = False

            if self.repair_with_pikepdf(path, repaired):
                repaired_done = True
            elif self.repair_with_ghostscript(path, repaired):
                repaired_done = True

            if not repaired_done:
                raise RuntimeError(f"Failed to read PDF and repair attempts failed: {e}")

            # Try reading the repaired file
            try:
                pdf_reader = PyPDF2.PdfReader(open(repaired, 'rb'))
                return pdf_reader, repaired
            except Exception as e2:
                raise RuntimeError(f"Reading repaired PDF failed: {e2}")

    def extract_pages(
        self,
        input_path: str,
        output_path: str,
        start_page: int,
        end_page: int
    ) -> dict:
        """
        Extract pages from a PDF to a new PDF with automatic repair if needed.

        Args:
            input_path: Path to the source PDF
            output_path: Path for the output PDF
            start_page: Starting page number (0-indexed)
            end_page: Ending page number (0-indexed, inclusive)

        Returns:
            Dictionary with operation status and metadata

        Raises:
            RuntimeError: If PDF cannot be read or repaired
        """
        pdf_reader, repaired_path = self._open_pdf_with_repair(input_path)

        total_pages = len(pdf_reader.pages)

        # Ensure the start_page and end_page are within the valid range
        start_page = max(0, min(start_page, total_pages - 1))
        end_page = min(end_page, total_pages - 1)

        # Create a new PDF writer and add the selected pages
        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(start_page, end_page + 1):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        # Write the new PDF to the output file
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        return {
            'status': 'success',
            'input_file': input_path,
            'output_file': output_path,
            'total_pages_in_source': total_pages,
            'pages_extracted': end_page - start_page + 1,
            'page_range': f"{start_page}-{end_page}",
            'repair_needed': repaired_path is not None,
            'repaired_file': repaired_path
        }

    def merge_pdfs(
        self,
        input_paths: List[str],
        output_path: str,
        auto_repair: bool = True
    ) -> dict:
        """
        Merge multiple PDF files into a single PDF.

        Args:
            input_paths: List of paths to PDF files to merge
            output_path: Path for the merged output PDF
            auto_repair: Whether to attempt repair on corrupted PDFs

        Returns:
            Dictionary with operation status and metadata

        Raises:
            ValueError: If input_paths is empty
            RuntimeError: If any PDF cannot be read
        """
        if not input_paths:
            raise ValueError("No input files provided")

        pdf_writer = PyPDF2.PdfWriter()
        files_info = []

        for path in input_paths:
            if auto_repair:
                pdf_reader, repaired_path = self._open_pdf_with_repair(path)
            else:
                pdf_reader = PyPDF2.PdfReader(path)
                repaired_path = None

            page_count = len(pdf_reader.pages)

            for page_num in range(page_count):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

            files_info.append({
                'file': path,
                'pages': page_count,
                'repaired': repaired_path is not None
            })

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        total_pages = sum(info['pages'] for info in files_info)

        return {
            'status': 'success',
            'output_file': output_path,
            'files_merged': len(input_paths),
            'total_pages': total_pages,
            'files_info': files_info
        }

    def get_info(self, pdf_path: str) -> dict:
        """
        Get information about a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary with PDF metadata and information
        """
        pdf_reader, repaired_path = self._open_pdf_with_repair(pdf_path)

        metadata = pdf_reader.metadata
        info = {
            'file': pdf_path,
            'total_pages': len(pdf_reader.pages),
            'repair_needed': repaired_path is not None,
            'metadata': {}
        }

        if metadata:
            info['metadata'] = {
                'title': metadata.get('/Title', 'N/A'),
                'author': metadata.get('/Author', 'N/A'),
                'subject': metadata.get('/Subject', 'N/A'),
                'creator': metadata.get('/Creator', 'N/A'),
                'producer': metadata.get('/Producer', 'N/A'),
            }

        return info

    def __repr__(self):
        return f"<PDFSkill version={self.version}>"
