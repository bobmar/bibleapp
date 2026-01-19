import json

class ChapterIO:
    chapter_list = []
    output_file = 'chapters.json'

    def __init__(self):
        pass

    def add_chapter(self, book_key, book_id, chapter_number, number_of_verses):
        chapter = {'chapterKey': book_key + ':' + str(chapter_number), 'bookId': book_id
            , 'chapterNumber': chapter_number, 'numberOfVerses': number_of_verses}
        self.chapter_list.append(chapter)
        return chapter

    def save_chapters(self, base_dir):
        with open(base_dir + '/' + self.output_file, 'w') as outfile:
            json.dump(self.chapter_list, outfile)
        print('Saved', len(self.chapter_list), 'chapters')