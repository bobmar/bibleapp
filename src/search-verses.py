import sys
import json
from pkg.repo import obj_repo
from pkg.util import bible_parm

words = sys.argv[1:]
parm = bible_parm.Parm().get_parm()
repo = obj_repo.ObjectRepo()

def construct_query(words):
    query = []
    for word in words:
        crit = {'word': word.upper()}
        query.append(crit)
    or_stmt = {'$or': query}
    return or_stmt

def find_verse_text(verse_ref):
    verse_text = None
    chapter = repo.find_by_query(parm['chapterCollection'], {'_id': verse_ref['chapterId']}, {'_id':1})
    for item in chapter:
        for verse in item['verses']:
            if verse_ref['verseNumber'] == verse['verseNum']:
                verse_text = verse['verse']
    return verse_text

def process_results(search_results):
    search_result = {}

    for item in search_results:
        search_result['translation_id'] = item['translationId']
        search_result['word'] = item['word']
        print(json.dumps(search_result, indent=4))
        for verse in item['verses']:
            verse_text = find_verse_text(verse)
            if verse_text is not None:
                verse['verse_text'] = verse_text
                verse['word'] = item['word']
                print(json.dumps(verse, indent=4))
            else:
                print('Verse not found for ', verse['chapterId'], verse['verseNum'])


print(words)
result = repo.find_by_query(parm['referenceCollection'], construct_query(words), {'word':1})
process_results(result)