""" BEWARE, this test uses working neo4j connection and dataset. Everything is based on SOURCE dataset """

from services.neo4j_db import Neo4jDb

neo_mgr = Neo4jDb("neo4j://neo_src:7687/", "neo4j")

def test_get_related_nodes_weighted_princeton():
    node_uri = "http://plwordnet.pwr.wroc.pl/wordnet/synset/294453"
    princeton = "TRUE"
    initial_uri = "http://plwordnet.pwr.wroc.pl/wordnet/synset/294453"
    nodes = neo_mgr.get_related_nodes_weighted(node_uri, princeton, initial_uri)
    assert len(nodes) == 5
    assert any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294455" for node in nodes])
    assert any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294457" for node in nodes])
    assert any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294454" for node in nodes])
    assert any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294435" and node["weight"] == 8 for node in nodes])
    assert any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294403" and node["weight"] == 8 for node in nodes])

def test_get_related_nodes_weighted_no_princeton():
    node_uri = "http://plwordnet.pwr.wroc.pl/wordnet/synset/294453"
    princeton = "FALSE"
    initial_uri = node_uri
    nodes = neo_mgr.get_related_nodes_weighted(node_uri, princeton, initial_uri)
    assert len(nodes) == 1
    assert not any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294435" for node in nodes])
    assert not any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294403" for node in nodes])
    assert not any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294455" for node in nodes])
    assert not any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294457" for node in nodes])
    assert not any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/294454" for node in nodes])
    assert any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/251975" for node in nodes])
    assert nodes[0]["weight"] == 1
    
def test_get_related_nodes_weighted_no_princeton_polish():
    node_uri = "http://plwordnet.pwr.wroc.pl/wordnet/synset/2169"
    princeton = "FALSE"
    initial_uri = node_uri
    nodes = neo_mgr.get_related_nodes_weighted(node_uri, princeton, initial_uri)
    assert len(nodes) == 21
    assert any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/1396" and node["weight"] == 12 for node in nodes])
    assert any([node["node2"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/72487" and node["weight"] == 12 for node in nodes])
