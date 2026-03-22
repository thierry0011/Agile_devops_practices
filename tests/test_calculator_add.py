"""
Test suite for Calculator.add() method.

US1: Addition feature tests.
Tests arithmetic addition with valid inputs, edge cases, and integration.
"""

import pytest
from agile_devops_practices_lab.calculator import Calculator


class TestCalculatorAdd:
    """Test cases for addition operation."""

    def test_add_two_positive_integers(self, calculator):
        """Test addition of two positive integers."""
        assert calculator.add(5, 3) == 8

    def test_add_two_negative_integers(self, calculator):
        """Test addition of two negative integers."""
        assert calculator.add(-5, -3) == -8

    def test_add_positive_and_negative(self, calculator):
        """Test addition of positive and negative integers."""
        assert calculator.add(10, -4) == 6

    def test_add_zero_to_number(self, calculator):
        """Test adding zero to a number."""
        assert calculator.add(5, 0) == 5

    def test_add_two_zeros(self, calculator):
        """Test adding two zeros."""
        assert calculator.add(0, 0) == 0

    def test_add_floats(self, calculator):
        """Test addition of floating point numbers."""
        assert calculator.add(1.5, 2.5) == 4.0

    def test_add_mixed_int_float(self, calculator):
        """Test addition of integer and float."""
        result = calculator.add(5, 2.5)
        assert result == 7.5

    def test_add_large_numbers(self, calculator):
        """Test addition of large numbers."""
        assert calculator.add(1000000, 2000000) == 3000000

    def test_add_negative_floats(self, calculator):
        """Test addition of negative floats."""
        assert calculator.add(-1.5, -2.5) == -4.0

    @pytest.mark.parametrize("a,b,expected", [
        (1, 1, 2),
        (10, 20, 30),
        (-5, 5, 0),
        (0.1, 0.2, pytest.approx(0.3)),
        (100, -50, 50),
    ])
    def test_add_parametrized(self, calculator, a, b, expected):
        """Parametrized tests for addition with various inputs."""
        assert calculator.add(a, b) == expected
