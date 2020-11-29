from neo4j import GraphDatabase

URI = "neo4j://172.17.0.2/"
DB_NAME = "neo4j"
COUNT= "10000"

driver = GraphDatabase.driver(URI)
session = driver.session(database = DB_NAME)

to_delete = session.run("MATCH (n:Resource)-[r]-() WITH n,r, COUNT(r) AS cnt WHERE cnt > " + COUNT + " RETURN n.uri AS uri")
for node in to_delete:
    node_uri = node["uri"]
    print("DELETE " + node_uri)
    exists = session.run("MATCH (n:Resource {uri:'" +node_uri + "'}) RETURN n")
    while exists.length > 0:
        session.run("MATCH (n:Resource { uri: '" + node_uri + "'})-[r]-() DELETE r,n LIMIT 10000")

session.close()
driver.close()
