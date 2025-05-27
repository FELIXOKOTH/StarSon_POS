import json
import os

class LanguageSwitcher:
    def __init__(self, language='en', lang_dir='../languages'):
        self.language = language
        self.lang_dir = lang_dir
        self.translations = {}
        self.load_language()

    def load_language(self):
        try:
            with open(os.path.join(self.lang_dir, f"{self.language}.json"), "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            print(f"Language file {self.language}.json not found.")
            self.translations = {}

    def set_language(self, language_code):
        self.language = language_code
        self.load_language()

    def get(self, key):
        return self.translations.get(key, key)
