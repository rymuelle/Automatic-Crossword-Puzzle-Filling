import random

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

if __name__=="__main__":
    grid = generate_crossword_template(rows=10, cols=10, seed=42, black_fraction=0.)

    for row in grid:
        print(row, ",")