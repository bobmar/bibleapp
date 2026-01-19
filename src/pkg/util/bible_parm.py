import json
import os

class Parm:
    def __init__(self):
        print(os.getcwd())
        with open("bible-db.json", "r") as bible_parm:
            self.bible_dict = json.load(bible_parm)

    def get_parm(self):
        return self.bible_dict
