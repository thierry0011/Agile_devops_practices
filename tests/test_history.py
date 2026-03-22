"""
Test suite for CalculationHistory.

US6: History persistence feature tests.
Tests that calculations are saved, loaded, and managed correctly.
"""

import pytest
import json
import tempfile
from pathlib import Path
from agile_devops_practices_lab.history import CalculationHistory


class TestCalculationHistorySave:
    """Test cases for saving calculations."""

    def test_save_single_calculation(self):
        """Test saving a single calculation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = CalculationHistory(Path(tmpdir) / "history.json")
            history.add("5 + 3 = 8")
            assert len(history.get_history()) == 1

    def test_save_multiple_calculations(self):
        """Test saving multiple calculations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = CalculationHistory(Path(tmpdir) / "history.json")
            history.add("5 + 3 = 8")
            history.add("10 - 2 = 8")
            history.add("4 * 5 = 20")
            assert len(history.get_history()) == 3

    def test_history_persists_to_file(self):
        """Test that history is persisted to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "history.json"
            history1 = CalculationHistory(path)
            history1.add("5 + 3 = 8")
            
            # Create new instance with same file
            history2 = CalculationHistory(path)
            assert len(history2.get_history()) == 1


class TestCalculationHistoryLoad:
    """Test cases for loading history."""

    def test_load_empty_history(self):
        """Test loading with no prior file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = CalculationHistory(Path(tmpdir) / "history.json")
            assert len(history.get_history()) == 0

    def test_load_existing_history(self):
        """Test loading existing history file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "history.json"
            
            # Create history file manually
            data = [
                {"operation": "5 + 3 = 8", "timestamp": "2026-03-22 10:00:00"},
                {"operation": "10 - 2 = 8", "timestamp": "2026-03-22 10:01:00"}
            ]
            with open(path, 'w') as f:
                json.dump(data, f)
            
            history = CalculationHistory(path)
            assert len(history.get_history()) == 2

    def test_get_history_returns_list(self):
        """Test that get_history returns a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = CalculationHistory(Path(tmpdir) / "history.json")
            result = history.get_history()
            assert isinstance(result, list)


class TestCalculationHistoryRetrieve:
    """Test cases for retrieving history."""

    def test_get_last_n_calculations(self):
        """Test retrieving last N calculations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = CalculationHistory(Path(tmpdir) / "history.json")
            for i in range(10):
                history.add(f"{i} + 1 = {i+1}")
            
            last_5 = history.get_last(5)
            assert len(last_5) == 5

    def test_get_more_than_available(self):
        """Test requesting more history than available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = CalculationHistory(Path(tmpdir) / "history.json")
            history.add("5 + 3 = 8")
            history.add("10 - 2 = 8")
            
            all_history = history.get_last(100)
            assert len(all_history) == 2

    def test_history_entries_have_timestamp(self):
        """Test that history entries contain timestamp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = CalculationHistory(Path(tmpdir) / "history.json")
            history.add("5 + 3 = 8")
            
            entries = history.get_history()
            assert len(entries) > 0
            assert "timestamp" in entries[0]
            assert "operation" in entries[0]


class TestCalculationHistoryClear:
    """Test cases for clearing history."""

    def test_clear_history(self):
        """Test clearing all history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = CalculationHistory(Path(tmpdir) / "history.json")
            history.add("5 + 3 = 8")
            history.add("10 - 2 = 8")
            assert len(history.get_history()) == 2
            
            history.clear()
            assert len(history.get_history()) == 0

    def test_clear_empty_history(self):
        """Test clearing already empty history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = CalculationHistory(Path(tmpdir) / "history.json")
            history.clear()  # Should not raise error
            assert len(history.get_history()) == 0
