"""
Skills Repository

A modular system for organizing reusable functionality.
Each skill is a self-contained module that can be registered and used independently.
"""

from typing import Dict, Any, Callable
import importlib
import inspect


class SkillRegistry:
    """Central registry for all skills."""

    def __init__(self):
        self._skills: Dict[str, Any] = {}

    def register(self, name: str, skill_class: Any):
        """Register a skill with the registry.

        Args:
            name: Unique identifier for the skill
            skill_class: The skill class to register
        """
        if name in self._skills:
            raise ValueError(f"Skill '{name}' is already registered")
        self._skills[name] = skill_class
        print(f"✓ Registered skill: {name}")

    def get(self, name: str) -> Any:
        """Get a skill by name.

        Args:
            name: The skill identifier

        Returns:
            The skill class instance

        Raises:
            KeyError: If skill is not found
        """
        if name not in self._skills:
            raise KeyError(f"Skill '{name}' not found. Available skills: {list(self._skills.keys())}")
        return self._skills[name]

    def list_skills(self) -> Dict[str, Dict[str, Any]]:
        """List all registered skills with their metadata.

        Returns:
            Dictionary of skill names to their metadata
        """
        skills_info = {}
        for name, skill_class in self._skills.items():
            skills_info[name] = {
                'name': name,
                'description': getattr(skill_class, '__doc__', 'No description'),
                'methods': [method for method in dir(skill_class)
                           if not method.startswith('_') and callable(getattr(skill_class, method))]
            }
        return skills_info

    def auto_discover(self, package_name: str = 'skills'):
        """Auto-discover and register skills from a package.

        Args:
            package_name: The package to search for skills
        """
        try:
            package = importlib.import_module(package_name)
            # Iterate through all modules in the package
            for item_name in dir(package):
                item = getattr(package, item_name)
                if inspect.ismodule(item) and hasattr(item, 'skill_class'):
                    skill_name = getattr(item, 'SKILL_NAME', item_name)
                    self.register(skill_name, item.skill_class())
        except ImportError as e:
            print(f"Could not auto-discover skills: {e}")


# Global registry instance
registry = SkillRegistry()


def skill(name: str = None):
    """Decorator to register a skill class.

    Usage:
        @skill(name='my_skill')
        class MySkill:
            def do_something(self):
                pass
    """
    def decorator(cls):
        skill_name = name or cls.__name__.lower()
        registry.register(skill_name, cls())
        return cls
    return decorator
