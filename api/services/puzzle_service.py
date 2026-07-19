from datetime import date

from api import db
from api.errors import PuzzleNotFound
from api.generator import generate_monthly_puzzles


def get_puzzle_for_date(date_str: str):
    puzzle = db.fetch_puzzle(date_str)
    if puzzle is None:
        raise PuzzleNotFound
    return puzzle.public_payload()


def check_solution(date_str: str, submitted: list) -> bool:
    solution = db.fetch_solution(date_str)
    if solution is None:
        raise PuzzleNotFound
    return submitted == solution


def generate_and_store_month(year: int, month: int):
    puzzles = generate_monthly_puzzles(year, month)
    db.upsert_puzzles(puzzles)


def prune_old_puzzles(today: date | None = None) -> int:
    """Delete any puzzle dated before the first of the current month."""
    today = today or date.today()
    cutoff = date(today.year, today.month, 1).isoformat()
    return db.delete_puzzles_before(cutoff)

