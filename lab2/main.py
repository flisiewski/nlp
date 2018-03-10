import json
import os

from tqdm import tqdm
from elasticsearch_dsl import analyzer, DocType, Text, Date, Keyword, Nested, InnerDoc

analyzer(
    'my_tokenizer',
    tokenizer="standard",
    filter=["morfologik_stem"],
)


class Judge(InnerDoc):
    name = Text(analyzer=analyzer)


class Judgment(DocType):
    content = Text(analyzer=analyzer)
    judgment_date = Date()
    signature = Keyword()
    judges = Nested(Judge)


Judge.init()
Judgment.init()

DATA_DIR = "/run/media/maciej/Nowy/data/json/"
CHOSEN_YEAR = str(2011)


def load_data():
    files = os.listdir(DATA_DIR)
    results = []
    for file in tqdm(files):
        if file.startswith("judgment"):
            file_path = os.path.join(DATA_DIR, file)

            with open(file_path, 'r') as f:
                data = json.load(f)
                judgments = [x for x in data["items"] if x["judgmentDate"].startswith(CHOSEN_YEAR)]

            for judgment in judgments:
                Judgment(
                    content=judgment['textContent'],
                    judgment_date=judgment['judgmentDate'],
                    signature=judgment['id'],
                    judge=[Judge(name=judge['name']) for judge in judgment['judges']],
                )
                Judgment.save()

    return results


load_data()
