from neo4j import GraphDatabase
import json

class Neo4jDb:
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

    def get_triangle_weight(self, node, node2):
        result = self.session.run("MATCH (start:Resource {uri: '" + node + "'})-[rel1]-(second: Resource {uri: '" + node2 + "'}), connections_second=(second)-[rel2]-(third: Resource), triangle_connections=(third: Resource)-[rel3]-(start) RETURN COUNT(triangle_connections) AS cardinality")
        return [record["cardinality"] for record in result][0] + 1

    def get_related_nodes(self, node):
        result = self.session.run("MATCH (n:Resource {uri: '" + node + "'}) -[r]- (b:Resource), (b) -[r2]- (n) RETURN b AS resource, r AS relation, r2 AS relation2")
        return [(record["resource"], (record["relation"], record["relation2"])) for record in result]

    def get_related_nodes_weighted(self, node, language):
        query = "MATCH (n:Resource {uri: '" + node + "'}) -[r]- (b:Resource), (b) -[r2]- (n) OPTIONAL MATCH (b) -- (c: Resource), (c) -[r_triangle]- (n) RETURN b.uri AS node2, r AS relation, r2 AS relation2, COUNT(r_triangle) AS weight"
        if language == "@en":
            query = "MATCH (n:Resource {uri: '" + node + "'})  -[r]- (b:Resource), (b) -[r2]- (n) OPTIONAL MATCH (b) -- (c: Resource), (c) -[r_triangle]- (n) WHERE ANY (x IN b.skos__prefLabel WHERE x CONTAINS '@en') AND ANY (x IN c.skos__prefLabel WHERE x CONTAINS '@en') RETURN b.uri AS node2, r AS relation, r2 AS relation2, COUNT(r_triangle) AS weight"
        elif language == "@pl":
            query = "MATCH (n:Resource {uri: '" + node + "'})  -[r]- (b:Resource), (b) -[r2]- (n) OPTIONAL MATCH (b) -- (c: Resource), (c) -[r_triangle]- (n) WHERE ANY (x IN b.skos__prefLabel WHERE x CONTAINS '@pl') AND ANY (x1 IN c.skos__prefLabel WHERE x1 CONTAINS '@pl') RETURN b.uri AS node2, r AS relation, r2 AS relation2, COUNT(r_triangle) AS weight"
        result = self.session.run(query)
        return [{
            "node1": node,
            "node2": record["node2"],
            "relation": (record["relation"].type, record["relation2"].type),
            "weight": record["weight"] + 1
        } for record in result]

    def get_number_of_nodes(self):
        result = self.session.run("MATCH (n:Resource) RETURN COUNT(n) AS qty")
        return [record["qty"] for record in result][0]

    def get_node_by_index(self, ind):
        result = self.session.run("MATCH (n:Resource) RETURN n.uri AS resource, properties(n) AS properties SKIP " + str(ind) + " LIMIT 1")
        return [(record["resource"], record["properties"] ) for record in result][0]

    def get_uri_single_node(self, node):
        return node["uri"]

    def get_label_single_node(self, node):
        return node["rdfs__label"]

    def compose_props(self, properties):
        props = []
        for prop in properties.keys():
            if type(properties[prop]) == str:
                props.append("n."+prop + "= '" + str(properties[prop]) + "'")
            else:
                props.append("n."+prop + "= " + str(properties[prop]).replace("\\x", "?"))
        separator = ", "
        return separator.join(props)

    def create_node(self, properties):
        props = self.compose_props(properties)
        self.session.run("MERGE (n:Resource {uri: '" + properties["uri"] + "'}) SET " + props)

    def purge(self):
        self.session.run("MATCH (n)-[r]-(b) DELETE r")
        self.session.run("MATCH (n) DELETE n")

    def create_relation(self, node1_uri, node2_uri, relations):
        self.session.run("MATCH (start: Resource {uri: '" + node1_uri + "'}) MERGE (end:Resource {uri: '" + node2_uri + "'}) MERGE  (start)-[:" + relations[0] + "]->(end) MERGE  (end)-[:" + relations[1] + "]->(start) WITH end SET end.inSignatures = COALESCE(end.inSignatures, []) + '" + node1_uri + "'")

    def __del__(self):
        self.session.close()
        self.driver.close()
