from api.services.puzzle_service import prune_old_puzzles

if __name__ == "__main__":
    deleted = prune_old_puzzles()
    print(f"Deleted {deleted} puzzle(s) dated before the current month.")
