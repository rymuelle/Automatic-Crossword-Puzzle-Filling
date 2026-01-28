from pathlib import Path
from typing import List


def write_grid(grid: List[List[str]], path: str | Path) -> None:
    """
    Write a 2D crossword grid to a plain-text ASCII file.

    Each row is written as a single line.
    Each cell must be exactly one character.
    """
    path = Path(path)

    # Sanity checks
    if not grid:
        raise ValueError("Grid is empty")

    width = len(grid[0])
    for row in grid:
        if len(row) != width:
            raise ValueError("Grid is jagged")
        for cell in row:
            if len(cell) != 1:
                raise ValueError(f"Invalid cell {cell!r}")

    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in grid:
            f.write("".join(row) + "\n")



def read_grid(path: str | Path) -> List[List[str]]:
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f]

    if not rows:
        raise ValueError("File is empty")

    width = len(rows[0])
    if any(len(r) != width for r in rows):
        raise ValueError("Grid is not rectangular")

    return [list(row) for row in rows]
