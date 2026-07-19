from dataclasses import dataclass


@dataclass
class Puzzle:
    puzzle_date: str
    grid_id: str
    difficulty: str
    rows: int
    cols: int
    cells: list

    @classmethod
    def from_row(cls, row: dict) -> "Puzzle":
        return cls(
            puzzle_date=row["puzzle_date"],
            grid_id=row["grid_id"],
            difficulty=row["difficulty"],
            rows=row["rows"],
            cols=row["cols"],
            cells=row["cells"],
        )

    def public_payload(self) -> dict:
        """Client-facing payload --> solutions are stored separately and never included here."""
        return {
            "date": self.puzzle_date,
            "gridId": self.grid_id,
            "difficulty": self.difficulty,
            "rows": self.rows,
            "cols": self.cols,
            "cells": self.cells,
        }
