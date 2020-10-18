from nltk.stem.wordnet import WordNetLemmatizer
from services.neo4j_disambiguation import Neo4jDisambiguation

class Disambiguation:
    text = ''
    neo4j_mgr = None
    def __init__(self, text):
        self.text = text
        self.neo4j_mgr = Neo4jDisambiguation('datbaseuse')

    def find_word(self, word):
        lemmatizer = WordNetLemmatizer()
        word_lemma = lemmatizer.lemmatize(word)
        results = self.neo4j_mgr.find_word(word_lemma)