#!/usr/bin/env python3
"""
PDF Operations Script

Complete implementation of PDF manipulation operations including
merge, extract, and repair capabilities.

Usage:
    python pdf_operations.py merge file1.pdf file2.pdf -o output.pdf
    python pdf_operations.py extract input.pdf 0 5 -o output.pdf
    python pdf_operations.py repair corrupted.pdf -o repaired.pdf
"""

import PyPDF2
import subprocess
import shutil
import argparse
from pathlib import Path
from typing import List, Optional, Tuple
from PyPDF2.errors import PdfReadError


def repair_with_pikepdf(input_path: str, repaired_path: str) -> bool:
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
        print("⚠️  pikepdf not installed. Install with: pip install pikepdf")
        return False

    try:
        with pikepdf.open(input_path) as pdf:
            pdf.save(repaired_path)
        print(f"✓ Repaired with pikepdf: {repaired_path}")
        return True
    except Exception as e:
        print(f"✗ pikepdf repair failed: {e}")
        return False


def repair_with_ghostscript(input_path: str, repaired_path: str) -> bool:
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
        print("⚠️  Ghostscript not found. Install with: brew install ghostscript")
        return False

    try:
        result = subprocess.run([
            gs,
            '-o', repaired_path,
            '-sDEVICE=pdfwrite',
            '-dPDFSETTINGS=/prepress',
            input_path
        ], check=True, capture_output=True, text=True)
        print(f"✓ Repaired with Ghostscript: {repaired_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Ghostscript repair failed: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ Ghostscript repair failed: {e}")
        return False


def open_pdf_with_repair(path: str) -> Tuple[Optional[PyPDF2.PdfReader], Optional[str]]:
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
        print(f"⚠️  Failed to open PDF directly: {e}")
        print(f"   Attempting repair...")

        # Attempt repairs
        repaired = str(Path(path).with_suffix('')) + '_repaired.pdf'
        repaired_done = False

        if repair_with_pikepdf(path, repaired):
            repaired_done = True
        elif repair_with_ghostscript(path, repaired):
            repaired_done = True

        if not repaired_done:
            raise RuntimeError(f"Failed to read PDF and all repair attempts failed")

        # Try reading the repaired file
        try:
            pdf_reader = PyPDF2.PdfReader(open(repaired, 'rb'))
            return pdf_reader, repaired
        except Exception as e2:
            raise RuntimeError(f"Reading repaired PDF failed: {e2}")


def extract_pages(
    input_path: str,
    output_path: str,
    start_page: int,
    end_page: int,
    verbose: bool = True
) -> dict:
    """
    Extract pages from a PDF to a new PDF with automatic repair if needed.

    Args:
        input_path: Path to the source PDF
        output_path: Path for the output PDF
        start_page: Starting page number (0-indexed)
        end_page: Ending page number (0-indexed, inclusive)
        verbose: Print progress information

    Returns:
        Dictionary with operation status and metadata
    """
    if verbose:
        print(f"\n📄 Extracting pages from: {input_path}")

    pdf_reader, repaired_path = open_pdf_with_repair(input_path)
    total_pages = len(pdf_reader.pages)

    if verbose:
        print(f"   Total pages in source: {total_pages}")

    # Ensure the start_page and end_page are within the valid range
    original_start = start_page
    original_end = end_page

    start_page = max(0, min(start_page, total_pages - 1))
    end_page = min(end_page, total_pages - 1)

    if start_page != original_start or end_page != original_end:
        if verbose:
            print(f"   ⚠️  Adjusted page range from {original_start}-{original_end} to {start_page}-{end_page}")

    # Create a new PDF writer and add the selected pages
    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(start_page, end_page + 1):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    # Write the new PDF to the output file
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    result = {
        'status': 'success',
        'input_file': input_path,
        'output_file': output_path,
        'total_pages_in_source': total_pages,
        'pages_extracted': end_page - start_page + 1,
        'page_range': f"{start_page}-{end_page}",
        'repair_needed': repaired_path is not None,
        'repaired_file': repaired_path
    }

    if verbose:
        print(f"\n✓ Success!")
        print(f"   Extracted {result['pages_extracted']} pages (range: {start_page+1}-{end_page+1} in viewer)")
        print(f"   Output: {output_path}")
        if repaired_path:
            print(f"   ⚠️  Repair was needed, repaired file: {repaired_path}")

    return result


def merge_pdfs(
    input_paths: List[str],
    output_path: str,
    auto_repair: bool = True,
    verbose: bool = True
) -> dict:
    """
    Merge multiple PDF files into a single PDF.

    Args:
        input_paths: List of paths to PDF files to merge
        output_path: Path for the merged output PDF
        auto_repair: Whether to attempt repair on corrupted PDFs
        verbose: Print progress information

    Returns:
        Dictionary with operation status and metadata
    """
    if not input_paths:
        raise ValueError("No input files provided")

    if verbose:
        print(f"\n📑 Merging {len(input_paths)} PDF files...")

    pdf_writer = PyPDF2.PdfWriter()
    files_info = []

    for idx, path in enumerate(input_paths, 1):
        if verbose:
            print(f"   [{idx}/{len(input_paths)}] Processing: {Path(path).name}")

        if auto_repair:
            pdf_reader, repaired_path = open_pdf_with_repair(path)
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

        if verbose and repaired_path:
            print(f"       ⚠️  Repair was needed")

    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    total_pages = sum(info['pages'] for info in files_info)

    result = {
        'status': 'success',
        'output_file': output_path,
        'files_merged': len(input_paths),
        'total_pages': total_pages,
        'files_info': files_info
    }

    if verbose:
        print(f"\n✓ Success!")
        print(f"   Merged {len(input_paths)} files with {total_pages} total pages")
        print(f"   Output: {output_path}")

    return result


def get_pdf_info(pdf_path: str, verbose: bool = True) -> dict:
    """
    Get information about a PDF file.

    Args:
        pdf_path: Path to the PDF file
        verbose: Print information

    Returns:
        Dictionary with PDF metadata and information
    """
    pdf_reader, repaired_path = open_pdf_with_repair(pdf_path)

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

    if verbose:
        print(f"\n📄 PDF Information")
        print(f"   File: {Path(pdf_path).name}")
        print(f"   Total pages: {info['total_pages']}")
        if info['metadata'].get('title') != 'N/A':
            print(f"   Title: {info['metadata']['title']}")
        if info['metadata'].get('author') != 'N/A':
            print(f"   Author: {info['metadata']['author']}")
        if repaired_path:
            print(f"   ⚠️  Repair was needed")

    return info


def main():
    """Command-line interface for PDF operations."""
    parser = argparse.ArgumentParser(
        description='PDF manipulation tool for merging, extracting, and repairing PDFs'
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge multiple PDFs')
    merge_parser.add_argument('files', nargs='+', help='PDF files to merge')
    merge_parser.add_argument('-o', '--output', required=True, help='Output PDF file')

    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract pages from PDF')
    extract_parser.add_argument('input', help='Input PDF file')
    extract_parser.add_argument('start', type=int, help='Start page (0-indexed)')
    extract_parser.add_argument('end', type=int, help='End page (0-indexed, inclusive)')
    extract_parser.add_argument('-o', '--output', required=True, help='Output PDF file')

    # Info command
    info_parser = subparsers.add_parser('info', help='Get PDF information')
    info_parser.add_argument('file', help='PDF file to inspect')

    # Repair command
    repair_parser = subparsers.add_parser('repair', help='Repair a corrupted PDF')
    repair_parser.add_argument('input', help='Input PDF file')
    repair_parser.add_argument('-o', '--output', required=True, help='Output PDF file')

    args = parser.parse_args()

    try:
        if args.command == 'merge':
            merge_pdfs(args.files, args.output)
        elif args.command == 'extract':
            extract_pages(args.input, args.output, args.start, args.end)
        elif args.command == 'info':
            get_pdf_info(args.file)
        elif args.command == 'repair':
            repaired = repair_with_pikepdf(args.input, args.output)
            if not repaired:
                repaired = repair_with_ghostscript(args.input, args.output)
            if not repaired:
                print("✗ All repair attempts failed")
                return 1
        else:
            parser.print_help()
            return 1

        return 0

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
