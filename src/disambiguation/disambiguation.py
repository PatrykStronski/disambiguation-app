import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from services.neo4j_disambiguation import Neo4jDisambiguation

LANGUAGE_ALIAS = {
    "polish": "@pl",
    "english": "@en"
}

class Disambiguation:
    neo4j_mgr = None
    lemmatizer = WordNetLemmatizer()

    def __init__(self):
        nltk.download('wordnet')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('pl196x')
        self.neo4j_mgr = Neo4jDisambiguation('databaseuse')

    def basify_words(self, tokens, lang = "english"):
        tagged = nltk.pos_tag(tokens)
        lemmatized = []
        for word in tagged:
            print(word)
            if word[1].startswith("V"):
                lemmatized.append(self.lemmatizer.lemmatize(word[0].lower() + LANGUAGE_ALIAS[lang], "v"))
            elif word[1].startswith("N"):
                lemmatized.append(self.lemmatizer.lemmatize(word[0].lower() + LANGUAGE_ALIAS[lang]))
            else:
                lemmatized.append(word[0].lower() + LANGUAGE_ALIAS[lang])
        return lemmatized

    def disambiguate_text(self, text, lang): #lang must be 'polish' or 'english'
        tokens = nltk.word_tokenize(text, "english")
        basic_forms = self.basify_words(tokens, "english")
        candidates = [self.neo4j_mgr.find_word(word) for word in basic_forms]
        print(candidates)
        return {
            "data": candidates
        }