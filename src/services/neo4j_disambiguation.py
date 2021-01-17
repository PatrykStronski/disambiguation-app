from neo4j import GraphDatabase
from config import PHRASE_SEPARATOR
import re

class Neo4jDisambiguation:
    URI = "neo4j://neo_dest:7687/"
    database_name = ""
    session = None
    driver = None

    def __init__(self, database_name):
        self.database_name = database_name
        self.driver = GraphDatabase.driver(self.URI)
        self.session = self.driver.session(database = self.database_name)

    def find_word_labels(self, word, lang):
        print(word + lang)
        if len(word) < 3 or re.match('-.*-', word):
            return []
        if lang == "polish":
            result = self.session.run("MATCH (n:Resource) -[r]-> (b:Resource) WHERE n.labels_polish CONTAINS '" + PHRASE_SEPARATOR + word.lower() + PHRASE_SEPARATOR + "' RETURN n.uri AS uri, COUNT(r) as deg, collect(b.uri) AS sign, n.labels AS prefLabel")
        else:
            result = self.session.run("MATCH (n:Resource) -[r]-> (b:Resource) WHERE n.labels_english CONTAINS '" + PHRASE_SEPARATOR + word.lower() + PHRASE_SEPARATOR + "' RETURN n.uri AS uri, COUNT(r) as deg, collect(b.uri) AS sign, n.labels AS prefLabel")
        return [{ "uri": record["uri"], "deg": record["deg"], "sign": record["sign"], "labels": record["prefLabel"] } for record in result]

    def find_word_labels_weak(self, word, lang):
        print(word + lang)
        if len(word) < 3 or re.match('-.*-', word):
            return []
        if lang == "polish":
            result = self.session.run("MATCH (n:Resource) -[r]-> (b:Resource) WHERE n.labels_polish CONTAINS '" + word.lower() + "' RETURN n.uri AS uri, COUNT(r) as deg, collect(b.uri) AS sign, n.labels AS prefLabel")
        else:
            result = self.session.run("MATCH (n:Resource) -[r]-> (b:Resource) WHERE n.labels_english CONTAINS '" + word.lower() + "' RETURN n.uri AS uri, COUNT(r) as deg, collect(b.uri) AS sign, n.labels AS prefLabel")
        return [{ "uri": record["uri"], "deg": record["deg"], "sign": record["sign"], "labels": record["prefLabel"] } for record in result]
