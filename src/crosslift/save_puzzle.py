
from crosslift.crossword import Crossword
from crosslift.read_write import read_grid
import puz
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(description="Crosslift Command Line Puzzle Generator: Saving as a .puz")
    
    parser.add_argument("--outdir", type=str, default="out", help="Dir to save result to.")
    parser.add_argument("--title", type=str, default="My Puzzle", help="Title of Puzzle")
    parser.add_argument("--name", type=str, default="Ryan Mueller", help="Puzzle creator name.")

    args = parser.parse_args()

    grid = read_grid(Path(args.outdir, "filled_grid.txt"))
    H, W = len(grid), len(grid[0])
    xword = Crossword(H, W, optional_grid=grid)

    p = puz.Puzzle()
    p.width = W
    p.height = H

    # 1. Convert grid to a flat string.
    solution_str = "".join(["".join(row) for row in grid])
    p.solution = solution_str

    # 2. Create the 'fill' (the blank grid for the player)
    # Characters are '-' for playable cells and '.' for blocks
    p.fill = "".join(['-' if c != '.' else '.' for c in solution_str])

    # 3. Add Metadata
    p.title = args.title
    p.author = "Ryan Mueller"

    # 4. Define Clues
    clues = []
    with open(Path(args.outdir, "clues.txt"), 'r') as f:
        for line in f.readlines():
            clues.append(line)
    p.clues = clues
    p.save(Path(args.outdir, "puzzles.puz"))

if __name__ == "__MAIN__":
    main()