from crossword import Crossword
from timer import Timer
from ConstructionAlgorithm import *
from scoring import *
import random
from generate_grid import generate_grid
import copy
# from sentiment import self_sentiment_score

wordlist_file = 'xwordlist.dict'
wordlist_files = ['xwordlist.dict']
score_multipliers =[1]


# xword_list = []
# score_list = []
# score_list_geom = []
# n_inserted_words = []
# sentiment_list = []
row, column = 15, 15
n_words_to_insert = 5
black_fraction=.2



n_puzzles = 10
min_score = 50
while True:
    while True:     
        word_list_dict, word_score_dict = combine_word_lists(wordlist_files, score_multipliers, min_score=min_score)
        key_word_list = [k for k,v in open_dict('pokemon.txt', min_score=min_score).items() if v>=100]
        words_to_insert = random.sample(key_word_list, n_words_to_insert)
        test_grid, _xword = generate_grid(rows=row, cols=column, seed=None, black_fraction=black_fraction, max_length=12, words_to_insert=words_to_insert)
        if test_grid is not None: break
    sentiment = None
    orig_gird = copy.deepcopy(test_grid)
    result, xword = IntelligentLookahead.construct(row, column, test_grid, word_list_dict, word_score_dict, sentiment=sentiment)
    if result:
        print("SUCCESS")
        score = score_xword(xword, word_score_dict)
        score_geom = score_xword_geometric(xword, word_score_dict)
        # xword_list.append(xword)
        # score_list.append(score)
        # score_list_geom.append(score_geom)
        # n_inserted_words.append(n_words_to_insert)
        # # sentiment_list.append(self_sentiment_score(xword.getWords())[0])
        # sentiment_list.append(0)
        break
    else:
        print("FAILED")

xword.draw_crossword()

print(xword, score, score_geom)
print(words_to_insert)
xword = Crossword(row, column, optional_grid=orig_gird)
xword.draw_crossword()
print(xword)
# score_list, score_list_geom, xword_list, sentiment_list, n_inserted_words = zip(*sorted(zip(score_list, score_list_geom, xword_list, sentiment_list, n_inserted_words), key=lambda x: x[4]))
# print(score_list)
# for i in range(n_puzzles):
#     print("---")
#     try:
#         xword_list[i].draw_crossword()
#         print(xword_list[i], score_list[i], score_list_geom[i], sentiment_list[i], n_inserted_words[i])
#     except:
#         print(None)
Timer.outputAll()
