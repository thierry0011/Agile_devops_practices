"""
Pytest configuration and fixtures.

Provides common fixtures for all test modules.
"""

import pytest
from agile_devops_practices_lab.calculator import Calculator
from agile_devops_practices_lab.validator import InputValidator


@pytest.fixture
def calculator():
    """Provide a Calculator instance for tests."""
    return Calculator()


@pytest.fixture
def validator():
    """Provide an InputValidator instance for tests."""
    return InputValidator()


@pytest.fixture
def sample_numbers():
    """Provide sample numbers for parametrized tests."""
    return [
        (5, 3),
        (10, 4),
        (-5, 3),
        (0, 5),
        (1.5, 2.5),
    ]
