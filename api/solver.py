"""Kakuro solver: backtracking uniqueness check and unique puzzle generator.
Given a Grid (from kakuro_types.py), fills white cells with digits 1-9
such that each run's digits are distinct and sum to the clue value.
"""
import random
from functools import lru_cache
from itertools import combinations

from kakuro_types import Grid, Run

DIGITS = range(1, 10)
ALL = 0b1111111110   #bitmask of digits 1..9 (bit d set means digit d available)

# SUBSETS - list of bitmasks: all valid digit combinations
SUBSETS = {}
for _k in range(1, 10):
    for _combo in combinations(DIGITS, _k):
        _m = sum(1 << d for d in _combo)
        SUBSETS.setdefault((_k, sum(_combo)), []).append(_m)


@lru_cache(maxsize=None)
def _bounds(avail_mask, k):
    """(min, max) sum of k distinct digits drawable from avail_mask, or None."""
    digits = [d for d in DIGITS if avail_mask >> d & 1]
    if len(digits) < k:
        return None
    return sum(digits[:k]), sum(digits[-k:])


# ----------------------------------------------------------------- solver

class Solver:
    """Backtracking solution counter. Stops at `limit` (default 2).

    Pruning: digit distinctness per run + remaining-sum bounds from digits
    still available. Cell order is dynamic (MRV: branch on fewest candidates).
    """

    def __init__(self, grid, across, down):
        self.grid = grid
        self.cell_runs = {}
        for run in across + down:
            for cell in run.cells:
                self.cell_runs.setdefault(cell, []).append(run)
        self.all_cells = sorted(self.cell_runs)
        self.run_used = {id(run): 0 for run in across + down}
        self.run_left = {id(run): len(run.cells) for run in across + down}
        self.run_sum  = {id(run): 0 for run in across + down}

    def count(self, limit=2):
        self.values = {}
        self.limit = limit
        self.found = 0
        self._search()
        return self.found

    def _candidates(self, cell):
        runs = self.cell_runs[cell]
        free = ALL
        for run in runs:
            free &= ~self.run_used[id(run)]
        out = []
        for d in DIGITS:
            if not free >> d & 1:
                continue
            ok = True
            for run in runs:
                rid = id(run)
                rem  = run.total - self.run_sum[rid] - d
                left = self.run_left[rid] - 1
                if left == 0:
                    if rem != 0:
                        ok = False; break
                else:
                    b = _bounds(ALL & ~self.run_used[rid] & ~(1 << d), left)
                    if b is None or rem < b[0] or rem > b[1]:
                        ok = False; break
            if ok:
                out.append(d)
        return out

    def _search(self):
        if self.found >= self.limit:
            return
        best_cell, best_cands = None, None
        for cell in self.all_cells:
            if cell in self.values:
                continue
            cands = self._candidates(cell)
            if best_cands is None or len(cands) < len(best_cands):
                best_cell, best_cands = cell, cands
                if len(cands) <= 1:
                    break
        if best_cell is None:
            self.found += 1
            return
        for d in best_cands:
            self._place(best_cell, d)
            self._search()
            self._unplace(best_cell, d)
            if self.found >= self.limit:
                return

    def _place(self, cell, d):
        self.values[cell] = d
        for run in self.cell_runs[cell]:
            rid = id(run)
            self.run_used[rid] |= 1 << d
            self.run_sum[rid]  += d
            self.run_left[rid] -= 1

    def _unplace(self, cell, d):
        del self.values[cell]
        for run in self.cell_runs[cell]:
            rid = id(run)
            self.run_used[rid] &= ~(1 << d)
            self.run_sum[rid]  -= d
            self.run_left[rid] += 1


# -------------------------------------------------- constraint propagation

def propagate(runs):
    """Propagate constraints to fixpoint. Returns cell -> candidate bitmask.
    If every mask is a single bit, the puzzle is uniquely solvable by logic alone."""
    cand = {}
    for run in runs:
        for cell in run.cells:
            if cell not in cand:
                cand[cell] = ALL

    changed = True
    while changed:
        changed = False
        for run in runs:
            k = len(run.cells)
            subsets = SUBSETS.get((k, run.total), [])
            cell_masks = [cand[c] for c in run.cells]
            union = 0
            for s in subsets:
                if all(m & s for m in cell_masks):
                    covered = 0
                    for m in cell_masks:
                        covered |= m & s
                    if covered == s:
                        union |= s
            solved = 0
            for m in cell_masks:
                if bin(m).count('1') == 1:
                    solved |= m
            for c in run.cells:
                m = cand[c]
                new = m & union
                if bin(m).count('1') > 1:
                    new &= ~solved
                if new != m:
                    cand[c] = new
                    changed = True
    return cand


def propagation_score(runs):
    """Cells still unresolved after propagation (0 = logically solvable + unique)."""
    cand = propagate(runs)
    score = 0
    for m in cand.values():
        n = bin(m).count('1')
        if n == 0:
            return 10_000   # contradiction
        if n > 1:
            score += 1
    return score


# ---------------------------------------------------- puzzle generation

def random_fill(grid, rng):
    """Assign digits to all white cells, distinct within every run.
    Returns {(r,c): digit} or None if the search dead-ends."""
    across, down = grid.runs()
    cell_runs = {}
    for run in across + down:
        for cell in run.cells:
            cell_runs.setdefault(cell, []).append(run)
    cells = sorted(cell_runs)
    used   = {id(run): set() for run in across + down}
    values = {}

    def search(i):
        if i == len(cells):
            return True
        cell = cells[i]
        cands = list(DIGITS)
        for run in cell_runs[cell]:
            cands = [d for d in cands if d not in used[id(run)]]
        rng.shuffle(cands)
        for d in cands:
            values[cell] = d
            for run in cell_runs[cell]:
                used[id(run)].add(d)
            if search(i + 1):
                return True
            for run in cell_runs[cell]:
                used[id(run)].discard(d)
            del values[cell]
        return False

    return values if search(0) else None


def _set_totals(runs, fill):
    for run in runs:
        run.total = sum(fill[cell] for cell in run.cells)


def generate_unique_puzzle(grid, rng, max_iters=20000, restart_after=600):
    """Find a clue assignment that gives exactly one solution.

    Hill-climbs on propagation score (cells not resolvable by logic alone).
    Score 0 means pure logic solves it — ideal for a daily puzzle.
    A backtracking uniqueness check double-confirms the result.
    Returns {"fill", "across", "down", "attempts"} or None on failure.
    """
    across, down = grid.runs()
    runs = across + down
    cell_runs = {}
    for run in runs:
        for cell in run.cells:
            cell_runs.setdefault(cell, []).append(run)
    cells = list(cell_runs)

    def mutate(fill):
        for _ in range(60):
            cell = cells[rng.randrange(len(cells))]
            used = set()
            for run in cell_runs[cell]:
                used |= {fill[c] for c in run.cells if c != cell}
            options = [d for d in DIGITS if d not in used and d != fill[cell]]
            if options:
                new = dict(fill)
                new[cell] = rng.choice(options)
                return new
        return None

    def score(fill):
        _set_totals(runs, fill)
        return propagation_score(runs)

    def is_unique(fill):
        _set_totals(runs, fill)
        return Solver(grid, across, down).count(limit=2) == 1

    fill = random_fill(grid, rng)
    if fill is None:
        return None
    best = score(fill)
    stagnant, tested = 0, False

    for it in range(1, max_iters + 1):
        if best == 0:
            assert is_unique(fill), "propagation-solved puzzle must be unique"
            return {"fill": fill, "across": across, "down": down, "attempts": it}
        if best <= 10 and not tested:
            tested = True
            if is_unique(fill):
                _set_totals(runs, fill)
                return {"fill": fill, "across": across, "down": down, "attempts": it}
        if stagnant >= restart_after:
            fill = random_fill(grid, rng)
            if fill is None:
                return None
            best = score(fill)
            stagnant, tested = 0, False
            continue
        cand = mutate(fill)
        if cand is None:
            stagnant += 1
            continue
        n = score(cand)
        if n < best:
            fill, best, stagnant, tested = cand, n, 0, False
        elif n == best and rng.random() < 0.5:
            fill, stagnant, tested = cand, stagnant + 1, False
        else:
            stagnant += 1

    _set_totals(runs, fill)
    return None


# ------------------------------------------------------------------ export

def puzzle_to_json(grid, result):
    """Serialise to the format the app consumes.
    Each cell is one of:
      {"type": "block"}
      {"type": "clue", "across": int|None, "down": int|None}
      {"type": "entry"}
    """
    across, down = result["across"], result["down"]
    clue_at = {}
    for run in across:
        r, c = run.cells[0]
        clue_at.setdefault((r, c - 1), {})["across"] = run.total
    for run in down:
        r, c = run.cells[0]
        clue_at.setdefault((r - 1, c), {})["down"] = run.total

    cells, solution = [], []
    for r in range(grid.rows):
        crow, srow = [], []
        for c in range(grid.cols):
            if grid.is_white(r, c):
                crow.append({"type": "entry"})
                srow.append(result["fill"][(r, c)])
            elif (r, c) in clue_at:
                k = clue_at[(r, c)]
                crow.append({"type": "clue",
                             "across": k.get("across"), "down": k.get("down")})
                srow.append(0)
            else:
                crow.append({"type": "block"})
                srow.append(0)
        cells.append(crow)
        solution.append(srow)

    return {
        "gridId": grid.id,
        "difficulty": grid.difficulty,
        "rows": grid.rows,
        "cols": grid.cols,
        "cells": cells,
        "solution": solution,
    }
