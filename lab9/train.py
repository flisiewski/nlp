import os, json, pickle

import regex
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from tqdm import tqdm

word_pattern = "\p{Letter}+"
DATA_DIR = "/run/media/maciej/Nowy/data/json/"

import pickle

phrases = Phrases()

import subprocess


def get_sum_data(files):
    sizes = subprocess.check_output(
        'du -s {}'.format(" ".join([file for file in files])),
        shell=True
    ).decode()
    lines = sizes.split("\n")
    tuples = [x.split('\t') for x in lines]
    tuples = [tuple for tuple in tuples if tuple != ['']]
    sizes, _ = zip(*tuples)
    size = sum([int(size) for size in sizes]) / 1024 / 1024
    print(size * 100 // 1)
    return size >= 1.0


def load_data():
    total_judgments = []
    # files = pickle.load(open('files.p', 'rb'))
    files = os.listdir(DATA_DIR)

    analyzed_files = []
    for file in files:
        if file.startswith("judgment"):
            file_path = os.path.join(DATA_DIR, file)

            with open(file_path, 'r') as f:
                data = json.load(f)
                judgments = [x["textContent"] for x in data["items"]]
            total_judgments += judgments
            analyzed_files.append(file_path)

            if get_sum_data(analyzed_files):
                break
    total_words = []

    i = 0
    for judgment in tqdm(total_judgments):
        judgment = regex.sub("<.*?>", "", judgment)
        judgment = regex.sub("-\n(\p{Letter}+)", r"\1", judgment)
        judgment = regex.sub("\n", "", judgment)
        judgment = judgment.lower()

        words = []
        for match in regex.finditer(word_pattern, judgment):
            words += match.captures()

        total_words += words
        i += 1
        if i == 3:
            return total_words


sentence_stream = load_data()

bigrams = Phrases(sentence_stream)
phraser_bigram = Phraser(bigrams)
phraser_bigram.save('bigrams')

trigrams = Phrases(bigrams[sentence_stream])
phraser_trigram = Phraser(trigrams)
phraser_trigram.save('trigrams')
