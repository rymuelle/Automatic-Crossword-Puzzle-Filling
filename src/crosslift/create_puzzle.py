import argparse
import random
import sys
from pathlib import Path
import os

# Standard Crosslift imports
from crosslift.crossword import Crossword
from crosslift.timer import Timer
from crosslift.ConstructionAlgorithm import IntelligentLookahead, combine_word_lists, open_dict
from crosslift.scoring import score_xword, score_xword_geometric, open_local_list
from crosslift.generate_grid import generate_grid
from crosslift.read_write import write_grid

file_template = "grid = [\n{}\n]"

def run_construction(args):
    """Main logic for puzzle generation."""
    
    # 1. Prepare word lists
    try:
        word_list_dict, word_score_dict = combine_word_lists(
            [args.wordlist], 
            [1], 
            min_score=args.min_score
        )
        
        # Load seed words (e.g., pokemon names)
        seed_data = open_local_list(args.seedlist, min_score=args.min_score)
        key_word_list = [k for k, v in seed_data.items() if v >= 100]
        
    except FileNotFoundError as e:
        print(f"Error: Could not find required file: {e.filename}")
        sys.exit(1)

    print(f"--- Starting Generation ({args.rows}x{args.cols}) ---")

    attempt = 0
    while True:
        attempt += 1
        
        # Select random words to force into the grid
        words_to_insert = random.sample(key_word_list, min(len(key_word_list), args.n_words))
        
        # Generate the initial black square layout
        test_grid, orig_xword = generate_grid(
            rows=args.rows, 
            cols=args.cols, 
            seed=None, 
            black_fraction=args.black_fraction, 
            max_length=12, 
            words_to_insert=words_to_insert
        )

        if test_grid is None:
            continue        
        # Attempt to fill the grid with words
        print(f"Attempt {attempt}: Filling grid...")
        result, xword = IntelligentLookahead.construct(
            args.rows, 
            args.cols, 
            test_grid, 
            word_list_dict, 
            word_score_dict, 
            sentiment=None
        )

        if result:
            print("\nSUCCESS! Puzzle generated.")
            
            # Scoring
            s_linear = score_xword(xword, word_score_dict)
            s_geom = score_xword_geometric(xword, word_score_dict)
            
            # Display result
            xword.draw_crossword()
            print(f"\nFinal Score (Linear): {s_linear}")
            print(f"Final Score (Geometric): {s_geom}")
            print(f"Inserted Seed Words: {', '.join(words_to_insert)}")

            os.makedirs(args.outdir, exist_ok=True)
            write_grid(xword.getGrid(), Path(args.outdir, "filled_grid.txt"))
            write_grid(orig_xword.grid, Path(args.outdir, "empty_grid.txt"))
            break
        else:
            print("FAILED. Retrying...")

    Timer.outputAll()

def main():
    parser = argparse.ArgumentParser(description="Crosslift Command Line Puzzle Generator")
    
    # Grid Dimensions
    parser.add_argument("--rows", type=int, default=15, help="Number of rows (default: 15)")
    parser.add_argument("--cols", type=int, default=15, help="Number of columns (default: 15)")
    
    # Generation Parameters
    parser.add_argument("--n_words", type=int, default=5, help="Number of seed words to force (default: 5)")
    parser.add_argument("--black_fraction", type=float, default=0.2, help="Percentage of black squares (default: 0.2)")
    parser.add_argument("--min_score", type=int, default=50, help="Minimum word score to include (default: 50)")
    
    # File Paths
    parser.add_argument("--wordlist", type=str, default="xwordlist.dict", help="Main dictionary file")
    parser.add_argument("--seedlist", type=str, default="pokemon.txt", help="Seed words file (e.g. pokemon.txt)")

    parser.add_argument("--outdir", type=str, default="out", help="Dir to save result to.")

    args = parser.parse_args()
    run_construction(args)

if __name__ == "__main__":
    main()