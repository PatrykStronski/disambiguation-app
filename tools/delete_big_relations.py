from neo4j import GraphDatabase

URI = "neo4j://neo_src/"
DB_NAME = "neo4j"
COUNT= "10000"

driver = GraphDatabase.driver(URI, auth=("neo4j", "123"))
session = driver.session(database = DB_NAME)

to_delete = session.run("MATCH (n:Resource)-[r]-() WITH n, COUNT(r) AS cnt WHERE cnt > " + COUNT + " RETURN n.uri AS uri")
for node in to_delete:
    node_uri = node["uri"]
    print("DELETE " + node_uri)
    exists = session.run('MATCH (n:Resource {uri:"' +node_uri + '"}) RETURN n')
    ex_array = [record for record in exists]
    session.run('MATCH (n:Resource { uri: "' + node_uri + '"})-[r]-() DELETE r,n')

session.close()
driver.close()
