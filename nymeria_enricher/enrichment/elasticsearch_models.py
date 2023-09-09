from datetime import datetime
from elasticsearch_dsl import Document, Date, Keyword, Text

class NymeriaRawCandidate(Document):
    source = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    date_created = Date(default_timezone='UTC')

    class Index:
        name = 'nymeria_raw_candidates'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        #self.lines = len(self.body.split())
        return super(NymeriaRawCandidate, self).save(** kwargs)

    def is_published(self):
        return datetime.now() > self.date_created