import random

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
        return grid
    return None


def validate_puzzle(grid):
    black_cells = [[cell == '#' for cell in row] for row in grid]
    n = GRID_SIZE
    if len(black_cells) not in range(BLACK_DENSITY_MIN * n * n, BLACK_DENSITY_MAX * n * n):
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