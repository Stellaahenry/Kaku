from datetime import date

from api import db
from api.errors import PuzzleNotFound
from api.generator import generate_monthly_puzzles


def get_puzzle_for_date(date_str: str):
    puzzle = db.fetch_puzzle(date_str)
    if puzzle is None:
        raise PuzzleNotFound
    return puzzle.public_payload()


def generate_and_store_month(year: int, month: int):
    puzzles = generate_monthly_puzzles(year, month)
    db.upsert_puzzles(puzzles)

