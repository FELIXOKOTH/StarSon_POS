"""
This module provides a hybrid translation service for the StarSon POS system.
It is branded as a capability of the Apillo AI agent.

How it works:
1.  It first checks for manually created translations in the `locales/` directory.
    This is ideal for custom languages or for overriding specific terms.
2.  If a translation is not found locally, it calls the Google Translate API.
3.  It caches all translations to improve performance and reduce API costs.
"""

import os
import json
# Use a try-except block to handle cases where the library isn't installed
try:
    from google.cloud import translate_v2 as translate
except ImportError:
    translate = None

class ApilloTranslator:
    def __init__(self):
        """
        Initializes the Apillo Translator.
        It loads local translations and initializes the Google Translate client.
        """
        self.client = translate.Client() if translate else None
        self.local_translations = self._load_local_translations()
        self.cache = {} # Key: (text_key, lang_code) -> translation

    def _load_local_translations(self):
        """
        Loads all JSON translation files from the 'locales' directory.
        """
        translations = {}
        locales_dir = 'locales'
        if os.path.exists(locales_dir):
            for lang_file in os.listdir(locales_dir):
                if lang_file.endswith('.json'):
                    lang = lang_file.split('.')[0]
                    file_path = os.path.join(locales_dir, lang_file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        translations[lang] = json.load(f)
        return translations

    def get_supported_languages(self):
        """
        Returns a list of all supported languages, both local and a curated list for the API.
        """
        local_langs = {lang: self.local_translations[lang].get("_language_name_", lang) for lang in self.local_translations.keys()}
        
        # Add other languages we want to support via API.
        # The key is the language code, the value is the display name.
        # Kikuyu's code is 'ki'. Google Translate also supports Luo ('luo').
        api_langs = {
            'ki': 'Gikuyu',
            'luo': 'Dholuo'
        }

        # Combine and ensure local names are preferred
        combined_langs = {**api_langs, **local_langs}
        return combined_langs

    def translate(self, text_key, lang_code):
        """
        Translates a given text key into the target language.
        """
        # Default to English if lang_code is invalid
        if not lang_code:
            lang_code = 'en'

        # Check cache first
        if (text_key, lang_code) in self.cache:
            return self.cache[(text_key, lang_code)]

        # 1. Try to find translation in local files (master dictionary)
        if lang_code in self.local_translations and text_key in self.local_translations[lang_code]:
            translation = self.local_translations[lang_code][text_key]
            self.cache[(text_key, lang_code)] = translation
            return translation

        # 2. If not found, fall back to Google Translate API if available
        english_text = self.local_translations.get('en', {}).get(text_key, text_key)
        if self.client and lang_code != 'en':
            try:
                result = self.client.translate(english_text, source_language='en', target_language=lang_code)
                translation = result['translatedText']
                self.cache[(text_key, lang_code)] = translation
                return translation
            except Exception as e:
                print(f"Google Translate API failed for lang '{lang_code}': {e}")
        
        # 3. Fallback to the original English text
        return english_text
