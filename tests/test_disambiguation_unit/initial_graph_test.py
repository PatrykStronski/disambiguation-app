import pandas as pd
from disambiguation.initial_graph import InitialGraph

#def test_extract_language_en():
#    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": ["Label@en", "Label1@en"]}, 0, 0, 0, None, None)
#    assert init_graph.extract_language() == "@en"
#    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": "Label@en"}, 0, 0, 0, None, None)
#    assert init_graph.extract_language() == "@en"

#def test_extract_language_pl():
#    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": ["Label@pl"]}, 0, 0, 0, None, None)
#    assert init_graph.extract_language() == "@pl"
#    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": "Label@pl"}, 0, 0, 0, None, None)
#    assert init_graph.extract_language() == "@pl"

#def test_extract_language_all():
#    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": ["Label@pl", "Label@en"]}, 0, 0, 0, None, None)
#    assert init_graph.extract_language() == "all"
#    init_graph = InitialGraph("http://dummyurl", { }, 0, 0, 0, None, None)
#    assert init_graph.extract_language() == "all"

def test_should_restart():
    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 0, 0, None, None)
    ret = init_graph.should_restart()
    assert ret == True or ret == False

def test_choose_relation():
    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None)
    relations = pd.DataFrame([
        { "relation": "rel1", "node2": "n1", "weight": 1 },
        { "relation": "rel2", "node2": "n1", "weight": 9 },
        { "relation": "rel3", "node2": "n1", "weight": 5 },
        { "relation": "rel4", "node2": "n1", "weight": 4 },
        { "relation": "rel5", "node2": "n1", "weight": 1 },
    ])
    picked_relation = init_graph.choose_relation(relations)
    assert type(picked_relation) is dict

def test_choose_relation_randomness():
    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None)
    relations = pd.DataFrame([
        { "relation": "rel1", "node2": "n1", "weight": 1 },
        { "relation": "rel2", "node2": "n1", "weight": 1 },
        { "relation": "rel3", "node2": "n1", "weight": 1 },
        { "relation": "rel4", "node2": "n1", "weight": 1 },
        { "relation": "rel5", "node2": "n1", "weight": 1 },
    ])
    picked1 = init_graph.choose_relation(relations)
    picked2 = init_graph.choose_relation(relations)
    if picked1["relation"] == picked2["relation"]:
        picked2 = init_graph.choose_relation(relations)
    if picked1["relation"] == picked2["relation"]:
        picked2 = init_graph.choose_relation(relations)
    assert picked1["relation"] != picked2["relation"]

def test_choose_relation_biasness():
    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None)
    relations = pd.DataFrame([
        { "relation": "rel1", "node2": "n1", "weight": 1 },
        { "relation": "rel2", "node2": "n1", "weight": 200 },
        { "relation": "rel3", "node2": "n1", "weight": 1 },
        { "relation": "rel4", "node2": "n1", "weight": 1 },
        { "relation": "rel5", "node2": "n1", "weight": 1 },
        { "relation": "rel6", "node2": "n1", "weight": 1 },
        { "relation": "rel7", "node2": "n1", "weight": 1 },
    ])
    picked1 = init_graph.choose_relation(relations)
    picked2 = init_graph.choose_relation(relations)
    assert picked1["relation"] == "rel2" or picked2["relation"] == "rel2"

def test_increment_visits_empty():
    init_graph = InitialGraph("ns", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None)
    picked_relation = { "relation": "rel3", "journey_length": 1.0, "node2": "n1", "node1": "ns" }
    assert init_graph.node_visit_counts.shape == (0,2)
    init_graph.increment_visits(picked_relation)
    assert init_graph.node_visit_counts.shape == (1,3)
    assert { "count": 1, "journey_length": 0.0, "node2": "n1" } == init_graph.node_visit_counts.loc[0].to_dict()

def test_increment_visits_same_entry():
    init_graph = InitialGraph("ns", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None)
    picked_relation = { "count": 1, "journey_length": 1.0, "relation": "rel3", "node1": "ns", "node2": "n1" }
    init_graph.node_visit_counts = pd.DataFrame([picked_relation])
    assert init_graph.node_visit_counts.shape == (1,5)
    init_graph.increment_visits(picked_relation)
    assert init_graph.node_visit_counts.shape == (1,5)
    assert { "count": 2, "journey_length": 1.0, "relation": "rel3", "node1": "ns", "node2": "n1" } == init_graph.node_visit_counts.loc[0].to_dict()

def test_increment_visits_different_entry():
    init_graph = InitialGraph("ns", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None)
    old_relation = { "count": 1, "journey_length": 1.0, "relation": "rel4", "node1": "nOld", "node2": "n1" }
    picked_relation = { "relation": "rel3", "journey_length": 1.0, "node2": "n1", "node1": "ns" }
    init_graph.node_visit_counts = pd.DataFrame([old_relation])
    assert init_graph.node_visit_counts.shape == (1,5)
    init_graph.increment_visits(picked_relation)
    assert init_graph.node_visit_counts.shape == (1,5)
    assert { "count": 2, "journey_length": 1.0, "relation": "rel4", "node1": "nOld", "node2": "n1" } == init_graph.node_visit_counts.loc[0].to_dict()
