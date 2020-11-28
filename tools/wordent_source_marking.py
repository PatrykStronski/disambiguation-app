from neo4j import GraphDatabase
import csv

tsv_file = open("/home/azath/Documents/THESIS/pwn-plwn-3.0.txt")
read_tsv = csv.reader(tsv_file, delimiter="\t")

URI = "neo4j://localhost/"
DB_NAME = "neo4j"
PREFIX = "http://plwordnet.pwr.wroc.pl/wordnet/synset/"

driver = GraphDatabase.driver(URI)
session = driver.session(database = DB_NAME)

for row in read_tsv:
   synset = PREFIX + row[0]
   session.run("MATCH (n:Resource { uri: '" + synset + "'}) SET n.princeton = true")
session.run("MATCH (n:Resource) WHERE n.uri STARTS WITH '" + PREFIX + "' AND n.princeton IS NULL SET n.princeton = false")
tsv_file.close()
session.close()
driver.close()
