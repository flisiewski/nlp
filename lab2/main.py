from elasticsearch_dsl import analyzer, DocType, Text, Date, Keyword

analyzer(
    'my_tokenizer',
    tokenizer="standard",
    filter=["morfologik_stem"],
)


class Judgment(DocType)
    content = Text(analyzer='morfologik')
    judgment_date = Date()
    signature = Keyword()
    judges = List


class Article(DocType):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Meta:
        index = 'blog'

    def save(self, **kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(**kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from
