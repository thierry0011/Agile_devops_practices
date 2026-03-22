"""
Validator module for input validation.

Provides validation for numeric inputs and operation requests.
Ensures the calculator handles invalid inputs safely and gracefully.
"""

from typing import Union, Tuple


class ValidationError(ValueError):
    """Raised when input validation fails."""
    pass


class InputValidator:
    """Validates calculator inputs."""

    @staticmethod
    def validate_number(value: str) -> Union[int, float]:
        """
        Validate and convert a string to a number.
        
        Args:
            value: String representation of a number
            
        Returns:
            int or float: The converted numeric value
            
        Raises:
            ValidationError: If the value is not a valid number
        """
        if not value or not isinstance(value, str):
            raise ValidationError("Input cannot be empty")
        
        value = value.strip()
        
        if not value:
            raise ValidationError("Input cannot be empty or whitespace only")
        
        # Check for invalid characters
        try:
            # Try float first (handles both int and float)
            if '.' in value:
                result = float(value)
            else:
                result = int(value)
            return result
        except ValueError:
            raise ValidationError(f"'{value}' is not a valid number")

    @staticmethod
    def validate_numbers(num1: str, num2: str) -> Tuple[Union[int, float], Union[int, float]]:
        """
        Validate two numbers.
        
        Args:
            num1: First number as string
            num2: Second number as string
            
        Returns:
            Tuple of two converted numbers
            
        Raises:
            ValidationError: If either input is invalid
        """
        try:
            n1 = InputValidator.validate_number(num1)
        except ValidationError as e:
            raise ValidationError(f"First number error: {str(e)}")
        
        try:
            n2 = InputValidator.validate_number(num2)
        except ValidationError as e:
            raise ValidationError(f"Second number error: {str(e)}")
        
        return n1, n2

    @staticmethod
    def is_valid_operation(operation: str) -> bool:
        """
        Check if operation is valid.
        
        Args:
            operation: Operation symbol (+, -, etc.)
            
        Returns:
            bool: True if operation is supported
        """
        return operation in {'+', '-', '*', '/'}
