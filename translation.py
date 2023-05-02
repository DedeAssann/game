"..."

from translate import Translator
from kivy.app import App


class TranslatedText:
    def __init__(
        self,
        text,
    ):
        # self.language = App.get_running_app().store.get("Language")["value"]
        self._t = Translator(to_lang="fr")
        self.text = self._t.translate(text)
