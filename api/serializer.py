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
