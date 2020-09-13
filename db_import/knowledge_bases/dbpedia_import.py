from rdflib.graph import Graph
import pprint

ARTICLE_LABELS_PL="/home/azath/Documents/THESIS/lex-sem-resources/LEX-SEM-RESOURCES/DBPEDIA/dbpedia_2020/article_label_pl"
DBPEDIA="/home/azath/Documents/THESIS/lex-sem-resources/LEX-SEM-RESOURCES/DBPEDIA/dbpedia_2020/dbpedia_skos.nt"
DBPEDIA_PREVIEW="/home/azath/Documents/THESIS/lex-sem-resources/LEX-SEM-RESOURCES/DBPEDIA/dbpedia_2020/categories_and_metadata_preview.nt"

def fetch():
    g = Graph()
    g.parse(DBPEDIA, format="nt")
    relation_types = set()
    conter = 0
    for stmt in g:
        print(counter)
        counter += 1
        relation_types.add(stmt[1].toPython())
    print(relation_types)
