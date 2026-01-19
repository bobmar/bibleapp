class WordStore:
    def __init__(self):
        self.word_xref = {}
        self.total_words = 0

    def add_words(self, word_str, chapter_id, verse_number):
        added_count = 0
        for word in word_str.split():
            self.total_words += 1
            if not word in self.word_xref.keys():
                self.word_xref[word] = {}
            verse_key = chapter_id + ':' + str(verse_number)
            verse_ref = {'verseKey': verse_key, 'chapterId': chapter_id, 'verseNumber': verse_number}
            if verse_key not in self.word_xref[word]:
                self.word_xref[word][verse_key] = verse_ref
            added_count += 1
        return added_count

    def get_total_words(self):
        return self.total_words

    def get_word_xref(self):
        return self.word_xref