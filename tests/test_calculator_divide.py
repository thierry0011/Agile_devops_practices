"""
Test suite for Calculator.divide() method.

US4: Division feature tests.
Tests arithmetic division with division-by-zero handling and edge cases.
"""

import pytest
from agile_devops_practices_lab.calculator import Calculator


class TestCalculatorDivide:
    """Test cases for division operation."""

    def test_divide_two_positive_integers(self, calculator):
        """Test division of two positive integers."""
        assert calculator.divide(10, 2) == 5

    def test_divide_resulting_in_float(self, calculator):
        """Test division resulting in float."""
        assert calculator.divide(10, 3) == pytest.approx(3.333, rel=1e-3)

    def test_divide_two_negative_integers(self, calculator):
        """Test division of two negative integers."""
        assert calculator.divide(-10, -2) == 5

    def test_divide_negative_by_positive(self, calculator):
        """Test dividing negative by positive."""
        assert calculator.divide(-10, 2) == -5

    def test_divide_positive_by_negative(self, calculator):
        """Test dividing positive by negative."""
        assert calculator.divide(10, -2) == -5

    def test_divide_zero_by_number(self, calculator):
        """Test dividing zero by a number."""
        assert calculator.divide(0, 5) == 0

    def test_divide_by_one(self, calculator):
        """Test dividing by one (identity)."""
        assert calculator.divide(42, 1) == 42

    def test_divide_by_zero_raises_error(self, calculator):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            calculator.divide(10, 0)
        assert "Division by zero" in str(exc_info.value)

    def test_divide_floats(self, calculator):
        """Test division of floating point numbers."""
        assert calculator.divide(7.5, 2.5) == pytest.approx(3.0)

    def test_divide_mixed_int_float(self, calculator):
        """Test division of integer and float."""
        result = calculator.divide(10, 2.5)
        assert result == pytest.approx(4.0)

    def test_divide_small_by_large(self, calculator):
        """Test dividing small number by large."""
        assert calculator.divide(1, 1000) == pytest.approx(0.001)

    def test_divide_fractional_result(self, calculator):
        """Test fractional division results."""
        assert calculator.divide(1, 3) == pytest.approx(0.3333, rel=1e-3)

    def test_divide_negative_floats(self, calculator):
        """Test division of negative floats."""
        assert calculator.divide(-5.5, 2.5) == pytest.approx(-2.2)

    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5),
        (9, 3, 3),
        (-10, -2, 5),
        (10, -5, -2),
        (0, 10, 0),
        (5, 2, 2.5),
    ])
    def test_divide_parametrized(self, calculator, a, b, expected):
        """Parametrized tests for division with various inputs."""
        assert calculator.divide(a, b) == pytest.approx(expected)

    def test_divide_by_zero_parametrized(self, calculator):
        """Test all division by zero cases raise error."""
        test_cases = [10, 0, -5, 100, 0.5]
        for num in test_cases:
            with pytest.raises(ValueError):
                calculator.divide(num, 0)
