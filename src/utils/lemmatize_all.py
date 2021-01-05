from utils.lemmatizer import Lemmatizer
from services.neo4j_lemmatizer import Neo4jLemmatizer

class OmniLemmatizer:
    neo4j_mgr = None
    lemmatizer = None

    def __init__(self):
        self.neo4j_mgr = Neo4jLemmatizer()
        self.lemmatizer = Lemmatizer()