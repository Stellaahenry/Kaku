from dataclasses import dataclass

@dataclass
class Run:
    cells: list     #list of (r, c) coordinates in grid
    total: int = 0 #clue sum

@dataclass
class Grid:
    id: str
    difficulty: str
    cells: list

    @property
    def rows(self):
        return len(self.cells)
    
    @property
    def cols(self):
        return len(self.cells[0])
    
    def is_white(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.cells[r][c] == '.'

    def runs(self):
        """extracts list of white cell runs"""
        across, down = [], []
        for r in range(self.rows):
            c = 0
            while c < self.cols:
                if self.is_white(r, c):
                    seg = []
                    while c < self.cols and self.is_white(r, c):
                        seg.append((r, c))
                        c += 1
                    across.append(Run(seg))
                else:
                    c += 1
        for c in range(self.cols):
            r = 0
            while r < self.rows:
                if self.is_white(r, c):
                    seg = []
                    while r < self.rows and self.is_white(r, c):
                        seg.append((r, c))
                        r += 1
                    down.append(Run(seg))
                else:
                    r += 1
        return across, down
    