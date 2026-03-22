"""
Test suite for Calculator.multiply() method.

US3: Multiplication feature tests.
Tests arithmetic multiplication with valid inputs and edge cases.
"""

import pytest
from agile_devops_practices_lab.calculator import Calculator


class TestCalculatorMultiply:
    """Test cases for multiplication operation."""

    def test_multiply_two_positive_integers(self, calculator):
        """Test multiplication of two positive integers."""
        assert calculator.multiply(5, 3) == 15

    def test_multiply_two_negative_integers(self, calculator):
        """Test multiplication of two negative integers."""
        assert calculator.multiply(-5, -3) == 15

    def test_multiply_positive_and_negative(self, calculator):
        """Test multiplication of positive and negative integers."""
        assert calculator.multiply(10, -4) == -40

    def test_multiply_by_zero(self, calculator):
        """Test multiplying by zero."""
        assert calculator.multiply(5, 0) == 0

    def test_multiply_two_zeros(self, calculator):
        """Test multiplying two zeros."""
        assert calculator.multiply(0, 0) == 0

    def test_multiply_floats(self, calculator):
        """Test multiplication of floating point numbers."""
        assert calculator.multiply(2.5, 4.0) == 10.0

    def test_multiply_mixed_int_float(self, calculator):
        """Test multiplication of integer and float."""
        result = calculator.multiply(5, 2.5)
        assert result == 12.5

    def test_multiply_large_numbers(self, calculator):
        """Test multiplication of large numbers."""
        assert calculator.multiply(1000, 2000) == 2000000

    def test_multiply_negative_floats(self, calculator):
        """Test multiplication of negative floats."""
        assert calculator.multiply(-1.5, -2.5) == pytest.approx(3.75)

    def test_multiply_one(self, calculator):
        """Test multiplying by one (identity)."""
        assert calculator.multiply(42, 1) == 42

    def test_multiply_fractions(self, calculator):
        """Test multiplication of fractions."""
        assert calculator.multiply(0.5, 0.5) == pytest.approx(0.25)

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 6),
        (5, 5, 25),
        (-5, -3, 15),
        (10, -2, -20),
        (0, 100, 0),
        (1.5, 2, 3.0),
    ])
    def test_multiply_parametrized(self, calculator, a, b, expected):
        """Parametrized tests for multiplication with various inputs."""
        assert calculator.multiply(a, b) == expected
