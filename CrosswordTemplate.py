import random

class CrosswordTemplate:
    def __init__(self, rows, cols, target_black_squares=0):
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.protected = set()  # Coordinates of seed words
        self.target_black_squares = target_black_squares

    def add_seed_word(self, word, start_r, start_c, direction):
        """Places a word and protects its coordinates from becoming black squares."""
        word = word.lower()
        for i, char in enumerate(word):
            r = start_r + (i if direction == 'down' else 0)
            c = start_c + (i if direction == 'across' else 0)
            
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.grid[r][c] = char
                self.protected.add((r, c))
            else:
                print(f"Warning: Word '{word}' exceeds bounds at ({r}, {c})")

    def _get_symmetric_pos(self, r, c):
        """Calculates the 180-degree rotational symmetry partner."""
        return self.rows - 1 - r, self.cols - 1 - c

    def _is_valid_segment(self, row_or_col):
        """Checks if a row or column string has segments shorter than 3 chars."""
        # Split by black squares
        segments = "".join(row_or_col).split('.')
        for seg in segments:
            if 0 < len(seg) < 3:
                return False
        return True

    def _check_all_rules(self):
        """Validates the 3-character rule across the whole grid."""
        for r in range(self.rows):
            if not self._is_valid_segment(self.grid[r]):
                return False
        for c in range(self.cols):
            col_data = [self.grid[r][c] for r in range(self.rows)]
            if not self._is_valid_segment(col_data):
                return False
        return True

    def generate_blocks(self):
        """Attempts to place black squares following symmetry and min-length rules."""
        count = 0
        attempts = 0
        max_attempts = 1000 # Safety break
        
        while count < self.target_black_squares and attempts < max_attempts:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            sym_r, sym_c = self._get_symmetric_pos(r, c)

            # Rules: 
            # 1. Can't be a seed word cell
            # 2. Can't already be a block
            if (r, c) not in self.protected and (sym_r, sym_c) not in self.protected \
               and self.grid[r][c] == ' ':
                
                # Temporarily place blocks
                old_val = self.grid[r][c]
                old_sym_val = self.grid[sym_r][sym_c]
                self.grid[r][c] = '.'
                self.grid[sym_r][sym_c] = '.'

                if self._check_all_rules():
                    count += 2 if (r, c) != (sym_r, sym_c) else 1
                else:
                    # Rollback if it breaks the 3-char rule
                    self.grid[r][c] = old_val
                    self.grid[sym_r][sym_c] = old_sym_val
            
            attempts += 1

    def display(self):
        for row in self.grid:
            # Using | to visualize the grid clearly
            print("[ '" + "' , '".join(row) + "' ],")

# --- Example Usage ---
# Create a 10x10 grid with approx 20 black squares
ct = CrosswordTemplate(15, 15, target_black_squares=30)

# Add your seed words
# ct.add_seed_word("lauren", 0, 3, "down")
# ct.add_seed_word("derek", 3, 1, "across")
# ct.add_seed_word("tarini", 0, 9, "down")

# Generate the black square layout
ct.generate_blocks()

# Output the result
ct.display()