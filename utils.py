def draw_crossword(grid):
    rows = len(grid)
    cols = len(grid[0])

    horizontal = "───"
    top = "┌" + "┬".join([horizontal] * cols) + "┐"
    mid = "├" + "┼".join([horizontal] * cols) + "┤"
    bottom = "└" + "┴".join([horizontal] * cols) + "┘"

    print(top)
    for r, row in enumerate(grid):
        line = "│"
        for cell in row:
            if cell == '.':
                line += "███│"
            elif cell != ' ':
                line += "  {}│".format(cell)
            else:
                line += "   │"
        print(line)
        if r < rows - 1:
            print(mid)
    print(bottom)