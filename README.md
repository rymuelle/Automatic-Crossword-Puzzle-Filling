# Crosslift

Crosslift is a suite of command-line tools designed to automate the creation, clue generation, and formatting of crossword puzzles. 

## Features

1. Customizable Grids: Adjust dimensions and black square density.

2. Themed Generation: Force specific "seed" words into your puzzle.

3. Automated Cluing: Format and manage clues for your generated grids.

4. Industry Standard Output: Export your finished puzzles to the .puz format.

## Installation

To use Crosslift, ensure you have Python installed, then clone this repository and install the dependencies:
Bash

git clone https://github.com/yourusername/crosslift.git
cd crosslift
pip install .

## Usage Guide

Crosslift is split into three main commands that follow the natural workflow of puzzle creation.
1. Create the Grid (crosslift-create)

Generate the physical layout and fill the words based on your dictionary.

```bash
crosslift-create --rows 15 --cols 15 --seedlist pokemon.txt --outdir ./my_puzzle --n_words 5
```

This will provide both a filled in puzzle, and a blank template puzzle with only the inserted words for manual creation.


2. Format Clues (crosslift-clues)

Process the generated words into a format ready for cluing.

```bash
crosslift-clues --outdir ./my_puzzle
```

This will generate a text file in the output dir of each word. Overwrite the word with your clue prior to exporting to .puz

3. Export to .puz (crosslift-puz)

Finalize your puzzle into the standard .puz format used by most crossword software and players.

```bash
crosslift-puz --title "Gotta Solve 'Em All" --name "Ryan Mueller" --outdir ./my_puzzle
```

## Example puzzle generated:

https://crosshare.org/crosswords/QQMmFnZ2oKKGRS22DAJW/gotta-solve-em-all


## With thanks to:

The original author of the repository (https://github.com/MichaelWehar/Automatic-Crossword-Puzzle-Filling).

Clue database: https://xd.saul.pw/data

Wordlist: https://www.alexboisvert.com/xwordlist/;0