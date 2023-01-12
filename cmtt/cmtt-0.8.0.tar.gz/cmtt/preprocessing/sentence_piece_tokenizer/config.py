class LanguageCodes:
    hindi = 'hi'
    hinglish = 'hi-en'
    english = 'en'
    hinDev_engRom = 'hinDev_engRom'

    def get_all_language_codes(self):
        return [self.hindi, self.hinglish, self.english, self.hinDev_engRom]


class LMConfigs:
    all_language_codes = LanguageCodes()
    tokenizer_model_file_id = {
        all_language_codes.hindi: '1rtHpZjR65JyF6Km43Me_07uJDsDGmJUq',
        all_language_codes.hinglish: '1rKQufGrxZ881yHry7B4vPGJlC83wyjTT',
        all_language_codes.english: '1Cz1LSYjebfR11cNxjUyeBbEfvFF1znJ8',
        all_language_codes.hinDev_engRom: '1EPNWOPzH4PVWQlg6KgnVbQ9INZ7DN7eX',
        # all_language_codes.hindi: 'https://www.dropbox.com/s/5p19jcd4jlzf6r1/hindi_tokenizer.model?dl=0',
        # all_language_codes.hinglish: 'https://www.dropbox.com/s/j5itqvse5u77urs/hinglish_tokenizer.model?dl=0',
        # all_language_codes.english: 'https://www.dropbox.com/s/kpks31yovdhc20l/english_tokenizer.model?dl=0',
    }

    def __init__(self, language_code: str):
        self.language_code = language_code

    def get_config(self):
        return {
            'tokenizer_model_id': self.tokenizer_model_file_id[self.language_code],
            'tokenizer_model_file_name': 'tokenizer.model'
        }