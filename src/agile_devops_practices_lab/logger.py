"""
Logger module for operation and error logging.

Provides structured logging of operations and errors to file.
"""

from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import Union


class LogLevel(Enum):
    """Log level enumeration."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class OperationLogger:
    """Logs calculator operations and errors."""

    def __init__(self, filepath: Path):
        """
        Initialize logger.
        
        Args:
            filepath: Path to log file
        """
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        """
        Log a message.
        
        Args:
            message: Message to log
            level: Log level
        """
        timestamp = self._get_timestamp()
        log_entry = f"[{timestamp}] {level.value}: {message}\n"
        with open(self.filepath, 'a') as f:
            f.write(log_entry)

    def log_operation(self, a: Union[int, float], op: str, 
                     b: Union[int, float], result: Union[int, float]) -> None:
        """
        Log an operation.
        
        Args:
            a: First operand
            op: Operation symbol
            b: Second operand
            result: Operation result
        """
        message = f"Operation: {a} {op} {b} = {result}"
        self.log(message, LogLevel.INFO)

    def log_error(self, error_message: str) -> None:
        """
        Log an error.
        
        Args:
            error_message: Error description
        """
        self.log(error_message, LogLevel.ERROR)

    def log_warning(self, warning_message: str) -> None:
        """
        Log a warning.
        
        Args:
            warning_message: Warning description
        """
        self.log(warning_message, LogLevel.WARNING)
