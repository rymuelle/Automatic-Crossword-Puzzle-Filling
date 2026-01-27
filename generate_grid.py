import random
from utils import draw_crossword
from crossword import Crossword

def generate_crossword_template(
    rows=10,
    cols=10,
    black_fraction=0.18,
    min_word_length=3,
    seed=None,
):
    if seed is not None:
        random.seed(seed)

    # start with empty grid
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]

    def symmetric_cell(r, c):
        return rows - 1 - r, cols - 1 - c

    def can_place_black(r, c):
        # tentatively place black at (r, c) and its symmetric partner
        coords = {(r, c), symmetric_cell(r, c)}

        for rr, cc in coords:
            grid[rr][cc] = '.'

        # check all rows for short across words
        for rr in range(rows):
            run = 0
            for cc in range(cols):
                if grid[rr][cc] == ' ':
                    run += 1
                else:
                    if 0 < run < min_word_length:
                        undo(coords)
                        return False
                    run = 0
            if 0 < run < min_word_length:
                undo(coords)
                return False

        # check all columns for short down words
        for cc in range(cols):
            run = 0
            for rr in range(rows):
                if grid[rr][cc] == ' ':
                    run += 1
                else:
                    if 0 < run < min_word_length:
                        undo(coords)
                        return False
                    run = 0
            if 0 < run < min_word_length:
                undo(coords)
                return False

        return True

    def undo(coords):
        for rr, cc in coords:
            grid[rr][cc] = ' '

    target_blacks = int(rows * cols * black_fraction)
    attempts = 0

    while sum(row.count('.') for row in grid) < target_blacks and attempts < 5000:
        r = random.randrange(rows)
        c = random.randrange(cols)

        if grid[r][c] == ' ':
            if can_place_black(r, c):
                pass
            else:
                undo({(r, c), symmetric_cell(r, c)})
        attempts += 1

    return grid

def _generate_grid(rows=15, cols=15, seed=None, black_fraction=0.2, max_length=12, words_to_insert=[]):
        grid = generate_crossword_template(rows=rows, cols=cols, seed=seed, black_fraction=black_fraction)
        
        xword = Crossword(rows, cols, grid)
        lengths = [len(x) for x in xword.getAcrosses()] + [len(x) for x in xword.getDowns()]
        if max(lengths) > max_length: return None

        for word in words_to_insert:
            add_word(xword, word)
        
        for word in words_to_insert:
            if not word in xword.getWords():
                return None
        return xword
            
def generate_grid(rows=15, cols=15, seed=None, black_fraction=0.2, max_length=12, words_to_insert=[]):
    while True:
        xword = _generate_grid(rows, cols, seed, black_fraction, max_length, words_to_insert)
        if xword is not None:
            break
    grid = xword.getGrid()
    grid = [[char.lower() for char in row] for row in grid]
    
    return grid, xword

def add_word(xword, word):
    indicies = []
    for i, across_word in enumerate(xword.getAcrosses()):
        if len(across_word) == len(word):
            indicies.append(i)
    if len(indicies) > 0:
        idx = random.choice(indicies)
        xword.addAcross(idx, word)

if __name__=="__main__":
    grid, xword = generate_grid(rows=15, cols=15, seed=None, black_fraction=0.2, max_length=12, 
                                words_to_insert=["lauren", "tarini", "derek"])


    xword.draw_crossword()
