from crossword import Crossword
from abc import ABC, abstractmethod
import time
import random

from scoring import *
# Get current pathname
import os
pathname = os.path.dirname(os.path.abspath(__file__)) + "/"

class ConstructionAlgorithm(ABC):
    @staticmethod
    @abstractmethod
    def construct(rows, cols, empty_grid, word_list, params = {}):
        pass

    @staticmethod
    @abstractmethod
    def checkValid(crossword, word_list):
        pass

    @staticmethod
    @abstractmethod
    def readWordList(word_list_file):
        pass


class IntelligentLookahead(ConstructionAlgorithm):

    """
    IDEA: Store a list of words that could fit in each word space. Add words
    to the word space with the fewest options. If there are no options, remove
    the last added word. As you add words, update the list of words available
    for each word space.

    Despite this, this algorithm, with a sufficient wordlist, can quickly
    solve a 15x15 with ample shaded squares.
    """
    def _matches(dict_word, grid_word):
        """
        Take a dict_word: a word
        Take a grid_word: spaces for blanks, and letters for letters
        return true if the word `fits` given the letters
        """
        for i in range(len(grid_word)):
            dict_char = dict_word[i].upper()
            grid_char = grid_word[i].upper()
            if grid_char != dict_char and grid_char != ' ':
                return False

        return True

    def _buildGridDict(word_list_dict, xword):
        grid_words_dict = {}
        acrosses = xword.getAcrosses()
        # make across dictionaries
        for i, grid_word in enumerate(acrosses):
            curr_tup = (i, 'A')
            # get all words of length of current across saved at curr_tup index
            try:
                fitting_words = [dict_word for dict_word in word_list_dict[len(grid_word)]
                                    if IntelligentLookahead._matches(dict_word, grid_word)]
            except:
                # if there are no words of that length
                fitting_words = []
            if len(fitting_words) == 0 and ' ' not in grid_word:
                fitting_words.append(grid_word)
            elif len(fitting_words) == 0:
                return False
            grid_words_dict[curr_tup] = []
            grid_words_dict[curr_tup].append(set(fitting_words))

        downs = xword.getDowns()
        # make down dictionaries
        for i, grid_word in enumerate(downs):
            curr_tup = (i, 'D')
            # get all words of length of current down saved at curr_tup index
            try:
                fitting_words = [dict_word for dict_word in word_list_dict[len(grid_word)]
                                    if IntelligentLookahead._matches(dict_word, grid_word)]
            except:
                # if there are no words of that length
                fitting_words = []
            if len(fitting_words) == 0 and ' ' not in grid_word:
                fitting_words.append(grid_word)
            elif len(fitting_words) == 0:
                return False
            grid_words_dict[curr_tup] = []
            grid_words_dict[curr_tup].append(set(fitting_words))
        return grid_words_dict

    def _update_coords(coords, fixing_dir):
        """
        Given a tuple of coords, and a fixing direction A/D
        Return coordinates that move one character in the direction of the
        fixing direction
        """
        if (fixing_dir == 'D'):
            coords = (coords[0], coords[1] + 1, coords[2])
        elif (fixing_dir == 'A'):
            coords = (coords[0] + 1, coords[1], coords[2])
        return coords

    def _get_intersecting_spaces(xword, curr_fewest_tup, word):
        """
        Return a list of tuples that are keys for the grid_words_dict
        given a word tuple
        """
        intersecting_spaces = []

        word_index_to_coords = xword.getWordIndexToCoords()
        position_index_dict = xword.getPositionIndexDict()
        # get the starting coordinates (in (r, c) form), of the recently added word
        coords = word_index_to_coords[curr_fewest_tup]
        if (curr_fewest_tup[1] == 'A'):
            fixing_dir = 'D'
        elif (curr_fewest_tup[1] == 'D'):
            fixing_dir = 'A'
        coords += (fixing_dir,)

        # for each inserted char in the word, update the intersecting word's wordlist
        for i in range(len(word)):
            # get the index of the intersecting word
            fixing_dir_index = position_index_dict[coords][0]
            # get the character index of this (r,c) of the opposite direction word

            fixing_tup = (fixing_dir_index, fixing_dir)
            intersecting_spaces.append(fixing_tup)

            # update coords to go to the next character
            coords = IntelligentLookahead._update_coords(coords, fixing_dir)
        return intersecting_spaces

    def _findSmallestSet(grid_words_dict, tup_stack):
        """
        Take in the current list of words available for each word space and
        looks through each of the word lists (for any words not yet
        inserted).
        Return the tuple of the word with the fewest options.
        If all of the tuples have been inserted, return -1
        """
        min_amount = -1
        for key in grid_words_dict:
            if key not in tup_stack:
                if (len(grid_words_dict[key][-1]) < min_amount) or (min_amount == -1):
                    # curr_fewest_tup will be a tuple (ind, A/D)
                    curr_fewest_tup = key
                    min_amount = len(grid_words_dict[key][-1])
        if min_amount == -1:
            return -1
        return curr_fewest_tup

    def _updateGridDictAddWord(grid_words_dict, xword, curr_fewest_tup, word):
        word_index_to_coords = xword.getWordIndexToCoords()
        position_index_dict = xword.getPositionIndexDict()
        # get the starting coordinates (in (r, c) form), of the recently added word
        coords = word_index_to_coords[curr_fewest_tup]
        if (curr_fewest_tup[1] == 'A'):
            fixing_dir = 'D'
        elif (curr_fewest_tup[1] == 'D'):
            fixing_dir = 'A'
        coords += (fixing_dir,)

        intersecting_spaces = IntelligentLookahead._get_intersecting_spaces(xword, curr_fewest_tup, word)

        # for each inserted char in the word, update the intersecting word's wordlist
        for i in range(len(intersecting_spaces)):
            fixing_tup = intersecting_spaces[i]
            words_still_valid = set()
            fixing_char_num = position_index_dict[coords][1]

            # Loop through the "active" word list
            for list_word in grid_words_dict[fixing_tup][-1]:
                # remove every word in the list if the character that was added
                # doesn't match the character at that spot in the list
                if list_word[fixing_char_num] == word[i] and list_word != word:
                    words_still_valid.add(list_word)
            # push onto the stack the new set of valid words
            grid_words_dict[fixing_tup].append(words_still_valid)
            coords = IntelligentLookahead._update_coords(coords, fixing_dir)

        return grid_words_dict

    def _updateGridDictRemoveWord(grid_words_dict, xword, removed_word_tup, removed_word):
        word_index_to_coords = xword.getWordIndexToCoords()
        position_index_dict = xword.getPositionIndexDict()
        # get the starting coordinates (in (r, c) form), of the recently removed word
        coords = word_index_to_coords[removed_word_tup]
        if (removed_word_tup[1] == 'A'):
            fixing_dir = 'D'
        elif (removed_word_tup[1] == 'D'):
            fixing_dir = 'A'
        coords += (fixing_dir,)

        # for each inserted letter in the word, update the intersecting word's wordlist
        for i in range(len(removed_word)):
            # get the opposite direction word's index
            fixing_dir_index = position_index_dict[coords][0]
            fixing_tup = (fixing_dir_index, fixing_dir)
            # pop the last wordlist off the stack
            grid_words_dict[fixing_tup].pop()
            # increment the coordinates to be the next letter
            coords = IntelligentLookahead._update_coords(coords, fixing_dir)

        return grid_words_dict

    def construct(rows, cols, empty_grid, word_list_dict, score_dict, sentiment = None, MAX_TIME = 10):
        start_time = time.time()
        # make the crossword out of the empty grid
        xword = Crossword(rows, cols, empty_grid)
        
        # for each across/down word, make a list of words that could fit there
        # this will be a dictionary:
        #   Keys will be a tuple, index of word and A/D
        #   Values will be a STACK of sets of words
        # if grid_words_dict is False, then it won't be able to fill
        grid_words_dict = IntelligentLookahead._buildGridDict(word_list_dict, xword)
        if not grid_words_dict:
            return False, xword

        # this list is a stack that keeps track of which words have been
        # inserted in what order
        tup_stack = []
        num_words = len(xword.getWords())

        while len(tup_stack) != num_words:
            # if the program is taking longer than MAX_TIME, quit
            if time.time() - start_time > MAX_TIME:
                print("Exceeded time limit")
                return False, xword

            # find the word with the fewest options that hasn't yet been filled in
            curr_fewest_tup = IntelligentLookahead._findSmallestSet(grid_words_dict, tup_stack)

            # if curr_fewest_tup is -1, then all of the tuples are in tup_stack
            if curr_fewest_tup == -1:
                min_amount = -1
            else:
                min_amount = len(grid_words_dict[curr_fewest_tup][-1])

            # if min_amount IS -1, that means that the grid is filled in well
            if min_amount > 0:
                tup_stack.append(curr_fewest_tup)
                smallest_set = grid_words_dict[curr_fewest_tup][-1]
                # get a random word from the set and remove it from the set
                scores = [score_word(s, score_dict, sentiment=sentiment) for s in smallest_set]
                # word = choice(list(smallest_set))
                try:
                    word = random.choices(list(smallest_set), weights=scores, k=1)[0]
                except:
                    print(scores, word)
                    test
                grid_words_dict[curr_fewest_tup][-1].remove(word)

                xword.addWord(curr_fewest_tup, word)
                IntelligentLookahead._updateGridDictAddWord(grid_words_dict, xword, curr_fewest_tup, word)

            # if min_amount == 0, then the last insert forced a collision, so remove the last word
            elif min_amount == 0:
                # if the list is empty, that means we've tried every path
                if len(tup_stack) == 0:
                    return False, xword
                removed_word_tup = tup_stack.pop()
                removed_word = xword.removeWord(removed_word_tup)
                IntelligentLookahead._updateGridDictRemoveWord(grid_words_dict, xword, removed_word_tup, removed_word)

            # print(xword)
            # print("--------")
        # print("FOUND:")
        # print(xword)

        # double check that all inserted words are valid
        for word in xword.getWords():
            if word not in word_list_dict[len(word)]:
                print("THAT'S NOT A WORD:", word)

        return True, xword

    def readWordList(word_list_file):
        # returns a dictionary with:
        # key as len and value as a list of uppercase words of that len
        word_list_dict = {}

        with open(pathname + 'wordlists/' + word_list_file) as my_file:
            for line in my_file:
                line = line.strip()
                word, score = line.split(';')
                try:
                    word_list_dict[len(word)].append(word.upper())
                except KeyError:
                    word_list_dict[len(word)] = []
                    word_list_dict[len(word)].append(word.upper())
        return word_list_dict



    
