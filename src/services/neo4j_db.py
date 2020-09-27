from neo4j import GraphDatabase

URI = "neo4j://localhost:7687/"
KNOWLEDGE_BASE = "knowledgebase"
driver = GraphDatabase.driver(URI)
session = driver.session(database = KNOWLEDGE_BASE)

def get_resource_label(label):
    result = session.run("MATCH (n:Resource {rdfs__label: '" + label + "'}) -- (b) RETURN n AS resource")
    return [record["resource"] for record in result]

def get_relation(node1, node2):
    result = session.run("MATCH (n {id: '" + str(node1.id) + "'}) -[r]- (b {id: '" + str(node2.id) + "'}) RETURN r AS relation")
    relation = [record["relation"] for record in result]
    if (len(relation) == 0):
        return {}
    return [record["relation"] for record in result][0]

def get_relation_cardinality(node1, node2):
    cardinality = 0
    result = session.run("MATCH (n {id: '" + str(node1.id) + "'}) -[r]- (b) RETURN COUNT(r) AS cardinality")
    cardinality += [record["cardinality"] for record in result][0]
    result = session.run("MATCH (n {id: '" + str(node2.id) + "'}) -[r]- (b) RETURN COUNT(r) AS cardinality")
    cardinality += [record["cardinality"] for record in result][0]
    return cardinality

def get_cardinality_uri(resource_uri):
    return session.run("MATCH (:Resource {uri: '" + resource_uri + "'}) -[r]- (n) RETURN COUNT(r) AS cardinality")
    return [record["cardinality"] for record in result][0]

def get_cardinality_label(resource_label):
    result = session.run("MATCH (:Resource {rdfs__label: '" + resource_label + "'}) -[r]- (n) RETURN COUNT(r) AS cardinality")
    return [record["cardinality"] for record in result][0]

def get_related_nodes_label(label):
    result = session.run("MATCH (:Resource {rdfs__label: '" + label + "'}) -- (b) RETURN b AS resource")
    return [record["resource"] for record in result]

def get_related_nodes_uri(uri):
    result = session.run("MATCH (:Resource {uri: '" + uri + "'}) -- (b) RETURN b AS resource")
    return [record["resource"] for record in result]

def get_number_of_nodes():
    result = session.run("MATCH (n:Resource) RETURN COUNT(n) AS qty")
    return [record["qty"] for record in result][0]

def get_node_by_index(ind):
    result = session.run("MATCH (n:Resource) RETURN n AS resource SKIP " + str(ind) + " LIMIT 1")
    return [record["resource"] for record in result][0]

def get_uri_single_node(node):
    return node["uri"]

def get_label_single_node(node):
    return node["rdfs__label"]

def get_uris(nodes):
    return [node["uri"] for node in nodes]

def get_labels(nodes):
    return [node["rdfs__label"] for node in nodes]

def close_db():
    session.close()
    driver.close()


close_db()
