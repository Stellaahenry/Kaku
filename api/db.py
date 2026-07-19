import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import create_client, Client

from api.models import Puzzle

load_dotenv()

PUZZLES_TABLE = "puzzles"
SOLUTIONS_TABLE = "puzzle_solutions"


@lru_cache
def get_client() -> Client:
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SECRET_KEY"])


def fetch_puzzle(date_str: str) -> Puzzle | None:
    resp = (
        get_client()
        .table(PUZZLES_TABLE)
        .select("*")
        .eq("puzzle_date", date_str)
        .limit(1)
        .execute()
    )
    if not resp.data:
        return None
    return Puzzle.from_row(resp.data[0])


def fetch_solution(date_str: str) -> list | None:
    resp = (
        get_client()
        .table(SOLUTIONS_TABLE)
        .select("solution")
        .eq("puzzle_date", date_str)
        .limit(1)
        .execute()
    )
    if not resp.data:
        return None
    return resp.data[0]["solution"]


def upsert_puzzles(puzzles: dict) -> None:
    client = get_client()
    for date_str, payload in puzzles.items():
        client.table(PUZZLES_TABLE).upsert({
            "puzzle_date": date_str,
            "grid_id": payload["gridId"],
            "difficulty": payload["difficulty"],
            "rows": payload["rows"],
            "cols": payload["cols"],
            "cells": payload["cells"],
        }).execute()
        client.table(SOLUTIONS_TABLE).upsert({
            "puzzle_date": date_str,
            "solution": payload["solution"],
        }).execute()


def delete_puzzles_before(cutoff_date_str: str) -> int:
    """Delete puzzles (and their solutions) dated earlier than cutoff_date_str --> Returns the rows deleted."""
    client = get_client()
    deleted = client.table(PUZZLES_TABLE).delete().lt("puzzle_date", cutoff_date_str).execute()
    client.table(SOLUTIONS_TABLE).delete().lt("puzzle_date", cutoff_date_str).execute()
    return len(deleted.data or [])
