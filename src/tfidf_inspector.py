import numpy as np
import pymorphy2
from stop_words import get_stop_words


class TfidfInspector:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.stop_words = get_stop_words('russian')
        self.result = {}

    def lemma(self, word) -> list[str]:
        morph_analyze = self.morph.parse(word.lower())
        return morph_analyze[0].normal_form

    def tfidf(self, k, title_page, texts) -> tuple[float, float]:
        tf = round(title_page.count(k) / len(title_page), 3)

        try:
            idf = round(np.log10(len(texts) / sum([1 for t in texts if k in texts[t] and k not in self.stop_words])), 3)
            return tf, idf
        except ZeroDivisionError:
            return tf, 0.0

    def inspector(self, texts: dict, filename: str) -> dict:

        for k in set(texts[filename]):
            tf, idf = self.tfidf(k, texts[filename], texts)
            self.result.update({k: {"tf": tf, "idf": idf}})

        return dict(sorted(self.result.items(), key=lambda item: item[1]["idf"], reverse=True)[:50])
