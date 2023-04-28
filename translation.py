"..."

from translate import Translator
from kivy.app import App


class TranslatedText:
    def __init__(
        self,
        text,
    ):
        self.language = App.get_running_app().store.get("Language")["value"]
        self.t = Translator(to_lang=self.language)
        self.text = self.t.translate(text)
