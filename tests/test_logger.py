"""
Test suite for OperationLogger.

US8: Logging feature tests.
Tests that operations and errors are logged correctly.
"""

import pytest
import tempfile
from pathlib import Path
from agile_devops_practices_lab.logger import OperationLogger, LogLevel


class TestLoggerInitialization:
    """Test cases for logger initialization."""

    def test_create_logger(self):
        """Test creating logger instance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            assert logger is not None

    def test_logger_creates_file(self):
        """Test that logger creates log file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            logger = OperationLogger(log_path)
            logger.log("test message", LogLevel.INFO)
            assert log_path.exists()


class TestLoggerOperations:
    """Test cases for logging operations."""

    def test_log_operation(self):
        """Test logging an operation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log_operation(5, "+", 3, 8)
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            assert "5" in content
            assert "+" in content
            assert "3" in content
            assert "8" in content

    def test_log_multiple_operations(self):
        """Test logging multiple operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log_operation(5, "+", 3, 8)
            logger.log_operation(10, "-", 2, 8)
            logger.log_operation(4, "*", 5, 20)
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                lines = f.readlines()
            assert len(lines) == 3

    def test_log_operation_with_floats(self):
        """Test logging operation with float values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log_operation(1.5, "+", 2.5, 4.0)
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            assert "1.5" in content
            assert "2.5" in content
            assert "4.0" in content


class TestLoggerErrors:
    """Test cases for logging errors."""

    def test_log_error(self):
        """Test logging an error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log_error("Division by zero")
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            assert "ERROR" in content or "error" in content
            assert "Division by zero" in content

    def test_log_multiple_errors(self):
        """Test logging multiple errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log_error("Error 1")
            logger.log_error("Error 2")
            logger.log_error("Error 3")
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                lines = f.readlines()
            assert len(lines) == 3

    def test_log_invalid_input_error(self):
        """Test logging invalid input error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log_error("Invalid input: 'abc' is not a valid number")
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            assert "Invalid input" in content


class TestLoggerTimestamp:
    """Test cases for log timestamps."""

    def test_logs_have_timestamp(self):
        """Test that log entries include timestamp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log("test message", LogLevel.INFO)
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            # Check for common timestamp formats
            assert "2026" in content or "-" in content or ":" in content

    def test_log_operations_timestamped(self):
        """Test that operations are timestamped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log_operation(5, "+", 3, 8)
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            # Look for time/date indicators
            assert ":" in content or "-" in content


class TestLoggerLevels:
    """Test cases for log levels."""

    def test_log_info_level(self):
        """Test logging at INFO level."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log("info message", LogLevel.INFO)
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            assert "INFO" in content or "info" in content.lower()

    def test_log_error_level(self):
        """Test logging at ERROR level."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log("error message", LogLevel.ERROR)
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            assert "ERROR" in content or "error" in content.lower()

    @pytest.mark.parametrize("level", [LogLevel.INFO, LogLevel.ERROR, LogLevel.WARNING])
    def test_all_log_levels(self, level):
        """Test all log levels."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log("test", level)
            
            log_path = Path(tmpdir) / "test.log"
            assert log_path.exists()
            with open(log_path, 'r') as f:
                content = f.read()
            assert len(content) > 0

    def test_log_warning_level(self):
        """Test logging at WARNING level."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log("warning message", LogLevel.WARNING)
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            assert "WARNING" in content or "warning" in content.lower()

    def test_log_warning_method(self):
        """Test log_warning helper method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log_warning("This is a warning")
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                content = f.read()
            assert "WARNING" in content
            assert "This is a warning" in content

    def test_multiple_warnings(self):
        """Test logging multiple warnings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = OperationLogger(Path(tmpdir) / "test.log")
            logger.log_warning("warning 1")
            logger.log_warning("warning 2")
            logger.log_warning("warning 3")
            
            log_path = Path(tmpdir) / "test.log"
            with open(log_path, 'r') as f:
                lines = f.readlines()
            assert len(lines) == 3
