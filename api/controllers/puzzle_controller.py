from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.errors import PuzzleNotFound
from api.services import puzzle_service

router = APIRouter(prefix="/puzzles", tags=["puzzles"])


class SolutionCheck(BaseModel):
    grid: list[list[int]]


@router.get("/today")
def get_today_puzzle():
    return _get_or_404(date.today().isoformat())


@router.post("/{date_str}/check")
def check_puzzle(date_str: str, body: SolutionCheck):
    try:
        correct = puzzle_service.check_solution(date_str, body.grid)
    except PuzzleNotFound:
        raise HTTPException(status_code=404, detail=f"No puzzle for {date_str}")
    return {"correct": correct}


@router.get("/{date_str}")
def get_puzzle(date_str: str):
    return _get_or_404(date_str)


def _get_or_404(date_str: str):
    try:
        return puzzle_service.get_puzzle_for_date(date_str)
    except PuzzleNotFound:
        raise HTTPException(status_code=404, detail=f"No puzzle for {date_str}")
