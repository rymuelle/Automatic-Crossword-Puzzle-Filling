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
                clue_dict[answer] = (clue, year,pub)
    return clue_dict

if __name__ == "__main__":
    import pandas as pd
    clue_dict = make_clue_dict()
    df = pd.DataFrame.from_dict(clue_dict, orient='index', columns=['clue', 'year', 'pub'])
    print(df.pub.unique())