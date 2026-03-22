"""
Integration test suite for Calculator CLI.

Tests end-to-end CLI workflows with realistic user scenarios.
Ensures all components work together correctly.
"""

import pytest
from agile_devops_practices_lab.cli import CLI
from agile_devops_practices_lab.validator import ValidationError


class TestCLIParsing:
    """Test CLI input parsing."""

    def test_parse_addition_input(self):
        """Test parsing addition expression."""
        cli = CLI()
        num1, op, num2 = cli.parse_input("5 + 3")
        assert num1 == 5
        assert op == "+"
        assert num2 == 3

    def test_parse_subtraction_input(self):
        """Test parsing subtraction expression."""
        cli = CLI()
        num1, op, num2 = cli.parse_input("10 - 4")
        assert num1 == 10
        assert op == "-"
        assert num2 == 4

    def test_parse_with_whitespace(self):
        """Test parsing with extra whitespace."""
        cli = CLI()
        num1, op, num2 = cli.parse_input("  5  +  3  ")
        assert num1 == 5
        assert op == "+"
        assert num2 == 3

    def test_parse_floats(self):
        """Test parsing floating point numbers."""
        cli = CLI()
        num1, op, num2 = cli.parse_input("1.5 + 2.5")
        assert num1 == 1.5
        assert op == "+"
        assert num2 == 2.5

    def test_parse_invalid_format_too_few_tokens(self):
        """Test parsing with too few tokens raises error."""
        cli = CLI()
        with pytest.raises(ValidationError):
            cli.parse_input("5 +")

    def test_parse_invalid_format_too_many_tokens(self):
        """Test parsing with too many tokens raises error."""
        cli = CLI()
        with pytest.raises(ValidationError):
            cli.parse_input("5 + 3 10")

    def test_parse_invalid_operation(self):
        """Test parsing with invalid operation raises error."""
        cli = CLI()
        with pytest.raises(ValidationError):
            cli.parse_input("5 ^ 3")

    def test_parse_invalid_number_raises_error(self):
        """Test parsing with non-numeric input raises error."""
        cli = CLI()
        with pytest.raises(ValidationError):
            cli.parse_input("abc + 5")


class TestCLIExecution:
    """Test CLI operation execution."""

    def test_execute_addition(self):
        """Test executing addition operation."""
        cli = CLI()
        result = cli.execute_operation(5, '+', 3)
        assert result == 8

    def test_execute_subtraction(self):
        """Test executing subtraction operation."""
        cli = CLI()
        result = cli.execute_operation(10, '-', 3)
        assert result == 7

    def test_execute_with_negative_results(self):
        """Test executing operation with negative result."""
        cli = CLI()
        result = cli.execute_operation(3, '-', 10)
        assert result == -7

    def test_execute_with_floats(self):
        """Test executing operation with floats."""
        cli = CLI()
        result = cli.execute_operation(1.5, '+', 2.5)
        assert result == 4.0

    def test_execute_with_zeros(self):
        """Test executing operations with zero."""
        cli = CLI()
        assert cli.execute_operation(5, '+', 0) == 5
        assert cli.execute_operation(5, '-', 0) == 5


class TestCLIIntegration:
    """Test end-to-end CLI workflows."""

    def test_single_calculation_flow(self):
        """Test complete single calculation flow."""
        cli = CLI()
        result = cli.run_single("5 + 3")
        assert result == 8

    def test_calculation_with_floats_flow(self):
        """Test calculation flow with floating point numbers."""
        cli = CLI()
        result = cli.run_single("1.5 + 2.5")
        assert result == 4.0

    def test_calculation_with_negatives_flow(self):
        """Test calculation flow with negative numbers."""
        cli = CLI()
        result = cli.run_single("-5 + 3")
        assert result == -2

    def test_multiple_operations_flow(self):
        """Test multiple consecutive calculations."""
        cli = CLI()
        
        result1 = cli.run_single("5 + 3")
        assert result1 == 8
        
        result2 = cli.run_single("10 - 4")
        assert result2 == 6

    def test_error_recovery_flow(self):
        """Test that CLI continues after error or invalid input."""
        cli = CLI()
        
        # First, invalid input should not crash
        with pytest.raises(ValidationError):
            cli.run_single("abc + 5")
        
        # But then a valid input should work
        result = cli.run_single("5 + 3")
        assert result == 8
