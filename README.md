# Kaku: Kakuro Daily Application

## Usage

```bash
python parse_templates.py "Kakuro Templates.xlsx"   # whenever templates change
python daily.py 2026-06-13                          # one day's puzzle
python generate_bank.py 30                          # or a 30-day static bank
```

## Puzzle JSON format (what the app consumes)

```json
{
  "date": "2026-06-11", "number": 1,
  "templateId": "medium-2", "difficulty": "medium",
  "rows": 9, "cols": 9,
  "cells": [[{"type":"block"} , {"type":"clue","across":17,"down":null},
             {"type":"entry"}, "..."]],
  "solution": [[0, 0, 7, "..."]]
}
```

`cells[r][c].type` is `block`, `clue` (with `across`/`down` sums), or `entry`.
`solution[r][c]` is the digit for entry cells, 0 elsewhere.

