import spacy

class Lemmatizer:
    nlp = None
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def lemmatize_pl(self, text):
        return self.lemmatize_en(text)

    def lemmatize_en(self, text):
        doc = self.nlp(text)
        print(doc)

    def lemmatize(self, text, language):
        if language == "polish":
            return self.lemmatize_pl(text)
        return self.lemmatize_en(text)

    def lemmatize_array(self, text, language):
        pass