from datetime import date

from fastapi import APIRouter, HTTPException

from api.errors import PuzzleNotFound
from api.services import puzzle_service

router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.get("/today")
def get_today_puzzle():
    return _get_or_404(date.today().isoformat())


@router.get("/{date_str}")
def get_puzzle(date_str: str):
    return _get_or_404(date_str)


def _get_or_404(date_str: str):
    try:
        return puzzle_service.get_puzzle_for_date(date_str)
    except PuzzleNotFound:
        raise HTTPException(status_code=404, detail=f"No puzzle for {date_str}")
