"""
Tests for __main__.py module entry point.

Verifies that the module can be run directly as an entry point.
"""

import pytest


def test_main_imports_successfully():
    """Test that main() can be imported from cli module."""
    from agile_devops_practices_lab.cli import main
    assert callable(main)


def test_main_module_executable():
    """Test that __main__ module is executable."""
    import agile_devops_practices_lab.__main__
    assert hasattr(agile_devops_practices_lab.__main__, '__name__')
