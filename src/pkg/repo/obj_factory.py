import datetime


def create_translation(translation):
    return {'_id': translation['id'], 'translationName': translation['name'], 'numberOfBooks': translation['numberOfBooks'],
        'numberOfVerses': translation['totalNumberOfVerses'], 'createdAt': datetime.datetime.now()}, translation['id']


def create_book(book):
    book_key = book['translationId'] + ':' + book['id']
    return {'_id': book_key, 'translationId': book['translationId'], 'bookId': book['id'], 'bookName': book['name']
        , 'bookTitle': book['title'], 'bookSequence': book['order'], 'chapterCnt': book['numberOfChapters']
        , 'verseCnt': book['totalNumberOfVerses'], 'createdAt': datetime.datetime.now()}, book_key


def create_chapter(chapter):
    chapter_key = chapter['book']['translationId'] + ':' + chapter['book']['id'] + ':' + str(chapter['chapter']['number'])
    return {'_id': chapter_key, 'bookId': chapter['book']['id'], 'translationId': chapter['book']['translationId']
        , 'chapterNumber': chapter['chapter']['number'], 'numberOfVerses': chapter['numberOfVerses']
        , 'createdAt': datetime.datetime.now()}, chapter_key

def create_reference(reference):
    reference_key = reference['translationId'] + ':' + reference['word']
    return {'_id': reference_key, 'translationId': reference['translationId'], 'word': reference['word']
        , 'verses': reference['verses']}, reference_key