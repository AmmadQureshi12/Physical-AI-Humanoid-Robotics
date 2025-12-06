"""
Test suite for the AI Embodied Intelligence Curriculum
"""
import pytest


def test_curriculum_structure_exists():
    """Test that the basic curriculum structure exists"""
    import os
    assert os.path.exists('book'), "Book directory should exist"
    assert os.path.exists('book/chapter-01-robotic-nervous-system'), "Chapter 1 directory should exist"
    assert os.path.exists('book/chapter-02-digital-twin'), "Chapter 2 directory should exist"


def test_curriculum_config_files_exist():
    """Test that configuration files exist"""
    import os
    assert os.path.exists('book/docusaurus.config.js'), "Docusaurus config should exist"
    assert os.path.exists('book/sidebars.js'), "Sidebars config should exist"
    assert os.path.exists('book/package.json'), "Package.json should exist"


if __name__ == "__main__":
    pytest.main([__file__])