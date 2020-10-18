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
        result_pref = self.session.run("MATCH (n:Resource) WHERE " + word + " IN n.skos__prefLabel RETURN n.uri")
        result_alt = self.session.run("MATCH (n:Resource) WHERE " + word + " IN n.skos__altLabel RETURN n.uri")
        return result_alt + result_pref
