"""
    Kakuro Grid Generator
"""
import random

DIFFICULTY_LEVELS = { # difficulty: (black density within grid, max white run length)
    "easy": (0.3, 4),
    "medium": (0.22, 5),
    "hard": (0.15, 6),
}

def generate_kakuro_grid(size, density, max_run):
    n = size
    black_cells = [[False] * n for _ in range(n)]
    for i in range(n):
        black_cells[0][i] = True
        black_cells[i][0] = True
    
    # step 1: randomly place black cells
    for i in range(1, n):
        for j in range(1, n):
            if not black_cells[i][j] and random.random() < density:
                black_cells[i][j] = True
    
    # step 2: fix lone white cells and ensure max run length is not exceeded
    for _ in range(40): # limit iterations to prevent infinite loops (chose random number 40 - TODO: update?)
        def runs(horizontal):
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
        done = True

        for horizontal in (True, False):
            for run in runs(horizontal):
                if len(run) == 1: # lone white cell, extend the run by making on neighbour white
                    k, l = run[0]
                    dk, dl = (0, 1) if horizontal else (1, 0)
                    options = [(k - dk, l - dl), (k + dk, l + dl)]
                    options = [(x, y) for x, y in options if 1 <= x < n and 1 <= y < n] # valid neighbours

                    if options:
                        x, y = random.choice(options)
                        black_cells[x][y] = False 
                    else:
                        black_cells[k][l] = True #change to black if no option to extend run
                    done = False
                elif len(run) > max_run:
                    a, b = run[len(run) // 2 + random.randrange(-1, 2)] # break the run by placing a black cell in the middle
                    black_cells[a][b] = True
                    done = False
        if done:
            break
    else:
        return None # failed to generate a valid grid after 40 iterations
    

