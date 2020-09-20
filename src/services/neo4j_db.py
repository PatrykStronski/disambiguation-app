from neo4j import GraphDatabase

URI = "neo4j://localhost:7687/"
KNOWLEDGE_BASE = "knowledgebase"
driver = GraphDatabase.driver(URI)
session = driver.session(database = KNOWLEDGE_BASE)

def get_resource_label(label):
    result = session.run("MATCH (n:Resource {rdfs__label: '" + label + "'}) -- (b) RETURN n AS resource")
    return [record["resource"] for record in result]

def get_cardinality_uri(resource_uri):
    return session.run("MATCH (:Resource {uri: '" + resource_uri + "'}) -[r]- (n) RETURN COUNT(r) AS cardinality")

def get_cardinality_label(resource_label):
    result = session.run("MATCH (:Resource {rdfs__label: '" + resource_label + "'}) -[r]- (n) RETURN COUNT(r) AS cardinality")
    return [record["cardinality"] for record in result][0]

def get_related_nodes_label(label):
    result = session.run("MATCH (:Resource {rdfs__label: '" + label + "'}) -- (b) RETURN b AS resource")
    return [record["resource"] for record in result]

def get_uris(nodes):
    return [node["uri"] for node in nodes]

def get_labels(nodes):
    return [node["rdfs__label"] for node in nodes]

def close_db():
    session.close()
    driver.close()

#print(get_labels(get_resource_label("Canada@it")))
#close_db()
