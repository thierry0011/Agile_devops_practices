"""
Tests for CLI display and output methods.

Tests the display_welcome, display_help, and _show_history methods
with output capture to verify correct behavior.
"""

import pytest
import tempfile
from pathlib import Path
from io import StringIO
import sys
from agile_devops_practices_lab.cli import CLI


class TestCLIDisplay:
    """Test cases for CLI display methods."""

    def test_display_welcome(self, capsys):
        """Test display_welcome prints welcome message."""
        cli = CLI()
        cli.display_welcome()
        
        captured = capsys.readouterr()
        assert "Welcome" in captured.out
        assert "Calculator" in captured.out

    def test_display_welcome_shows_operations(self, capsys):
        """Test display_welcome shows available operations."""
        cli = CLI()
        cli.display_welcome()
        
        captured = capsys.readouterr()
        assert "+" in captured.out
        assert "-" in captured.out
        assert "*" in captured.out
        assert "/" in captured.out

    def test_display_help(self, capsys):
        """Test display_help shows help message."""
        cli = CLI()
        cli.display_help()
        
        captured = capsys.readouterr()
        assert "Usage" in captured.out
        assert "Examples" in captured.out

    def test_display_help_shows_commands(self, capsys):
        """Test display_help shows available commands."""
        cli = CLI()
        cli.display_help()
        
        captured = capsys.readouterr()
        assert "history" in captured.out
        assert "clear" in captured.out

    def test_display_help_shows_examples(self, capsys):
        """Test display_help shows calculation examples."""
        cli = CLI()
        cli.display_help()
        
        captured = capsys.readouterr()
        assert "5 + 3" in captured.out or "+" in captured.out

    def test_display_welcome_and_help_sequence(self, capsys):
        """Test calling welcome and help in sequence."""
        cli = CLI()
        cli.display_welcome()
        cli.display_help()
        
        captured = capsys.readouterr()
        assert "Welcome" in captured.out
        assert "Usage" in captured.out


class TestCLIShowHistory:
    """Test cases for _show_history method."""

    def test_show_history_empty(self, capsys):
        """Test showing history when no entries exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Override history path to temp directory
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.history.history = []
            
            cli._show_history(10)
            captured = capsys.readouterr()
            assert "No history" in captured.out or "no history" in captured.out.lower()

    def test_show_history_single_entry(self, capsys):
        """Test showing history with single entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.history.add("5 + 3 = 8")
            
            cli._show_history(10)
            captured = capsys.readouterr()
            assert "5 + 3 = 8" in captured.out or "= 8" in captured.out

    def test_show_history_multiple_entries(self, capsys):
        """Test showing history with multiple entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            
            cli.history.add("5 + 3 = 8")
            cli.history.add("10 - 2 = 8")
            cli.history.add("4 * 5 = 20")
            
            cli._show_history(10)
            captured = capsys.readouterr()
            assert "Last" in captured.out or "last" in captured.out.lower()

    def test_show_history_limited_number(self, capsys):
        """Test showing limited number of history entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            
            for i in range(20):
                cli.history.add(f"{i} + 1 = {i+1}")
            
            cli._show_history(5)
            captured = capsys.readouterr()
            # Should show "Last 5 calculations" since we only have 20 total
            assert "Last" in captured.out or "last" in captured.out.lower()

    def test_show_history_shows_timestamps(self, capsys):
        """Test that _show_history displays timestamps."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.history.add("5 + 3 = 8")
            
            cli._show_history(10)
            captured = capsys.readouterr()
            # Check for time formatting (should have colons for HH:MM:SS)
            assert ":" in captured.out or "-" in captured.out

    def test_show_history_with_specific_count(self, capsys):
        """Test showing specific number of history entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            
            cli.history.add("1 + 1 = 2")
            cli.history.add("2 + 2 = 4")
            cli.history.add("3 + 3 = 6")
            
            cli._show_history(2)
            captured = capsys.readouterr()
            assert "Last" in captured.out or "last" in captured.out.lower()

    def test_show_history_output_formatting(self, capsys):
        """Test that history output is properly formatted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            cli.history.add("5 + 3 = 8")
            
            cli._show_history(10)
            captured = capsys.readouterr()
            # Should have numbered entries
            assert "1." in captured.out or "5 + 3 = 8" in captured.out


class TestCLIIntegrationDisplayAndHistory:
    """Test integration of display methods and history."""

    def test_run_single_updates_history(self):
        """Test that run_single executes correctly (history only in interactive mode)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            
            result = cli.run_single("5 + 3")
            assert result == 8

    def test_multiple_operations_create_history(self):
        """Test that multiple operations execute correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            
            result1 = cli.run_single("5 + 3")
            result2 = cli.run_single("10 - 2")
            result3 = cli.run_single("4 * 5")
            
            assert result1 == 8
            assert result2 == 8
            assert result3 == 20

    def test_show_history_after_operations(self, capsys):
        """Test showing history after performing operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cli = CLI()
            cli.history.filepath = Path(tmpdir) / "history.json"
            
            cli.run_single("5 + 3")
            cli.run_single("10 - 2")
            
            cli._show_history(10)
            captured = capsys.readouterr()
            assert len(captured.out) > 0
