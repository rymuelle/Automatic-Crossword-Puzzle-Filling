# loop over '/Users/ryanmueller/Downloads/xd/clues.tsv'
# https://xd.saul.pw/data
import os

pathname = os.path.dirname(os.path.abspath(__file__)) + "/"

def make_clue_dict(file='wordlists/clues.tsv'):
    clue_dict = {}
    with open(pathname + file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 4:
                pub = parts[0]
                year = parts[1]
                answer = parts[2]
                clue = parts[3] 
                try:
                    year = int(year)
                except:
                    year = 0
                # Keep most recent clue
                if answer in clue_dict:
                    if year > clue_dict[answer][1]:
                        clue_dict[answer] = (clue, year, pub)
                else:
                    clue_dict[answer] = (clue, year, pub)
    return clue_dict



def read_clue_csv():
    clue_dict = {}
    with open(pathname + 'wordlists/clues.csv', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                pub = parts[3]
                year = parts[2]
                answer = parts[0]
                clue = parts[1] 
                try:
                    year = int(year)
                except:
                    year = 0
                # Keep most recent clue
                if answer in clue_dict:
                    if year > clue_dict[answer][1]:
                        clue_dict[answer] = (clue, year, pub)
                else:
                    clue_dict[answer] = (clue, year, pub)
    return clue_dict

if __name__ == "__main__":
    # import pandas as pd
    clue_dict = make_clue_dict()
    with open(pathname + 'wordlists/clues_short.tsv', 'w') as f:
        for answer, (clue, year, pub) in clue_dict.items():
            f.write('{}\t{}\t{}\t{}\n'.format(pub, year, answer, clue))

