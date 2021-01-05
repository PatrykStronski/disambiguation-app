import spacy

#spacy.prefer_gpu()

class Lemmatizer:
    nlp_en = None
    nlp_pl = None

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

    def lemmatize_detect_language(self, word):
        if word.endswith("@en"):
            return " ".join(self.lemmatize_en(word[:-3]))+"@en"
        elif word.endswith("@pl"):
            return " ".join(self.lemmatize_pl(word[:-3]))+"@pl"
        return word

    def lemmatize_labels(self, label_list = []):
        return [self.lemmatize_detect_language(word) for word in label_list]