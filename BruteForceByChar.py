from ConstructionAlgorithm import ConstructionAlgorithm
from crossword import Crossword

class BruteForceByChar(ConstructionAlgorithm):

    def _recBruteForceConstruct(curr_let_ind, alphabet, positions, xword, word_list_dict):
        if (curr_let_ind == len(positions)):
            if BruteForceByChar.checkValid(xword, word_list_dict):
                # print("FOUND:")
                # print(xword)
                return True
            else:
                return False
        for i in range(len(alphabet)):
            loc = positions[curr_let_ind]
            char = alphabet[i]
            r = loc[0]
            c = loc[1]
            xword.addLetter(r, c, char)
            if BruteForceByChar._recBruteForceConstruct(curr_let_ind + 1, alphabet, positions, xword, word_list_dict):
                return True
        return False

    """
    Very slow construction algorithm which takes every possible
    permutation of letters that could fit in the crossword and checks to see
    if all of the words are valid
    """
    def construct(rows, cols, empty_grid, word_list):

        # TODO change to whatever
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        xword = Crossword(rows, cols, empty_grid)

        word_list_dict = BruteForceByChar.readWordList(word_list)

        # first assign every empty cell to be the first character in the alphabet
        # save every cell that you assign in a list
        positions = []
        curr_grid = xword.getGrid()
        for r in range(rows):
            for c in range(cols):
                if (curr_grid[r][c] != '.'):
                    positions.append( (r,c) )
        return BruteForceByChar._recBruteForceConstruct(0, alphabet, positions, xword, word_list_dict)

    """
    Helper function to check if a given grid's words are in the word list
    Returns: Boolean True/False
    """
    def checkValid(xword, word_list_dict):
        for word in xword.getAcrosses():
            if word not in word_list_dict[len(word)]:
                return False
        for word in xword.getDowns():
            if word not in word_list_dict[len(word)]:
                return False
        return True

    def readWordList(word_list_file):
        # returns a dictionary with key as len and value as a set of words of that len
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

class BruteForceByWord(ConstructionAlgorithm):
    def _recBruteForceConstruct(curr_word_ind, word_list_dict, xword):
        if (curr_word_ind == len(xword.getAcrosses() )):
            # know that all inserted acrosses are valid so we only check downs
            isValid = BruteForceByWord.checkValid(xword, word_list_dict)
            if isValid:
                # print("FOUND:")
                # print(xword)
                return True
            else:
                # print("--------")
                # print(xword)
                return False
        current_across = xword.getAcrosses()[curr_word_ind]

        try:
            filtered_word_set = word_list_dict[len(current_across)]
        except:
            # if there are were no words available of that length
            return False
        for i in range(len(filtered_word_set)):
            word = word_list_dict[len(current_across)].popleft()
            Timer.start("addAcross")
            xword.addAcross(curr_word_ind, word)
            Timer.stop("addAcross")
            if BruteForceByWord._recBruteForceConstruct(curr_word_ind + 1, word_list_dict, xword):
                return True
            Timer.start("removeAcross")
            xword.removeAcross(curr_word_ind)
            Timer.stop("removeAcross")
            word_list_dict[len(current_across)].append(word)
        return False

    # should be a parent method in ConstructionAlgorithm
    def _shuffleDict(word_list_dict):
        for key in word_list_dict:
            temp_list = list(word_list_dict[key])
            shuffle(temp_list)
            word_list_dict[key] = deque(temp_list)
        return word_list_dict

    def construct(rows, cols, empty_grid, word_list_file):
        Timer.start("readWordList")
        word_list_dict = BruteForceByWord.readWordList(word_list_file)
        Timer.stop("readWordList")
        # shuffle the wordlist
        Timer.start("shuffleDict")
        word_list_dict = BruteForceByWord._shuffleDict(word_list_dict)
        Timer.stop("shuffleDict")
        xword = Crossword(rows, cols, empty_grid)
        return BruteForceByWord._recBruteForceConstruct(0, word_list_dict, xword)

    def checkValid(xword, word_list_dict):
        # removed makes sure none of the downs are the same as any other down/across
        removed = []
        for word in xword.getDowns():
            if word not in word_list_dict[len(word)] or word in removed:
                return False
            else:
                removed.append(word)
        return True

    def readWordList(word_list_file):
        # returns a dictionary with key as len and value as a deque of that len
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