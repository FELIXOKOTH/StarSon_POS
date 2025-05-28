from googletrans import Translator

def translate_message(msg, lang_code='sw'):
    translator = Translator()
    translated = translator.translate(msg, dest=lang_code)
    return translated.text

print(translate_message('Welcome to StarSon POS', 'sw'))
