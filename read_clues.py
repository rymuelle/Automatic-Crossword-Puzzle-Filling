# loop over '/Users/ryanmueller/Downloads/xd/clues.tsv'
# https://xd.saul.pw/data
def make_clue_dict():
    clue_dict = {}
    with open('wordlists/clues.tsv', 'r') as f:
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
    with open('wordlists/clues.csv', 'r') as f:
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
    import pandas as pd
    clue_dict = make_clue_dict()
    df = pd.DataFrame.from_dict(clue_dict, orient='index', columns=['clue', 'year', 'pub'])
    df.to_csv("wordlists/clues.csv")
    print(df.year.mean())