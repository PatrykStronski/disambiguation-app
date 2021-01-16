from neo4j import GraphDatabase
import sys

URI = "neo4j://neo_dest/"
DB_NAME = "neo4j"
COUNT= "10000"

LANGUAGE_ALIAS = {
    "polish": "@pl",
    "english": "@en"
}

PHRASE_SEPARATOR = "*"
SUPPORTED_LANGUAGES = ["polish", "english"]
SUPPORTED_LANGUAGES_SUFFIXES = ["@en", "@pl"]

driver = GraphDatabase.driver(URI)
session = driver.session(database = DB_NAME)

def transform_langtag(labels):
    ret = []
    for lab in labels:
       ret.append(PHRASE_SEPARATOR + lab[:-3] + PHRASE_SEPARATOR)
    return " ".join(list(set(ret)))

start = int(sys.argv[1])
end = int(sys.argv[2])
for node_ind in range(start, end):
    if node_ind % 1000 == 0:
        print(node_ind)
    node = [{"elabels": rec["elabels"], "plabels": rec["plabels"], "uri": rec["uri"]} for rec in session.run('MATCH (n:Resource) RETURN n.uri AS uri, n.labels_polish AS plabels, n.labels_english AS elabels SKIP ' + str(node_ind) + ' LIMIT 1')][0]
    if node["plabels"]:
        lab_pl = PHRASE_SEPARATOR + PHRASE_SEPARATOR.join(node["plabels"].split(" ")) + PHRASE_SEPARATOR
    else:
        lab_pl = ""
    if node["elabels"]:
        lab_en = PHRASE_SEPARATOR + PHRASE_SEPARATOR.join(node["elabels"].split(" ")) + PHRASE_SEPARATOR
    else:
        lab_en = ""
    session.run('MATCH (n: Resource {uri: "' + node["uri"] + '"}) SET n.labels_english = "'+ lab_en +'" SET n.labels_polish = "' + lab_pl + '"')

session.close()
driver.close()
