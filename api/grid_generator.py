"""
    Kakuro Grid Generator
"""
import random
from kakuro_types import Grid

DIFFICULTY_LEVELS = { # difficulty: (black density within grid, max white run length)
    "easy": (0.38, 4),
    "medium": (0.22, 5),
    "hard": (0.15, 6),
}

MIN_WHITE_CELLS = 0.45

def generate_kakuro_grid(size, density, max_run, rng=random):
    n = size
    black_cells = [[False] * n for _ in range(n)]
    for i in range(n):
        black_cells[0][i] = True
        black_cells[i][0] = True

    def grid_runs(horizontal):
        out = []
        for i in range(1, n):
            segment = []
            for j in range(1, n+1):
                k, l = (i, j) if horizontal else (j, i)
                if j < n and not black_cells[k][l]:
                    segment.append((k, l))
                else:
                    if segment:
                        out.append(segment)
                    segment = []
        return out

    #step 1:randomly place black cells
    for i in range(1, n):
        for j in range(1, n):
            if not black_cells[i][j] and rng.random() < density:
                black_cells[i][j] = True

    # step 2: fix lone white cells and ensure max run length is not exceeded
    for _ in range(40):
        done = True
        for horizontal in (True, False):
            for run in grid_runs(horizontal):
                if len(run) == 1:
                    k, l = run[0]
                    dk, dl = (0, 1) if horizontal else (1, 0)
                    options = [(k - dk, l - dl), (k + dk, l + dl)]
                    options = [(x, y) for x, y in options if 1 <= x < n and 1 <= y < n]
                    if options:
                        x, y = rng.choice(options)
                        black_cells[x][y] = False
                    else:
                        black_cells[k][l] = True
                    done = False
                elif len(run) > max_run:
                    a, b = run[len(run) // 2 + rng.randrange(-1, 2)]
                    black_cells[a][b] = True
                    done = False
        if done:
            break
    else:
        return None
    
    valid = validate_grid(black_cells, n)

    if valid:
        grid = [''.join('#' if black_cells[r][c] else '.' for c in range(n)) for r in range(n)]
        grid_object = Grid("candidate", "?", grid)
        if final_validate_grid(grid_object):
            return None
        a, d = grid_object.runs()
        if any(len(run.cells) > max_run for run in a + d):
            return None
        return grid
    return None

    
def validate_grid(black_cells, n):
    white_cells = {(x, y) for x in range(1, n) for y in range(1, n) if not black_cells[x][y]}
    if len(white_cells) < MIN_WHITE_CELLS * (n-1)**2: #checks density of white cells in centre of grid
        return None

    start = next(iter(white_cells))
    visited = {start}
    stack = [start]

    while stack:
        x, y = stack.pop()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in white_cells and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((nx, ny))
    
    if len(visited) == len(white_cells):
        return black_cells
    return None

def final_validate_grid(grid):
    problems = []
    across, down = grid.runs()
    for kind, runs in (("across", across), ("down", down)):
        for run in runs:
            if len(run.cells) == 1:
                problems.append(f"length-1 {kind} run at {run.cells[0]}")
            if len(run.cells) > 9:
                problems.append(f"{kind} run longer than 9 at {run.cells[0]}")
    if not across and not down:
        problems.append("no white cells")
    return problems


def generate_grids(count, size, difficulty, rng=random):
    density, max_run = DIFFICULTY_LEVELS[difficulty]
    grids = []
    while len(grids) < count:
        grid = generate_kakuro_grid(size, density, max_run, rng)
        if grid:
            grids.append(grid)
    return grids