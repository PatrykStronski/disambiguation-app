from neo4j import GraphDatabase
import toolz

class Neo4jDisambiguation:
    URI = "neo4j://neo_dest:7687/"
    database_name = ""
    session = None
    driver = None

    def __init__(self, database_name):
        self.database_name = database_name
        self.driver = GraphDatabase.driver(self.URI)
        self.session = self.driver.session(database = self.database_name)

    def get_relation(self, node1, node2):
        result = self.session.run("MATCH (n {uri: '" + node1 + "'}) -[r]- (b {uri: '" + node2 + "'}) RETURN r AS relation")
        relation = [record["relation"] for record in result]
        return relation

    def find_word_regexp(self, word, lang_tag):
        print(word)
        result_pref = self.session.run("MATCH (n:Resource) -[r]-> (b:Resource) WHERE ANY(x IN n.skos__prefLabel WHERE x =~ '(?i).*\\\\b" + word + "\\\\b.*') RETURN n.uri AS uri, COUNT(r) as deg, collect(b.uri) AS sign, n.skos__prefLabel AS prefLabel")
        result_alt = self.session.run("MATCH (n:Resource) -[r]-> (b:Resource) WHERE ANY(x IN n.skos__altLabel WHERE x =~ '(?i).*\\\\b" + word + "\\\\b.*') RETURN n.uri AS uri, COUNT(r) as deg, collect(b.uri) AS sign, n.skos__prefLabel AS prefLabel")
        result_label = self.session.run("MATCH (n:Resource) -[r]-> (b:Resource) WHERE ANY(x IN n.skos__label WHERE x =~ '(?i).*\\\\b" + word + "\\\\b.*') RETURN n.uri AS uri, COUNT(r) as deg, collect(b.uri) AS sign, n.skos__label AS label")
        res_pref = [{ "uri": record["uri"], "source": "prefLabel", "deg": record["deg"], "sign": record["sign"], "labels": record["prefLabel"] } for record in result_pref]
        res_alt = [{ "uri": record["uri"], "source": "altLabel", "deg": record["deg"], "sign": record["sign"], "labels": record["prefLabel"] } for record in result_alt]
        res_label = [{ "uri": record["uri"], "source": "label", "deg": record["deg"], "sign": record["sign"], "labels": record["label"] } for record in result_label]
        return toolz.unique(res_alt + res_pref + res_label, key=lambda x: x["uri"])
