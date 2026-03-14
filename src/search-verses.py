import sys
import json
from pkg.repo import obj_repo
from pkg.util import bible_parm

words = sys.argv[1:]
parm = bible_parm.Parm().get_parm()
repo = obj_repo.ObjectRepo()

def find_verse_text(verse_ref):
    verse_text = None
    chapter = repo.find_by_query(parm['chapterCollection'], {'_id': verse_ref['chapterId']}, {'_id':1})
    for item in chapter:
        for verse in item['verses']:
            if verse_ref['verseNumber'] == verse['verseNum']:
                verse_text = verse['verse']
    return verse_text

def process_results(search_results):
    search_result = {'verses': []}

    for item in search_results:
        search_result['translation_id'] = item['translationId']
        search_result['word'] = item['word']
        print(json.dumps(search_result, indent=4))
        for verse in item['verses']:
            verse_text = find_verse_text(verse)
            if verse_text is not None:
                verse['verse_text'] = verse_text
                search_result['verses'].append(verse)
            else:
                print('Verse not found for ', verse['chapterId'], verse['verseNum'])
    return search_result

def find_common_verses(word_result):
    verse_counts = {}
    for item in word_result:
        for verse in item['verses']:
            if verse['verseKey'] not in verse_counts:
                verse_counts[verse['verseKey']] = 1
            else:
                verse_counts[verse['verseKey']] += 1
    for key, value in verse_counts.items():
        if value > 1:
            print(key)

word_results = []
for word in words:
    v = repo.find_by_query(parm['referenceCollection'], {'word': word.upper()}, {'_id':1})
    for ref in v:
        word_results.append(ref)
find_common_verses(word_results)
print(json.dumps(word_results, indent=4))