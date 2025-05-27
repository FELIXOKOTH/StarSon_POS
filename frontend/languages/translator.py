from google.cloud import translate_v2 as translate

class CachedTranslator:
    def __init__(self, target_lang="en"):
        self.target_lang = target_lang
        self.client = translate.Client()
        self.cache = {}  # Key: (text, lang) -> translation

    def translate_text(self, text):
        key = (text.lower(), self.target_lang)
        if key in self.cache:
            return self.cache[key]
        result = self.client.translate(text, target_language=self.target_lang)
        translated = result["translatedText"]
        self.cache[key] = translated
        return translated

    def set_language(self, lang_code):
        self.target_lang = lang_code
