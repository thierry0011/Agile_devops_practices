"""
History module for calculation persistence.

Provides persistent storage of calculation history to JSON file.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class CalculationHistory:
    """Manages calculation history persistence."""

    def __init__(self, filepath: Path):
        """
        Initialize history manager.
        
        Args:
            filepath: Path to JSON history file
        """
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self):
        """Load history from file."""
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []
        else:
            self.history = []

    def _save(self):
        """Save history to file."""
        with open(self.filepath, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add(self, operation: str) -> None:
        """
        Add calculation to history.
        
        Args:
            operation: String representation of calculation (e.g., "5 + 3 = 8")
        """
        entry = {
            "operation": operation,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(entry)
        self._save()

    def get_history(self) -> List[Dict]:
        """
        Get all history entries.
        
        Returns:
            List of history entries
        """
        return self.history

    def get_last(self, n: int = 10) -> List[Dict]:
        """
        Get last N history entries.
        
        Args:
            n: Number of entries to retrieve
            
        Returns:
            List of last N history entries
        """
        return self.history[-n:] if len(self.history) >= n else self.history

    def clear(self) -> None:
        """Clear all history."""
        self.history = []
        self._save()
