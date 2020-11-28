from neo4j import GraphDatabase
import sys

URI = "neo4j://localhost/"
DB_NAME = "neo4j"
PREFIX = "http://plwordnet.pwr.wroc.pl/wordnet/synset/"

driver = GraphDatabase.driver(URI)
session = driver.session(database = DB_NAME)

result = session.run("MATCH (n:Resource) RETURN COUNT(n) AS count")
res2 = [record.count for record in result]
if res2[0] < 8000000:
    sys.exit(2137)
session.close()
driver.close()