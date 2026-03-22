"""
Test suite for InputValidator.

US5: Input Validation feature tests.
Tests that invalid input is rejected, errors are clear, and program continues safely.
"""

import pytest
from agile_devops_practices_lab.validator import InputValidator, ValidationError


class TestInputValidatorValidateNumber:
    """Test cases for validate_number method."""

    def test_validate_positive_integer(self, validator):
        """Test validation of positive integer."""
        assert validator.validate_number("5") == 5

    def test_validate_negative_integer(self, validator):
        """Test validation of negative integer."""
        assert validator.validate_number("-5") == -5

    def test_validate_zero(self, validator):
        """Test validation of zero."""
        assert validator.validate_number("0") == 0

    def test_validate_float(self, validator):
        """Test validation of float."""
        assert validator.validate_number("3.14") == 3.14

    def test_validate_negative_float(self, validator):
        """Test validation of negative float."""
        assert validator.validate_number("-2.5") == -2.5

    def test_validate_number_with_whitespace(self, validator):
        """Test validation of number with leading/trailing whitespace."""
        assert validator.validate_number("  42  ") == 42

    def test_validate_non_numeric_string_raises_error(self, validator):
        """Test that non-numeric string raises ValidationError."""
        with pytest.raises(ValidationError):
            validator.validate_number("abc")

    def test_validate_empty_string_raises_error(self, validator):
        """Test that empty string raises ValidationError."""
        with pytest.raises(ValidationError):
            validator.validate_number("")

    def test_validate_whitespace_only_raises_error(self, validator):
        """Test that whitespace-only string raises ValidationError."""
        with pytest.raises(ValidationError):
            validator.validate_number("   ")

    def test_validate_special_characters_raise_error(self, validator):
        """Test that special characters raise ValidationError."""
        with pytest.raises(ValidationError):
            validator.validate_number("5@#$")

    def test_validate_mixed_alphanumeric_raises_error(self, validator):
        """Test that mixed alphanumeric raises ValidationError."""
        with pytest.raises(ValidationError):
            validator.validate_number("5a")

    def test_validate_error_message_is_clear(self, validator):
        """Test that error message is clear and user-friendly."""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_number("not_a_number")
        assert "not a valid number" in str(exc_info.value)


class TestInputValidatorValidateNumbers:
    """Test cases for validate_numbers method."""

    def test_validate_two_positive_numbers(self, validator):
        """Test validation of two positive numbers."""
        num1, num2 = validator.validate_numbers("5", "3")
        assert num1 == 5 and num2 == 3

    def test_validate_two_negative_numbers(self, validator):
        """Test validation of two negative numbers."""
        num1, num2 = validator.validate_numbers("-5", "-3")
        assert num1 == -5 and num2 == -3

    def test_validate_mixed_positive_negative(self, validator):
        """Test validation of mixed positive and negative numbers."""
        num1, num2 = validator.validate_numbers("10", "-5")
        assert num1 == 10 and num2 == -5

    def test_validate_floats_and_integers(self, validator):
        """Test validation of float and integer."""
        num1, num2 = validator.validate_numbers("5.5", "3")
        assert num1 == 5.5 and num2 == 3

    def test_validate_invalid_first_number_raises_error(self, validator):
        """Test that invalid first number raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_numbers("abc", "5")
        assert "First number" in str(exc_info.value)

    def test_validate_invalid_second_number_raises_error(self, validator):
        """Test that invalid second number raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_numbers("5", "xyz")
        assert "Second number" in str(exc_info.value)

    def test_validate_both_invalid_raises_first_error(self, validator):
        """Test that if both are invalid, first error is raised."""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_numbers("abc", "xyz")
        assert "First number" in str(exc_info.value)


class TestInputValidatorIsValidOperation:
    """Test cases for is_valid_operation method."""

    @pytest.mark.parametrize("operation,expected", [
        ('+', True),
        ('-', True),
        ('*', True),
        ('/', True),
        ('add', False),
        ('x', False),
        ('^', False),
        ('', False),
        ('++', False),
    ])
    def test_is_valid_operation(self, validator, operation, expected):
        """Parametrized test for operation validation."""
        assert validator.is_valid_operation(operation) == expected

    def test_all_supported_operations_are_valid(self, validator):
        """Test that all four supported operations are valid."""
        operations = ['+', '-', '*', '/']
        for op in operations:
            assert validator.is_valid_operation(op)

    def test_unsupported_operations_are_invalid(self, validator):
        """Test that unsupported operations are invalid."""
        invalid_ops = ['^', '%', '&', '|', '**']
        for op in invalid_ops:
            assert not validator.is_valid_operation(op)
