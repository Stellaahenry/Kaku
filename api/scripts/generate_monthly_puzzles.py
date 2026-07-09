import argparse
import os
import random
import calendar
from datetime import date

from supabase import create_client

from api.generator import generate_kakuro_grid, set_difficulty
from api.solver import generate_unique_puzzle, puzzle_to_json


def generate_and_store_month(year: int, month: int):
    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SECRET_KEY"],
    )

    num_days = calendar.monthrange(year, month)[1]

    for day in range(1, num_days + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        rng = random.Random(int(date(year, month, day).strftime("%Y%m%d")))

        while True:
            grid = generate_kakuro_grid(rng)
            if grid is None:
                continue

            result = generate_unique_puzzle(grid, rng)
            if result is None:
                continue

            grid.id = date_str
            grid.difficulty = set_difficulty(grid)

            payload = puzzle_to_json(grid, result)

            supabase.table("puzzles").upsert({
                "puzzle_date": date_str,
                "grid_id": payload["gridId"],
                "difficulty": payload["difficulty"],
                "rows": payload["rows"],
                "cols": payload["cols"],
                "cells": payload["cells"],
            }).execute()

            supabase.table("puzzle_solutions").upsert({
                "puzzle_date": date_str,
                "solution": payload["solution"],
            }).execute()

            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", type=int, required=True)
    args = parser.parse_args()

    generate_and_store_month(args.year, args.month)