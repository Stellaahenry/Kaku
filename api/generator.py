import random
import calendar
from api.kakuro_types import Grid
from datetime import date
from api.solver import generate_unique_puzzle
from api.serializer import puzzle_to_json


GRID_SIZE = 9
BLACK_DENSITY_MIN = 0.55
BLACK_DENSITY_MAX = 0.65


def generate_kakuro_grid(rng=random):
    n = GRID_SIZE
    black_cells = [[False] * n for _ in range(n)]

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

    # set left column and top row to be black cells
    for r in range(n):
        black_cells[r][0] = True
        black_cells[0][r] = True

    # randomly place black cells in the grid
    density = rng.uniform(BLACK_DENSITY_MIN, BLACK_DENSITY_MAX)
    for r in range(1, n):
        for c in range(1, n):
            if rng.random() < density:
                black_cells[r][c] = True
    
    # ensure that there are no lone white cells
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
        if done:
            break
    else:
        return None
    
    if validate_puzzle(black_cells):
        grid = [''.join('#' if black_cells[r][c] else '.' for c in range(n)) for r in range(n)]
        grid_object = Grid("candidate", "?", grid)
        return grid_object
    return None


def validate_puzzle(black_cells):
    n = GRID_SIZE
    black_count = sum(black_cells[r][c] for r in range(n) for c in range(n))
    if not (BLACK_DENSITY_MIN <= black_count / (n * n) <= BLACK_DENSITY_MAX):
        return False
    
    # DFS check to see if all white cells are connected
    start = None

    for r in range(n):
        for c in range(n):
            if not black_cells[r][c]:
                start = (r, c)
                break
        else:
            continue
        break

    if start is None:
        return False
    
    stack = [start]
    visited = set()
    visited.add(start)

    while stack:
        r, c = stack.pop()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not black_cells[nr][nc] and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append((nr, nc))

    if len(visited) != sum(not cell for row in black_cells for cell in row):
        return False
    return True


def set_difficulty(grid):
    return "easy" #placeholder for difficulty logic


def generate_monthly_grids(year: int, month: int):
    num_days = calendar.monthrange(year, month)[1]
    monthly = {}

    for day in range(1, num_days + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        seed = int(date(year, month, day).strftime("%Y%m%d"))
        rng = random.Random(seed)

        grid = None
        while grid is None:
            grid = generate_kakuro_grid(rng)

        grid.id = date_str
        grid.difficulty = set_difficulty(grid)
        monthly[date_str] = grid

    return monthly


def generate_monthly_puzzles(year: int, month: int):
    grids = generate_monthly_grids(year, month)
    puzzles = {}

    for date_str, grid in grids.items():
        rng = random.Random(int(date_str.replace("-", "")))
        result = generate_unique_puzzle(grid, rng)

        if result is None:
            continue

        puzzles[date_str] = puzzle_to_json(grid, result)

    return puzzles
