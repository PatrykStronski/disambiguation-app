import sys
import os
import urllib.parse

RELATIONS = {
    "sameAs": "<http://www.w3.org/2002/07/owl#sameAs>",
    "narrower": "<http://www.w3.org/2004/02/skos/core#narrower>",
    "broader": "<http://www.w3.org/2004/02/skos/core#broader>",
    "related": "<http://www.w3.org/2004/02/skos/core#related>"
}

def parse_relation(relation):
    if relation.startswith("http://") or relation.startswith("https://"):
        return '<' + relation + '>'
    else:
        rel = RELATIONS.get(relation)
        if rel:
            return rel
        else:
            return '\"' + urllib.parse.quote(relation) + '\"'

file_name = sys.argv[1]
out = sys.argv[2]
if os.path.exists(out):
    os.remove(out)
destination = open(out, "a+", encoding="utf-8")

with open(file_name, "r", encoding="utf-8") as content:
    for line in content:
        triplet_rdf = line.split('\t')
        write_line = "<" + triplet_rdf[0] + "> "
        write_line += parse_relation(triplet_rdf[1]) + ' '
        if triplet_rdf[2].startswith("http://") or triplet_rdf[2].startswith("https://"):
            write_line += "<" + triplet_rdf[2].strip() + "> .\n"
        else:
            write_line += "\"" + urllib.parse.quote(triplet_rdf[2]) + "\" .\n"
        destination.write(write_line)

destination.close()
