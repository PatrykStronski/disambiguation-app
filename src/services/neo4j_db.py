from neo4j import GraphDatabase

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
        result = self.session.run("MATCH (start:Resource {uri: '" + node + "'})-[rel1]-(second: Resource {uri: '" + node2 + "'}), connections_second=(second)-[rel2]-(third: Resource), triangle_connections=(third)-[rel3]-(start) RETURN COUNT(triangle_connections) AS cardinality")
        return [record["cardinality"] for record in result][0] + 1

    def get_related_nodes(self, node):
        result = self.session.run("MATCH (n {uri: '" + node + "'}) -[r]- (b) RETURN b AS resource, r AS relation")
        return [(record["resource"], record["relation"]) for record in result]

    def get_number_of_nodes(self):
        result = self.session.run("MATCH (n:Resource) RETURN COUNT(n) AS qty")
        return [record["qty"] for record in result][0]

    def get_node_by_index(self, ind):
        result = self.session.run("MATCH (n:Resource) RETURN n AS resource SKIP " + str(ind) + " LIMIT 1")
        return [record["resource"] for record in result][0]

    def get_uri_single_node(self, node):
        return node["uri"]

    def get_label_single_node(self, node):
        return node["rdfs__label"]

    def __del__(self):
        self.session.close()
        self.driver.close()
