import json

class BibleTranslation:
    translation_list = []
    output_file = 'translations.json'
    def __init__(self):
        pass

    def add_translation(self, translation_id, translation_name):
        translation_dict = {'translationId': translation_id, 'translationName': translation_name}
        self.translation_list.append(translation_dict)
        print('Added', translation_id, translation_name)

    def save_translations(self, base_dir):
        with open(base_dir + '/' + self.output_file, 'w') as json_file:
            json.dump(self.translation_list, json_file)
            json_file.close()
        print('Saved', len(self.translation_list), 'translations')
