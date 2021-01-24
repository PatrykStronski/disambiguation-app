from disambiguation.random_walk import RandomWalk
from services.neo4j_db import Neo4jDb
from utils.lemmatizer import Lemmatizer
import pandas as pd
from config import PHRASE_SEPARATOR

def test_semantic_signature_pl():
    neo_src = Neo4jDb("bolt://neo_src/", "neo4j")
    neo_dest = Neo4jDb("bolt://neo_dest/", "neo4j")
    lemmatizer = Lemmatizer()
    initial_node = "http://plwordnet.pwr.wroc.pl/wordnet/synset/431894"
    node_properties = { "skos__prefLabel": ["krwawnikowy@pl"], "uri": "http://plwordnet.pwr.wroc.pl/wordnet/synset/431894", "princeton": "FALSE" }
    rw = RandomWalk(initial_node, node_properties, 50, 2, 0.1, neo_src, neo_dest, lemmatizer)
    rw.random_walk_with_restart()
    #test lemmatization
    assert rw.polish_lemmatization_code == None
    assert rw.node_properties["labels_polish"] == "*krwawnikowy*"
    assert rw.node_properties["labels_english"] == ""
    #test semsign
    semsign = rw.get_graph()
    assert type(semsign) == pd.DataFrame
    assert semsign.shape[0] > 3

def test_semantic_signature_pl_small_rw():
    neo_src = Neo4jDb("bolt://neo_src/", "neo4j")
    neo_dest = Neo4jDb("bolt://neo_dest/", "neo4j")
    lemmatizer = Lemmatizer()
    initial_node = "http://plwordnet.pwr.wroc.pl/wordnet/synset/431894"
    node_properties = { "skos__prefLabel": ["krwawnikowy@pl"], "uri": "http://plwordnet.pwr.wroc.pl/wordnet/synset/431894", "princeton": "FALSE" }
    rw = RandomWalk(initial_node, node_properties, 20, 3, 0.02, neo_src, neo_dest, lemmatizer)
    rw.random_walk_with_restart()
    #test semsign
    semsign = rw.get_graph()
    assert type(semsign) == pd.DataFrame
    assert semsign.shape[0] < 5

def test_semantic_signature_pl_big_rw():
    neo_src = Neo4jDb("bolt://neo_src/", "neo4j")
    neo_dest = Neo4jDb("bolt://neo_dest/", "neo4j")
    lemmatizer = Lemmatizer()
    initial_node = "http://plwordnet.pwr.wroc.pl/wordnet/synset/431894"
    node_properties = { "skos__prefLabel": ["krwawnikowy@pl"], "uri": "http://plwordnet.pwr.wroc.pl/wordnet/synset/431894", "princeton": "FALSE" }
    rw = RandomWalk(initial_node, node_properties, 50, 1, 0.05, neo_src, neo_dest, lemmatizer)
    rw.random_walk_with_restart()
    #test semsign
    semsign = rw.get_graph()
    assert type(semsign) == pd.DataFrame
    assert semsign.shape[0] > 10

def test_semantic_signature_pl_multiword():
    neo_src = Neo4jDb("bolt://neo_src/", "neo4j")
    neo_dest = Neo4jDb("bolt://neo_dest/", "neo4j")
    lemmatizer = Lemmatizer()
    initial_node = "http://plwordnet.pwr.wroc.pl/wordnet/synset/85138"
    node_properties = { "skos__prefLabel": ["przesączanie się@pl"], "uri": "http://plwordnet.pwr.wroc.pl/wordnet/synset/85138", "princeton": "FALSE" }
    rw = RandomWalk(initial_node, node_properties, 50, 2, 0.1, neo_src, neo_dest, lemmatizer)
    rw.random_walk_with_restart()
    #test lemmatization
    assert type(rw.polish_lemmatization_code) == str
    if rw.polish_lemmatization_code:
        rw.node_properties["labels_polish"] += rw.align_labels(rw.lemmatizer.download_lemmatization(rw.polish_lemmatization_code, PHRASE_SEPARATOR)[0])
    assert rw.node_properties["labels_polish"] == "*przesączać się*"
    assert rw.node_properties["labels_english"] == ""
    #test semsign
    semsign = rw.get_graph()
    assert type(semsign) == pd.DataFrame
    assert semsign.shape[0] > 3

def test_semantic_signature_en():
    neo_src = Neo4jDb("bolt://neo_src/", "neo4j")
    neo_dest = Neo4jDb("bolt://neo_dest/", "neo4j")
    lemmatizer = Lemmatizer()
    initial_node = "http://plwordnet.pwr.wroc.pl/wordnet/synset/270480"
    node_properties = { "skos__prefLabel": ["known@en"], "uri": "http://plwordnet.pwr.wroc.pl/wordnet/synset/270480", "princeton": "TRUE" }
    rw = RandomWalk(initial_node, node_properties, 50, 2, 0.1, neo_src, neo_dest, lemmatizer)
    rw.random_walk_with_restart()
    #test lemmatization
    assert rw.polish_lemmatization_code == None
    assert rw.node_properties["labels_polish"] == ""
    assert rw.node_properties["labels_english"] == "*known*"
    #test semsign
    semsign = rw.get_graph()
    assert type(semsign) == pd.DataFrame
    assert semsign.shape[0] > 3

