from crossword import Crossword
from timer import Timer
from construction_algorithm import *
from scoring import *
import random
from generate_grid import generate_grid
# from sentiment import self_sentiment_score


test_grid = [
             [' ', ' ', ' ', ' ', ' ', ' '],
             [' ', '.', ' ', 'd', ' ', ' '],
             [' ', ' ', ' ', 'e', ' ', ' '],
             ['l', 'a', 'u', 'r', 'e', 'n'],
             [' ', ' ', ' ', 'e', ' ', ' '],
             [' ', ' ', ' ', 'k', ' ', ' '],
            ]
test_grid = [
['l', 'a', 'u', 'r', 'e', 'n', '.', ' ', ' ', ' '] ,
[' ', ' ', ' ', ' ', ' ', ' ', '.', ' ', ' ', ' '] ,
[' ', ' ', ' ', ' ', ' ', ' ', '.', ' ', ' ', ' '] ,
[' ', ' ', ' ', ' ', ' ', '.', ' ', ' ', ' ', '.'] ,
['.', '.', '.', 'd', 'e', 'r', 'e', 'k', '.', '.'] ,
['.', '.', ' ', ' ', ' ', ' ', ' ', '.', '.', '.'] ,
['.', ' ', ' ', ' ', '.', ' ', ' ', ' ', ' ', ' '] ,
[' ', ' ', ' ', '.', ' ', ' ', ' ', ' ', ' ', ' '] ,
[' ', ' ', ' ', '.', 't', 'a', 'r', 'i', 'n', 'i'] ,
[' ', ' ', ' ', '.', ' ', ' ', ' ', ' ', ' ', ' '] ,
]





wordlist_file = 'xwordlist.dict'

xword_list = []
score_list = []
score_list_geom = []
sentiment_list = []

n_puzzles = 10
for i in range(n_puzzles):
    test_grid = [
['t', 'a', 'r', 'i', 'n', 'i', '.', ' ', ' ', 'd'] ,
[' ', ' ', '.', ' ', ' ', ' ', '.', ' ', ' ', 'e'] ,
[' ', ' ', ' ', ' ', ' ', ' ', '.', ' ', ' ', 'r'] ,
[' ', ' ', ' ', '.', ' ', ' ', ' ', ' ', ' ', 'e'] ,
['.', '.', ' ', ' ', '.', ' ', ' ', '.', ' ', 'k'] ,
[' ', ' ', '.', ' ', ' ', '.', ' ', ' ', '.', '.'] ,
[' ', ' ', ' ', ' ', ' ', ' ', '.', ' ', ' ', ' '] ,
[' ', ' ', ' ', '.', ' ', ' ', ' ', ' ', ' ', ' '] ,
[' ', ' ', ' ', '.', ' ', ' ', ' ', '.', ' ', ' '] ,
[' ', ' ', ' ', '.', 'l', 'a', 'u', 'r', 'e', 'n'] ,
    ]
    #words_to_insert=["horseland", "nookmiles", "bells", "katie", "Isabelle", "Blathers", "dace"]
    row, column = 10, 10
    test_grid, _xword= generate_grid(rows=row, cols=column, seed=None, black_fraction=.20, max_length=12, 
                                     words_to_insert=[])
    sentiment = None

    word_list_dict = readWordList(wordlist_file)
    score_dict = open_dict(wordlist_file)
    result, xword = IntelligentLookahead.construct(row, column, test_grid, word_list_dict, score_dict, sentiment=sentiment)
    if result:
        print("SUCCESS", i)
        score = score_xword(xword, wordlist_file)
        score_goem = score_xword_geometric(xword, wordlist_file)
        xword_list.append(xword)
        score_list.append(score)
        score_list_geom.append(score_goem)
        # sentiment_list.append(self_sentiment_score(xword.getWords())[0])
        sentiment_list.append(0)
    else:
        print("FAILED")

score_list, score_list_geom, xword_list, sentiment_list = zip(*sorted(zip(score_list, score_list_geom, xword_list, sentiment_list), key=lambda x: x[1]))
print(score_list)
for i in range(n_puzzles):
    print("---")
    try:
        xword_list[i].draw_crossword()
        print(xword_list[i], score_list[i], score_list_geom[i], sentiment_list[i])
    except:
        print(None)
Timer.outputAll()
