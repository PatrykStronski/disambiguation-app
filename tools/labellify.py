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
    return ret

start = int(sys.argv[1])
end = int(sys.argv[2])
for node_ind in range(start, end):
    if node_ind % 1000 == 0:
        print(node_ind)
    node = [{"alabels": rec["alabels"], "plabels": rec["plabels"], "uri": rec["uri"]} for rec in session.run('MATCH (n:Resource) RETURN n.uri AS uri, n.skos__prefLabel AS plabels, n.skos_altLabel AS alabels SKIP ' + str(node_ind) + ' LIMIT 1')][0]
    if not node["alabels"] and not node["plabels"]:
        continue
    if not node["alabels"]:
        node["alabels"] = []
    if not node["plabels"]:
        node["plabels"] = []
    labels = node["alabels"] + node["plabels"]
    print(labels)
    plabels = transform_langtag(list(filter(lambda l: l.endswith("@pl"),labels)))
    elabels = transform_langtag(list(filter(lambda l: l.endswith("@en"),labels)))
    if plabels:
        lab_pl = PHRASE_SEPARATOR + PHRASE_SEPARATOR.join(plabels) + PHRASE_SEPARATOR
    else:
        lab_pl = ""
    if elabels:
        lab_en = PHRASE_SEPARATOR + PHRASE_SEPARATOR.join(elabels) + PHRASE_SEPARATOR
    else:
        lab_en = ""
    session.run('MATCH (n: Resource {uri: "' + node["uri"] + '"}) SET n.labels_english = "'+ lab_en +'" SET n.labels_polish = "' + lab_pl + '"')

session.close()
driver.close()
