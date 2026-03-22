"""
Tests for CLI interactive mode with mocked input/output.

Tests the CLI interactive loop by mocking stdin and stdout.
"""

import pytest
import tempfile
from pathlib import Path
from unittest import mock
from io import StringIO
from agile_devops_practices_lab.cli import CLI


class TestCLIInteractiveMode:
    """Test cases for CLI interactive mode."""

    def test_interactive_exit_command(self):
        """Test exiting interactive mode with 'exit' command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Mock input to provide 'exit' command
            with mock.patch('builtins.input', return_value='exit'):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            assert not cli.running

    def test_interactive_help_command(self):
        """Test help command in interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Mock input to provide 'help' then 'exit'
            with mock.patch('builtins.input', side_effect=['help', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()) as fake_out:
                    cli.run_interactive()
            
            assert not cli.running

    def test_interactive_calculation(self):
        """Test performing calculation in interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Mock input to perform calculation then exit
            with mock.patch('builtins.input', side_effect=['5 + 3', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            # Check that calculation was logged
            log_path = Path(tmpdir) / "logs.txt"
            assert log_path.exists()

    def test_interactive_show_history_command(self):
        """Test history command in interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Add some history first
            cli.history.add("5 + 3 = 8")
            
            # Mock input to show history then exit
            with mock.patch('builtins.input', side_effect=['history', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            assert not cli.running

    def test_interactive_history_n_command(self):
        """Test history N command in interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Add some history
            for i in range(10):
                cli.history.add(f"{i} + 1 = {i+1}")
            
            # Mock input to show last 3 histories then exit
            with mock.patch('builtins.input', side_effect=['history 3', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            assert not cli.running

    def test_interactive_clear_command(self):
        """Test clear command in interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Add history first
            cli.history.add("5 + 3 = 8")
            initial_count = len(cli.history.get_history())
            assert initial_count > 0
            
            # Mock input to clear history then exit
            with mock.patch('builtins.input', side_effect=['clear', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            # History should be cleared
            assert len(cli.history.get_history()) == 0

    def test_interactive_invalid_input_error_handling(self):
        """Test handling invalid input in interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Mock input with invalid operation then exit
            with mock.patch('builtins.input', side_effect=['5 ^ 3', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            # Should recover and exit successfully
            assert not cli.running

    def test_interactive_empty_input(self):
        """Test handling empty input in interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Mock input with empty line, then valid calc, then exit
            with mock.patch('builtins.input', side_effect=['', '5 + 3', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            assert not cli.running

    def test_interactive_division_by_zero(self):
        """Test handling division by zero in interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Mock input with division by zero then exit
            with mock.patch('builtins.input', side_effect=['5 / 0', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            # Should handle error and continue
            assert not cli.running

    def test_interactive_multiple_operations(self):
        """Test performing multiple operations in interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Mock input with multiple operations then exit
            with mock.patch('builtins.input', side_effect=['5 + 3', '10 - 2', '4 * 5', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            # All operations should be in history
            history = cli.history.get_history()
            assert len(history) >= 3

    def test_interactive_logs_operations(self):
        """Test that operations are logged during interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Mock input to perform calculation then exit
            with mock.patch('builtins.input', side_effect=['5 + 3', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            # Check that operation was logged
            log_path = Path(tmpdir) / "logs.txt"
            with open(log_path, 'r') as f:
                log_content = f.read()
            
            assert "5" in log_content
            assert "3" in log_content

    def test_interactive_logs_errors(self):
        """Test that errors are logged during interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.logger.filepath = Path(tmpdir) / "logs.txt"
            
            # Mock input with invalid input then exit
            with mock.patch('builtins.input', side_effect=['abc + 5', 'exit']):
                with mock.patch('sys.stdout', new=StringIO()):
                    cli.run_interactive()
            
            # Error should be logged
            log_path = Path(tmpdir) / "logs.txt"
            with open(log_path, 'r') as f:
                log_content = f.read()
            
            assert "ERROR" in log_content or "Error" in log_content or "error" in log_content.lower()
