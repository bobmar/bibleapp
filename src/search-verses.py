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


def find_common_verses(word_result, word_count):
    verse_counts = {}
    common_verses = []
    #count occurrences of word match
    for item in word_result:
        for verse in item['verses']:
            if verse['verseKey'] not in verse_counts:
                verse_counts[verse['verseKey']] = verse.copy()
                verse_counts[verse['verseKey']]['count'] = 1
            else:
                verse_counts[verse['verseKey']]['count'] += 1
    for key, value in verse_counts.items():
        if value['count'] >= word_count:
            value['verseText'] = find_verse_text(value)
            common_verses.append(value)
    return common_verses


word_results = []
for word in words:
    v = repo.find_by_query(parm['referenceCollection'], {'word': word.upper()}, {'_id':1})
    for ref in v:
        word_results.append(ref)


result_obj = {'words': words, 'commonVerses': find_common_verses(word_results, len(words)), 'wordResults': word_results}
print(json.dumps(result_obj, indent=4))