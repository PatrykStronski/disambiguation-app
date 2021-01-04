import spacy

class Lemmatizer:
    nlp = None
    def __init__(self):
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_pl = spacy.load("pl_core_news_sm")

    def lemmatize_pl(self, text):
        doc = self.nlp_pl(text)
        return [token.lemma_ for token in doc]

    def lemmatize_en(self, text):
        doc = self.nlp_en(text)
        return [token.lemma_ for token in doc]

    def lemmatize(self, text, language):
        if language == "polish":
            return self.lemmatize_pl(text)
        return self.lemmatize_en(text)