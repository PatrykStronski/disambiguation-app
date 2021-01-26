from neo4j import GraphDatabase
import csv

tsv_file = open("/data/pwn-plwn-3.0.txt")
read_tsv = csv.reader(tsv_file, delimiter="\t")

senses_file = open("/data/index.sense")
read_senses = csv.reader(senses_file, delimiter=" ")

senses_arr = []
for sense_r in read_senses:
   senses_arr.append((sense_r[0], sense_r[1]))

URI = "neo4j://neo_dest/"
DB_NAME = "neo4j"
PREFIX = "http://plwordnet.pwr.wroc.pl/wordnet/synset/"

driver = GraphDatabase.driver(URI)
session = driver.session(database = DB_NAME)

def find_offset(princeton_id):
   ids = []
   for sense in senses_arr:
      if str(princeton_id) == str(sense[1]):
         ids.append(sense[0])
   if len(ids) > 0:
      print(" ".join(ids))
      return ", ".join(ids)
   return princeton_id

for row in read_tsv:
   if row[0] == "plwordnet_id":
      continue
   synset = PREFIX + row[0]
   princeton_id = row[1]
   princeton_offset = find_offset(princeton_id)
   session.run('MATCH (n:Resource { uri: "' + synset + '"}) SET n.princeton = true SET n.princeton_id = "' + princeton_offset + '"')
#session.run("MATCH (n:Resource) WHERE n.uri STARTS WITH '" + PREFIX + "' AND n.princeton IS NULL SET n.princeton = false")
tsv_file.close()
session.close()
driver.close()
