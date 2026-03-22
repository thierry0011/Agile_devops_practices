"""
Test suite for Calculator.subtract() method.

US2: Subtraction feature tests.
Tests arithmetic subtraction with valid inputs, edge cases, and integration.
"""

import pytest
from agile_devops_practices_lab.calculator import Calculator


class TestCalculatorSubtract:
    """Test cases for subtraction operation."""

    def test_subtract_two_positive_integers(self, calculator):
        """Test subtraction of two positive integers."""
        assert calculator.subtract(10, 3) == 7

    def test_subtract_resulting_in_negative(self, calculator):
        """Test subtraction resulting in negative number."""
        assert calculator.subtract(3, 10) == -7

    def test_subtract_two_negative_integers(self, calculator):
        """Test subtraction of two negative integers."""
        assert calculator.subtract(-5, -3) == -2

    def test_subtract_negative_from_positive(self, calculator):
        """Test subtracting negative number from positive."""
        assert calculator.subtract(10, -4) == 14

    def test_subtract_zero(self, calculator):
        """Test subtracting zero from a number."""
        assert calculator.subtract(5, 0) == 5

    def test_subtract_from_zero(self, calculator):
        """Test subtracting a number from zero."""
        assert calculator.subtract(0, 5) == -5

    def test_subtract_same_numbers(self, calculator):
        """Test subtracting identical numbers (result should be zero)."""
        assert calculator.subtract(7, 7) == 0

    def test_subtract_floats(self, calculator):
        """Test subtraction of floating point numbers."""
        assert calculator.subtract(5.5, 2.3) == pytest.approx(3.2)

    def test_subtract_mixed_int_float(self, calculator):
        """Test subtraction of integer and float."""
        result = calculator.subtract(10, 2.5)
        assert result == 7.5

    def test_subtract_large_numbers(self, calculator):
        """Test subtraction of large numbers."""
        assert calculator.subtract(5000000, 2000000) == 3000000

    @pytest.mark.parametrize("a,b,expected", [
        (10, 3, 7),
        (5, 5, 0),
        (-5, -3, -2),
        (10, -4, 14),
        (0, 5, -5),
        (1.5, 0.5, 1.0),
    ])
    def test_subtract_parametrized(self, calculator, a, b, expected):
        """Parametrized tests for subtraction with various inputs."""
        assert calculator.subtract(a, b) == expected
