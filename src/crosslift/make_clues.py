from crosslift.crossword import Crossword
from crosslift.read_clues import make_clue_dict
from crosslift.read_write import read_grid
import argparse
from pathlib import Path

def make_clues(args):
    grid = read_grid(Path(args.outdir, "filled_grid.txt"))
    
    H, W = len(grid), len(grid[0])
    xword = Crossword(H, W, optional_grid=grid)
    xword.draw_crossword()

    word_list = xword.get_puz_word_list()

    clue_dict = make_clue_dict(file='wordlists/clues_short.tsv')
    with open(Path(args.outdir, "clues.txt"), 'w') as f:
        for word in word_list:
            if word.upper() in clue_dict and args.make_clues:
                clue = clue_dict[word.upper()][0]
            else:
                clue = word
            f.write(clue +'\n')




def main():
    parser = argparse.ArgumentParser(description="Crosslift Command Line Puzzle Generator Clue Formater")
    
    parser.add_argument("--make_clues",  action="store_true", help="Input previous clues where possible.")

    parser.add_argument("--outdir", type=str, default="out", help="Dir to save result to.")

    args = parser.parse_args()
    make_clues(args)

if __name__ == "__main__":
    main()