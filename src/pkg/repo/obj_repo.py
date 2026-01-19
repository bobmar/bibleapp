from pkg.repo import dbutil

class ObjectRepo:
    def __init__(self):
        self._db = dbutil.get_client()

    def check_exists(self, collection, pk):
        doc_cnt = self._db[collection].count_documents({'_id': pk})
        return doc_cnt > 0

    def save_document(self, collection, document):
        return self._db[collection].insert_one(document)

    def update_document(self, collection, criteria, document):
        return self._db[collection].update_one(criteria, {'$set': document}, upsert=True)

    def find_all(self, collection):
        return self._db[collection].find()

    def find_by_query(self, collection, query, sort):
        return self._db[collection].find(query).sort(sort)