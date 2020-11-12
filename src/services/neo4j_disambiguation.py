from neo4j import GraphDatabase

class Neo4jDisambiguation:
    URI = "neo4j://localhost:7687/"
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

    def find_word(self, word):
        result_pref = self.session.run("MATCH (n:Resource) -[r]- (b:Resource) WHERE '" + word + "' IN n.skos__prefLabel RETURN n.uri AS uri, COUNT(r) as deg, n.inSignatures AS sign")
        result_alt = self.session.run("MATCH (n:Resource) -[r]- (b:Resource) WHERE '" + word + "' IN n.skos__altLabel RETURN n.uri AS uri, COUNT(r) as deg, n.inSignatures AS sign")
        res_pref = [{ "uri": record["uri"], "source": "prefLabel", "deg": record["deg"], "sign": record["sign"] } for record in result_pref]
        res_alt = [{ "uri": record["uri"], "source": "altLabel", "deg": record["deg"], "sign": record["sign"] } for record in result_alt]
        return res_alt + res_pref
