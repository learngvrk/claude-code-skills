"""
PDF Skill - PDF manipulation capabilities including merge, extract, and repair.
"""

from .pdf_class import PDFSkill

# Skill metadata
SKILL_NAME = 'pdf'
SKILL_VERSION = '1.0.0'
SKILL_DESCRIPTION = 'PDF manipulation: merge multiple PDFs, extract page ranges, repair corrupted files'

# Export the skill class
skill_class = PDFSkill

__all__ = ['PDFSkill', 'SKILL_NAME', 'SKILL_VERSION', 'SKILL_DESCRIPTION']
