from sentence_transformers import SentenceTransformer
import numpy as np
from src.crosslift.scoring import *

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(words):
    return model.encode(words, normalize_embeddings=True)

def cosine(a, b):
    return np.dot(a, b)

words = ["FOCUS", "LENS", "EXPOSURE", "SENSOR", "FILM", "CAMERA"]
# words = ["SPACE", "GALAXY", "STAR", "PLANET", "ASTEROID", "COMET"]
words = ["SPACE", "GALAXY", "STAR", "SENSOR", "FILM", "CAMERA"]

vecs = embed(words)

def sentiment_score_word(word, target_words):
    word_vec = embed([word])[0]
    target_vecs = embed(target_words)
    scores = [cosine(word_vec, target_vec) for target_vec in target_vecs]
    return sum(scores)


def self_sentiment_score(words):
    vecs = embed(words)
    similarity = {
        (words[i], words[j]): cosine(vecs[i], vecs[j])
        for i in range(len(words))
        for j in range(i+1, len(words))
    }
    similarity = sorted(similarity.items(), key=lambda x: -x[1])
    # Compute geometric mean
    geo_mean = 1
    for k, v in similarity:
        geo_mean *= v
    geo_mean = geo_mean ** (1 / len(similarity))
    mean = np.mean([v for k, v in similarity])
    return mean, geo_mean, similarity


from src.crosslift.scoring import *
from tqdm import tqdm

if __name__ == "__main__":

    mean, geo_mean, similarity = self_sentiment_score(words)
    print("Combined sentiment score:", round(mean, 3))
    for k, v in similarity:
        print(k, round(v, 3))

    # for word in words:
    #     score = sentiment_score_word(word, ["positive", "negative"])
    #     print(f"Sentiment score for {word}: {round(score, 3)}")

    # word_dict = open_dict('xwordlist.dict')

    # semantic_sring = ""
    # for word, score in tqdm(word_dict.items()):
    #     if score > 90:
    #         semantic_score = sentiment_score_word(word, words)*100
    #     else:
    #         semantic_score = 1
    #     semantic_sring += f"{word};{semantic_score*score}\n"

    # with open(f'{pathname}wordlists/xwordlist_sentiment.dict', 'w') as f: 
    #     f.write(semantic_sring)   