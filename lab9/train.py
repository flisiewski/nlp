import os, json, pickle

import regex
from tqdm import tqdm

word_pattern = "\p{Letter}+"
DATA_DIR = "/run/media/maciej/Nowy/data/json/"


def load_data():
    total_judgments = []
    files = os.listdir(DATA_DIR)

    for file in tqdm(files):
        if file.startswith("judgment"):
            file_path = os.path.join(DATA_DIR, file)

            with open(file_path, 'r') as f:
                data = json.load(f)
                judgments = [x["textContent"] for x in data["items"]]
            total_judgments += judgments

    analyzed_judgments = []

    #     i = 50
    for judgment in tqdm(total_judgments):
        judgment = regex.sub("<.*?>", "", judgment)
        judgment = regex.sub("-\n(\p{Letter}+)", r"\1", judgment)
        judgment = regex.sub("\n", "", judgment)

    return analyzed_judgments


analyzed_judgments = load_data()
