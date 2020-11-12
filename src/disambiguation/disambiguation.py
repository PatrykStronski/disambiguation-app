import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from services.neo4j_disambiguation import Neo4jDisambiguation
import re
import pandas as pd

LANGUAGE_ALIAS = {
    "polish": "@pl",
    "english": "@en"
}

DISAMBIGUATION_THRESHOLD = 0.0
TOP = 5
USE_FALLBACK = True

class Disambiguation:
    neo4j_mgr = None
    lemmatizer = WordNetLemmatizer()

    def __init__(self):
        nltk.download('wordnet')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('pl196x')
        self.neo4j_mgr = Neo4jDisambiguation('databaseuse')

    def filter_candidates(self, tokens):
        for index, token in tokens.iterrows():
            candidates = sorted(token[2], key=lambda cand: cand["score"])[:TOP]
            token[2] = candidates
            #filter(lambda cand: cand["score"] > DISAMBIGUATION_THRESHOLD, candidates)


    def calculate_w(self, v_uri, word, tokens):
        count_relations = 0
        words_number = tokens.shape[0]
        for index, token in tokens.iterrows():
            if token[1] == word:
                continue
            candidates = token[2]
            for cand in candidates:
                if cand["sign"] == None:
                    continue
                if v_uri in cand["sign"]:
                    count_relations += 1
        if USE_FALLBACK and count_relations == 0:
            count_relations = 0.1
        return count_relations/words_number

    def calculate_score(self, tokens):
        for index, token in tokens.iterrows():
            candidates = token[2]
            word = token[1]
            for cand in candidates:
                cand["score"] = cand["deg"]*self.calculate_w(cand["uri"], word, tokens)


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
        tokens = pd.DataFrame([{ "word": w } for w in re.split(r'\W+', text)])
        tokens["basic_form"] = self.basify_words(tokens["word"], lang)
        tokens["candidates"] = [self.neo4j_mgr.find_word(word) for word in tokens["basic_form"]]
        self.calculate_score(tokens)
        self.filter_candidates(tokens)
        return {
            "data": tokens.to_dict('records')
        }