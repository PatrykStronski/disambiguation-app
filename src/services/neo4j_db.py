from neo4j import GraphDatabase

class neo4JDb:
    URI = "neo4j://localhost:7687/"
    KNOWLEDGE_BASE = "naivefull"
    self.session = None
    self.driver = None

    def __init__(self):
        self.driver = GraphDatabase.driver(self.URI)
        self.self.session = driver.self.session(database = self.KNOWLEDGE_BASE)

    def get_resource_label(self, label):
        result = self.session.run("MATCH (n:Resource {rdfs__label: '" + label + "'}) -- (b) RETURN n AS resource")
        return [record["resource"] for record in result]

    def get_relation(self, node1, node2):
     result = self.session.run("MATCH (n {id: '" + str(node1.id) + "'}) -[r]- (b {id: '" + str(node2.id) + "'}) RETURN r AS relation")
        relation = [record["relation"] for record in result]
        if (len(relation) == 0):
            return None
        return [record["relation"] for record in result][0]

    def get_triangle_weight(self, node, node2):
        result = self.session.run("MATCH (start:Resource {uri: '" + node.uri + "'})-[rel1]-(second: Resource {uri: '" + node2.uri + "'}), connections_second=(second)-[rel2]-(third: Resource), triangle_connections=(third)-[rel3]-(start) RETURN COUNT(triangle_connections) AS cardinality")
        return [record["cardinality"] for record in result][0]["cardinality"] + 1

    def get_related_nodes_label(self, label):
        result = self.session.run("MATCH (:Resource {rdfs__label: '" + label + "'}) -- (b) RETURN b AS resource")
        return [record["resource"] for record in result]

    def get_related_nodes_uri(self, uri):
        result = self.session.run("MATCH (:Resource {uri: '" + uri + "'}) -- (b) RETURN b AS resource")
        return [record["resource"] for record in result]

    def get_related_nodes(self, node):
        result = self.session.run("MATCH (n {id: '" + str(node.id) + "'}) -- (b) RETURN b AS resource")
        return [record["resource"] for record in result]

    def get_number_of_nodes(self):
        result = self.session.run("MATCH (n:Resource) RETURN COUNT(n) AS qty")
        return [record["qty"] for record in result][0]

    def get_node_by_index(self, ind):
        result = self.session.run("MATCH (n:Resource) RETURN n AS resource SKIP " + str(ind) + " LIMIT 1")
    r   eturn [record["resource"] for record in result][0]

    def get_uri_single_node(self, node):
        return node["uri"]

    def get_label_single_node(self, node):
        return node["rdfs__label"]

    def get_uris(self, nodes):
        return [node["uri"] for node in nodes]

    def get_labels(self, nodes):
        return [node["rdfs__label"] for node in nodes]

    def __del__(self):
        self.session.close()
        self.driver.close()
