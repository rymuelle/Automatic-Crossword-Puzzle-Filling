
import os
import math

pathname = os.path.dirname(os.path.abspath(__file__)) + "/"

def logistic_function(x, scale=1, mean=0.5):
    return 1 / (1 + 10**(-(x-mean)*scale))

def open_dict(wordlist_file, score_function = lambda x: math.exp(x / 1)):
    word_score_dict = {}
    with open(pathname + 'wordlists/' + wordlist_file) as my_file:
        for line in my_file:
            line = line.strip()
            word, score = line.split(';')
            word_score_dict[word] = score_function(float(score))
        return word_score_dict

def score_word(word, score_list_dict):
    if word in score_list_dict:
        return score_list_dict[word] + 1
    return 1

def score_xword(xword, wordlist_file, score_function = lambda x: x):
        word_score_dict = open_dict(wordlist_file, score_function=score_function)
        words = xword.getWords()
        score = 0
        n_words = 0
        for word in words:
            if word in word_score_dict:
                score += word_score_dict[word]
                n_words += 1
        return score/n_words

def score_xword_geometric(xword, wordlist_file, score_function = lambda x: x):
        word_score_dict = open_dict(wordlist_file, score_function=score_function)
        words = xword.getWords()
        score = 1
        n_words = 0
        for word in words:
            if word in word_score_dict:
                score *= word_score_dict[word]
                n_words += 1
        return score**(1/n_words)