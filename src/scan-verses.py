import os
import re
from pkg.repo import obj_repo
from pkg.repo import obj_factory
from pkg.util import bible_parm
from pkg.util import word_store

parm = bible_parm.Parm().get_parm()

print('CWD: ', os.getcwd())
doc_repo = obj_repo.ObjectRepo()
translations = doc_repo.find_all(parm['translationCollection'])

def retrieve_books(translation_id):
    crit = {'translationId': translation_id}
    sort = {'bookSequence': 1}
    return doc_repo.find_by_query(parm['bookCollection'], crit, sort)


def retrieve_chapters(book_id, translation_id):
    crit = {'translationId': translation_id, 'bookId': book_id}
    sort = {'chapterNumber': 1}
    return doc_repo.find_by_query(parm['chapterCollection'], crit, sort)

def scrub_word_string(word_string):
    word_string = word_string.upper()
    no_punctuation = re.sub(r'[,;:.()?!]', '', word_string)
    return no_punctuation

def scan_verses(verses, chapter_id, words_obj):
    for verse in verses:
        print(verse['verseNum'], verse['verse'])
        added_count = words_obj.add_words(scrub_word_string(verse['verse']), chapter_id, verse['verseNum'])
        print('Added', added_count, 'words')

for translation in translations:
    print(translation['_id'], translation['translationName'])
    words = word_store.WordStore()
    books = retrieve_books(translation['_id'])
    for book in books:
        print(book['bookSequence'], book['bookName'])
        chapters = retrieve_chapters(book['bookId'], book['translationId'])
        for chapter in chapters:
            print(chapter['translationId'], chapter['bookId'], chapter['chapterNumber'])
            scan_verses(chapter['verses'], chapter['_id'], words)
    reference = {'translationId': translation['_id']}
    word_xref = words.get_word_xref()
    for word in word_xref.keys():
        print('Word:',word)
        reference['word'] = word
        verse_list = []
        for verse in word_xref[word].values():
            verse_list.append(verse)
        reference['verses'] = verse_list
        reference_doc, reference_key = obj_factory.create_reference(reference)
        criteria = {'_id': reference_key}
        doc_repo.update_document(parm['referenceCollection'], criteria, reference_doc)