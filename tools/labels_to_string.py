from neo4j import GraphDatabase

URI = "neo4j://neo_dest/"
DB_NAME = "neo4j"
COUNT= "10000"

LANGUAGE_ALIAS = {
    "polish": "@pl",
    "english": "@en"
}

SUPPORTED_LANGUAGES = ["polish", "english"]
SUPPORTED_LANGUAGES_SUFFIXES = ["@en", "@pl"]

driver = GraphDatabase.driver(URI)
session = driver.session(database = DB_NAME)

def transform_langtag(labels):
    ret = []
    for lab in labels:
       ret += lab[:-3].split(" ")
    return " ".join(list(set(ret)))

for node_ind in range(200000, 338597):
    if node_ind % 1000 == 0:
        print(node_ind)
    node = [{"labels": rec["labels"], "uri": rec["uri"]} for rec in session.run('MATCH (n:Resource) RETURN n.uri AS uri, n.labels AS labels SKIP ' + str(node_ind) + ' LIMIT 1')][0]
    labels = node["labels"]
    if labels:
        lab_en = transform_langtag(filter(lambda lab: lab.endswith("@en"), labels))
        lab_pl = transform_langtag(filter(lambda lab: lab.endswith("@pl"), labels))
        session.run('MATCH (n: Resource {uri: "' + node["uri"] + '"}) SET n.labels_english = "'+ lab_en +'" SET n.labels_polish = "' + lab_pl + '"')

session.close()
driver.close()
