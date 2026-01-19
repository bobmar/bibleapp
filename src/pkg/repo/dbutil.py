from pymongo import MongoClient
from pkg.util import bible_parm as parm


def open_db():
    bible_parm = parm.Parm().get_parm()
    try:
        client = MongoClient(bible_parm["url"])
        return client.bible
    except:
        return None


class CommonMongo:
    def __init__(self):
        self._db = open_db()

    def getclient(self):
        return self._db

common_db = CommonMongo()


def get_client():
    return common_db.getclient()