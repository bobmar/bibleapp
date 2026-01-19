import os
import json
import re
from pkg.io import translation_io as trans
from pkg.io import book_io as bookio
from pkg.io import chapter_io as chapio
from pkg.repo import obj_repo as objrepo
from pkg.util import bible_parm as parm
from pkg.repo import obj_factory

bible_parm = parm.Parm().get_parm()
bible_base_dir = bible_parm['bibleBaseDir'] #'/Users/rober/workspace/bible'
bible_api_dir = bible_base_dir + bible_parm['bibleApiDir'] #'/test-api'
bible_output_dir = bible_base_dir + bible_parm['bibleOutputDir'] #'/output'
book_collection = bible_parm['bookCollection']
translation_coll = bible_parm['translationCollection']
chapter_coll = bible_parm['chapterCollection']
content_type_list = []
verse_type_list = []
trans_io = trans.BibleTranslation()
book_io = bookio.Book()
chapter_io = chapio.ChapterIO()
object_repo = objrepo.ObjectRepo()


def prefix_verse_text(verse_line_cnt, verse_str, verse_str_list):
    if verse_line_cnt > 1:
        verse_str = ' ' + verse_str
    verse_str_list.append(verse_str)


def display_verse(verse_list):
    verse_str_list = []
    verse_line_cnt = 0
    for verse in verse_list:
        verse_line_cnt += 1
        verse_type = type(verse)
        if verse_type is not str and verse_type not in verse_type_list:
            verse_type_list.append(verse_type)
            print(verse_type)
        if verse_type is dict and 'text' in verse.keys():
            verse_str = re.sub(r'[^\x00-\x7F]', '', verse['text'])
            prefix_verse_text(verse_line_cnt, verse_str, verse_str_list)
        else:
            if verse_type is str:
                verse_str = re.sub(r'[^\x00-\x7F]','', verse)
                prefix_verse_text(verse_line_cnt, verse_str, verse_str_list)
            else:
                print(verse_type, verse)
    return ''.join(verse_str_list)

def retrieve_verses(chapter):
    verse_list = []
    for verse in chapter['chapter']['content']:
        verse_str = None
        if verse['type'] == 'verse':
            content_type = type(verse['content'])
            if content_type not in content_type_list:
                content_type_list.append(content_type)
            if content_type is list:
                verse_str = display_verse(verse['content'])
            else:
                print(chapter['translation']['name'], chapter['book']['translationId'], chapter['book']['id'], chapter['chapter']['number'],verse['number'], verse['content'], content_type)
            if verse_str is not None:
                verse_list.append({'verseNum': verse['number'], 'verse': verse_str})
    return verse_list


def display_chapter(chapter):
    chapter_doc, chapter_key = obj_factory.create_chapter(chapter)
    pk = {'_id': chapter_key}
    verse_list = retrieve_verses(chapter)
    chapter_doc['verses'] = verse_list
    object_repo.update_document(chapter_coll, pk, chapter_doc)

def get_next_chapter(chapter):
    return chapter['nextChapterApiLink']

def get_chapter(chapter_link):
    with open(chapter_link, encoding='utf-8') as chap_file:
        chapter = json.load(chap_file)
    return chapter

def scan_chapters(book):
    chapter = get_chapter(bible_base_dir + book['firstChapterApiLink'])
    chapter_link = get_next_chapter(chapter)
    while chapter_link is not None:
        print(chapter['thisChapterLink'])
        display_chapter(chapter)
        chapter_link = get_next_chapter(chapter)
        if chapter_link is not None:
            chapter = get_chapter(bible_base_dir + '/' + chapter_link)

def scan_books(translation_dir):
    print(translation_dir)
    with open(translation_dir + '/books.json', 'r') as f:
        books = json.load(f)
        doc, doc_key = obj_factory.create_translation(books['translation'])
        pk = {'_id': doc_key}
        del doc['_id']
        object_repo.update_document(translation_coll, pk, doc)
    for book in books['books']:
        doc, doc_key = obj_factory.create_book(book)
        pk = {'_id': doc_key}
        del doc['_id']
        object_repo.update_document(book_collection, pk, doc)
        scan_chapters(book)
try:
    with os.scandir(bible_api_dir) as base_folder:
        for entry in base_folder:
            print(entry.name)
            if entry.is_dir():
                scan_books(entry.path)
except FileNotFoundError:
    print("No such folder")

print('CWD:', os.getcwd())

print("Unique content types:")
for content_typ in content_type_list:
    print(content_typ)

print("Unique verse types:")
for verse_typ in verse_type_list:
    print(verse_typ)
