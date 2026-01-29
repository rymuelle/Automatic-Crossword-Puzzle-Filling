
import os
import math

pathname = os.path.dirname(os.path.abspath(__file__)) + "/"

def logistic_function(x, scale=1, mean=0.5):
    return 1 / (1 + 10**(-(x-mean)*scale))

def open_dict(wordlist_file, min_score=90):
    word_score_dict = {}
    with open(pathname + 'wordlists/' + wordlist_file) as my_file:
        for line in my_file:
            line = line.strip()
            split = line.split(';')
            if len(split) == 2:
                word, score = split
                if float(score) >= min_score:
                    word_score_dict[word] = float(score)
            else:
                word_score_dict[word] = 100.
        return word_score_dict

def open_local_list(wordlist_file, min_score=90):
    word_dict = {}
    with open(wordlist_file) as my_file:
        for line in my_file:
                line = line.strip()
                split = line.split(';')
                if len(split) == 2:
                    word, score = split
                    word = ''.join(x for x in word if x.isalpha())
                    if float(score) >= min_score:
                        word_dict[word] = float(score)
                else:
                    line = ''.join(x for x in line if x.isalpha())
                    word_dict[line] = 100.
        return word_dict

def score_word(word, score_list_dict, sentiment = None, score_function = lambda x: math.exp(min((x,100)) / 0.5)):
    if sentiment is not None:
        from src.crosslift.sentiment import sentiment_score_word
        sentiment_score = sentiment_score_word(word, sentiment)
    else:
        sentiment_score = 1
         
    if word in score_list_dict:
        score = (score_list_dict[word] + 1)*sentiment_score
        score = score_function(score)
        return score
    return 1


def score_xword(xword, word_score_dict):
        words = xword.getWords()
        score = 0
        n_words = 0
        for word in words:
            if word in word_score_dict:
                score += word_score_dict[word]
                n_words += 1
        return score/n_words 

def score_xword_geometric(xword, word_score_dict):
        words = xword.getWords()
        score = 1
        n_words = 0
        for word in words:
            if word in word_score_dict:
                score *= word_score_dict[word]
                n_words += 1
        return score**(1/n_words)


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



def combine_word_lists(word_list_files, score_multipliers, min_score=70):
    word_score_dict = {}
    word_list_dict = {}
    for word_list_file, score_multipliers in zip(word_list_files, score_multipliers):
        _word_list_dict = open_dict(word_list_file, min_score=min_score)
        for word, score in _word_list_dict.items():
            word_score_dict[word] = score * score_multipliers
            try:
                word_list_dict[len(word)].append(word.upper())
            except KeyError:
                word_list_dict[len(word)] = []
                word_list_dict[len(word)].append(word.upper())
    return word_list_dict, word_score_dict
