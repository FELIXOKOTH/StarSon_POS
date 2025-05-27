import tkinter as tk
from translator import CachedTranslator

class LanguagePanel:
    def __init__(self, root):
        self.translator = CachedTranslator()
        self.root = root
        self.root.title("Language Selector")
        self.root.geometry("300x200")

        tk.Label(root, text="Choose Language:").pack(pady=10)
        self.languages = {
            "English": "en",
            "French": "fr",
            "Spanish": "es",
            "Swahili": "sw"
        }

        self.var = tk.StringVar(value="English")
        for lang in self.languages:
            tk.Radiobutton(root, text=lang, variable=self.var, value=lang).pack()

        tk.Button(root, text="Apply", command=self.apply_lang).pack(pady=10)
        self.output = tk.Label(root, text="", wraplength=250)
        self.output.pack()

    def apply_lang(self):
        lang_code = self.languages[self.var.get()]
        self.translator.set_language(lang_code)
        translated = self.translator.translate_text("Welcome to StarSon POS")
        self.output.config(text=translated)

if __name__ == "__main__":
    root = tk.Tk()
    LanguagePanel(root)
    root.mainloop()
