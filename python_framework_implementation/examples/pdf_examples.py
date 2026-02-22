"""
Examples demonstrating how to use the PDF Skill.

This file shows various use cases for PDF manipulation.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import skills
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from skills.skill_manager import get_skill


def example_merge_pdfs():
    """Example: Merge multiple PDF files into one."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Merging PDFs")
    print("="*60)

    pdf = get_skill('pdf')

    # Define your input files and output file
    input_files = [
        '/path/to/document1.pdf',
        '/path/to/document2.pdf',
        '/path/to/document3.pdf'
    ]
    output_file = '/path/to/merged_output.pdf'

    try:
        result = pdf.merge_pdfs(
            input_paths=input_files,
            output_path=output_file
        )

        print(f"\n✓ Success!")
        print(f"  Files merged: {result['files_merged']}")
        print(f"  Total pages: {result['total_pages']}")
        print(f"  Output file: {result['output_file']}")

        print("\n  Details:")
        for file_info in result['files_info']:
            repaired = "⚠️ repaired" if file_info['repaired'] else "✓"
            print(f"    {repaired} {file_info['file']} ({file_info['pages']} pages)")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_extract_pages():
    """Example: Extract specific pages from a PDF."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Extracting Pages")
    print("="*60)

    pdf = get_skill('pdf')

    input_file_path = '/path/to/input.pdf'
    output_file_path = '/path/to/output.pdf'

    try:
        result = pdf.extract_pages(
            input_path=input_file_path,
            output_path=output_file_path,
            start_page=6,  # Pages are 0-indexed
            end_page=7
        )

        print(f"\n✓ Success!")
        print(f"  Input: {Path(result['input_file']).name}")
        print(f"  Output: {Path(result['output_file']).name}")
        print(f"  Source total pages: {result['total_pages_in_source']}")
        print(f"  Pages extracted: {result['pages_extracted']} (range: {result['page_range']})")

        if result['repair_needed']:
            print(f"  ⚠️  PDF repair was needed")
            print(f"  Repaired file: {result['repaired_file']}")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_get_pdf_info():
    """Example: Get information about a PDF file."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Getting PDF Information")
    print("="*60)

    pdf = get_skill('pdf')

    pdf_path = '/path/to/your/document.pdf'

    try:
        info = pdf.get_info(pdf_path)

        print(f"\n✓ PDF Information:")
        print(f"  File: {Path(info['file']).name}")
        print(f"  Total pages: {info['total_pages']}")
        print(f"  Repair needed: {'Yes' if info['repair_needed'] else 'No'}")

        if info['metadata']:
            print(f"\n  Metadata:")
            for key, value in info['metadata'].items():
                print(f"    {key}: {value}")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_batch_processing():
    """Example: Process multiple PDFs in a batch operation."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Batch Processing")
    print("="*60)

    pdf = get_skill('pdf')

    # Suppose you have a directory with multiple PDFs
    # and you want to extract the first 5 pages from each

    pdf_files = [
        '/path/to/doc1.pdf',
        '/path/to/doc2.pdf',
        '/path/to/doc3.pdf',
    ]

    output_dir = '/path/to/output/'

    for pdf_file in pdf_files:
        input_path = Path(pdf_file)
        output_path = Path(output_dir) / f"{input_path.stem}_first_5_pages.pdf"

        try:
            result = pdf.extract_pages(
                input_path=str(input_path),
                output_path=str(output_path),
                start_page=0,
                end_page=4  # First 5 pages (0-4)
            )
            print(f"✓ Processed: {input_path.name} -> {output_path.name}")

        except Exception as e:
            print(f"✗ Failed to process {input_path.name}: {e}")


def example_using_skill_manager():
    """Example: Using the SkillManager to explore available skills."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Using Skill Manager")
    print("="*60)

    from skills.skill_manager import SkillManager

    manager = SkillManager()

    # List all available skills
    print("\nListing all available skills:")
    manager.print_skills()

    # Get detailed information programmatically
    all_skills = manager.list_all_skills()
    print(f"\nTotal skills available: {len(all_skills)}")

    for skill_name, info in all_skills.items():
        print(f"\n{skill_name}:")
        print(f"  Methods: {', '.join(info['methods'])}")


def run_all_examples():
    """Run all examples (with placeholder paths)."""
    print("\n")
    print("█"*60)
    print("PDF SKILL USAGE EXAMPLES")
    print("█"*60)

    # Note: These examples use placeholder paths
    # Uncomment and modify paths to run actual operations

    # example_merge_pdfs()
    # example_extract_pages()
    # example_get_pdf_info()
    # example_batch_processing()
    example_using_skill_manager()

    print("\n" + "█"*60)
    print("NOTE: Uncomment examples and update file paths to run actual operations")
    print("█"*60 + "\n")


if __name__ == '__main__':
    run_all_examples()
