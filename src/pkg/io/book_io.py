import json

class Book:
    book_list = []
    output_file = 'books.json'
    def __init__(self):
        pass

    def add_book(self, translation_id, book_id, book_name, book_title, book_sequence, chapterCnt, verseCnt):
        book = {'bookKey': translation_id + ':' + book_id,'bookId': book_id, 'bookName': book_name
                ,'bookTitle': book_title, 'bookSequence': book_sequence, 'chapterCnt': chapterCnt, 'verseCnt': verseCnt}
        self.book_list.append(book)
        print('Added', book['bookKey'])

    def save_books(self, base_dir):
        with open(base_dir + '/' + self.output_file, 'w') as json_file:
            json.dump(self.book_list, json_file)
            json_file.close()
        print('Saved', len(self.book_list), 'books')


