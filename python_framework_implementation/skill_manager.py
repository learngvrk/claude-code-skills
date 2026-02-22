"""
Skill Manager - Easy interface for using skills.
"""

from . import registry
from .pdf import PDFSkill


class SkillManager:
    """
    High-level interface for working with skills.

    This provides a convenient way to discover, load, and use skills.
    """

    def __init__(self):
        """Initialize the skill manager and register available skills."""
        self.registry = registry
        self._auto_register_skills()

    def _auto_register_skills(self):
        """Automatically register all available skills."""
        # Register PDF skill
        try:
            self.registry.register('pdf', PDFSkill())
            print("✓ PDF skill registered successfully")
        except ValueError as e:
            print(f"Note: {e}")

        # Add more skills here as they are created
        # self.registry.register('excel', ExcelSkill())
        # self.registry.register('image', ImageSkill())

    def get_skill(self, skill_name: str):
        """
        Get a skill by name.

        Args:
            skill_name: The name of the skill to retrieve

        Returns:
            The skill instance

        Example:
            manager = SkillManager()
            pdf = manager.get_skill('pdf')
            pdf.merge_pdfs(['file1.pdf', 'file2.pdf'], 'output.pdf')
        """
        return self.registry.get(skill_name)

    def list_all_skills(self):
        """
        List all available skills with their descriptions.

        Returns:
            Dictionary of skill information
        """
        return self.registry.list_skills()

    def print_skills(self):
        """Print a formatted list of all available skills."""
        skills = self.list_all_skills()

        print("\n" + "="*60)
        print("AVAILABLE SKILLS")
        print("="*60)

        if not skills:
            print("No skills registered yet.")
            return

        for skill_name, info in skills.items():
            print(f"\n📦 {skill_name.upper()}")
            print(f"   Description: {info['description']}")
            print(f"   Methods:")
            for method in info['methods']:
                print(f"      - {method}()")

        print("\n" + "="*60)


# Convenience function for quick access
def get_skill(name: str):
    """
    Quick access to a skill.

    Args:
        name: The skill name

    Returns:
        The skill instance

    Example:
        from skills.skill_manager import get_skill
        pdf = get_skill('pdf')
    """
    manager = SkillManager()
    return manager.get_skill(name)
