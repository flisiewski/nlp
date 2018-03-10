from elasticsearch_dsl import analyzer, DocType, Text, Date, Keyword, Nested, InnerDoc

analyzer(
    'my_tokenizer',
    tokenizer="standard",
    filter=["morfologik_stem"],
)


class Judge(InnerDoc):
    first_name = Text(analyzer=analyzer)
    last_name = Text(analyzer=analyzer)


class Judgment(DocType):
    content = Text(analyzer=analyzer)
    judgment_date = Date()
    signature = Keyword()
    judges = Nested(Judge)
