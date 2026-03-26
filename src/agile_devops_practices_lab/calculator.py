"""
Calculator module for arithmetic operations.

Provides core arithmetic operations: addition, subtraction, multiplication, and division.
Designed to work with input validation from the validator module.
"""

from typing import Union


class Calculator:
    """Simple calculator for arithmetic operations."""

    def __init__(self):
        """Initialize calculator."""
        pass

    @staticmethod
    def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        return a + b

    @staticmethod
    def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Subtract two numbers.
        
        Args:
            a: First number
            b: Second number (to subtract from a)
            
        Returns:
            Difference (a - b)
        """
        return a - b

    @staticmethod
    def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        return a * b

    @staticmethod
    def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Divide two numbers.
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            Quotient (a / b)
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

    @staticmethod
    def power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
        """
        Raise a number to a power.
        
        Args:
            base: The base number
            exponent: The exponent to raise the base to
            
        Returns:
            Result of base raised to the exponent
        """
        return base ** exponent
