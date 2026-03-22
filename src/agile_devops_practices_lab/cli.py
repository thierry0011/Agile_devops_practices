"""
CLI module for command-line interface.

Provides the interactive command-line interface for the calculator.
"""

from typing import Union
from pathlib import Path
from .calculator import Calculator
from .validator import InputValidator, ValidationError
from .history import CalculationHistory
from .logger import OperationLogger


class CLI:
    """Command-line interface for the calculator."""

    def __init__(self):
        """Initialize CLI with calculator and validator."""
        self.calculator = Calculator()
        self.validator = InputValidator()
        self.running = True
        self.history = CalculationHistory(Path("history.json"))
        self.logger = OperationLogger(Path("logs.txt"))

    def display_welcome(self):
        """Display welcome message."""
        print("=" * 50)
        print("Welcome to Agile & DevOps Calculator")
        print("=" * 50)
        print("Operations: + (add), - (subtract), * (multiply), / (divide)")
        print("Type 'exit' to quit")
        print()

    def display_help(self):
        """Display help message."""
        print("\nUsage: Enter two numbers and an operation")
        print("Examples:")
        print("  5 + 3")
        print("  10 - 4")
        print("  6 * 7")
        print("  20 / 4")
        print("\nCommands:")
        print("  history     - Show last 10 calculations")
        print("  history N   - Show last N calculations")
        print("  clear       - Clear history")
        print()


    def parse_input(self, user_input: str) -> tuple:
        """
        Parse user input.
        
        Args:
            user_input: User's input string
            
        Returns:
            Tuple of (num1, operation, num2)
            
        Raises:
            ValidationError: If input format is invalid
        """
        tokens = user_input.strip().split()
        
        if len(tokens) != 3:
            raise ValidationError("Please enter: <number> <operation> <number>")
        
        num1_str, operation, num2_str = tokens
        
        if not self.validator.is_valid_operation(operation):
            raise ValidationError(f"Invalid operation: {operation}")
        
        num1, num2 = self.validator.validate_numbers(num1_str, num2_str)
        
        return num1, operation, num2

    def execute_operation(self, num1: Union[int, float], 
                         operation: str, 
                         num2: Union[int, float]) -> Union[int, float]:
        """
        Execute the requested operation.
        
        Args:
            num1: First operand
            operation: Operation symbol
            num2: Second operand
            
        Returns:
            Result of the operation
            
        Raises:
            ValueError: For invalid operations or division by zero
        """
        if operation == '+':
            return self.calculator.add(num1, num2)
        elif operation == '-':
            return self.calculator.subtract(num1, num2)
        elif operation == '*':
            return self.calculator.multiply(num1, num2)
        elif operation == '/':
            return self.calculator.divide(num1, num2)
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def run_interactive(self):
        """Run interactive calculator session."""
        self.display_welcome()
        
        while self.running:
            try:
                user_input = input(">>> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    print("Goodbye!")
                    self.running = False
                    break
                
                if user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                if user_input.lower() == 'history':
                    self._show_history(10)
                    continue
                
                if user_input.lower().startswith('history '):
                    try:
                        n = int(user_input.split()[1])
                        self._show_history(n)
                    except (ValueError, IndexError):
                        print("Usage: history [N]")
                    continue
                
                if user_input.lower() == 'clear':
                    self.history.clear()
                    print("History cleared.")
                    self.logger.log("History cleared")
                    continue
                
                num1, operation, num2 = self.parse_input(user_input)
                result = self.execute_operation(num1, operation, num2)
                
                print(f"Result: {num1} {operation} {num2} = {result}")
                
                # Log and save to history
                self.logger.log_operation(num1, operation, num2, result)
                self.history.add(f"{num1} {operation} {num2} = {result}")
                
            except ValidationError as e:
                print(f"Validation Error: {e}")
                self.logger.log_error(str(e))
            except ValueError as e:
                print(f"Error: {e}")
                self.logger.log_error(str(e))
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.logger.log_error(str(e))

    def _show_history(self, n: int = 10):
        """Show last N history entries."""
        entries = self.history.get_last(n)
        if not entries:
            print("No history available.")
            return
        print(f"\nLast {min(n, len(entries))} calculations:")
        for i, entry in enumerate(entries, 1):
            print(f"  {i}. {entry['operation']} ({entry['timestamp']})")
        print()

    def run_single(self, expression: str) -> Union[int, float]:
        """
        Run a single calculation.
        
        Args:
            expression: Calculation expression
            
        Returns:
            Result of the calculation
        """
        num1, operation, num2 = self.parse_input(expression)
        return self.execute_operation(num1, operation, num2)


def main():
    """Main entry point for CLI."""
    cli = CLI()
    cli.run_interactive()


if __name__ == "__main__":
    main()
