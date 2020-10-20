import pandas as pd
from disambiguation.initial_graph import InitialGraph

def test_should_restart():
    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 0, 0, None, None)
    ret = init_graph.should_restart()
    assert ret == True or ret == False

def test_choose_relation():
    init_graph = InitialGraph("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None)
    relations = pd.DataFrame([
        { "relation": "rel1", "node2": "n1", "probability": 0.01 },
        { "relation": "rel2", "node2": "n1", "probability": 0.09 },
        { "relation": "rel3", "node2": "n1", "probability": 0.5 },
        { "relation": "rel4", "node2": "n1", "probability": 0.4 },
        { "relation": "rel5", "node2": "n1", "probability": 0.1 },
    ])
    picked_relation = init_graph.choose_relation(relations)
    assert type(picked_relation) is dict

def test_increment_visits_empty():
    init_graph = InitialGraph("ns", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None)
    picked_relation = { "relation": "rel3", "node2": "n1", "node1": "ns", "probability": 0.5 }
    assert len(init_graph.node_visit_counts) == 0
    init_graph.increment_visits(picked_relation)
    assert len(init_graph.node_visit_counts) == 1
    assert { "count": 1, "relation": "rel3", "node1": "ns", "node2": "n1" } in init_graph.node_visit_counts

def test_increment_visits_same_entry():
    init_graph = InitialGraph("ns", 0, 5, 0, None)
    picked_relation = { "count": 1, "relation": "rel3", "node1": "ns", "node2": "n1" }
    init_graph.node_visit_counts = pd.DataFrame([picked_relation])
    assert len(init_graph.node_visit_counts) == 1
    init_graph.increment_visits(picked_relation)
    assert len(init_graph.node_visit_counts) == 1
    assert { "count": 2, "relation": "rel3", "node1": "ns", "node2": "n1" } in init_graph.node_visit_counts

def test_increment_visits_different_entry():
    init_graph = InitialGraph("ns", 0, 5, 0, None)
    old_relation = { "count": 1, "relation": "rel4", "node1": "nOld", "node2": "n1" }
    picked_relation = { "relation": "rel3", "node2": "n1", "probability": 0.5}
    init_graph.node_visit_counts = [old_relation]
    assert len(init_graph.node_visit_counts) == 1
    init_graph.increment_visits(picked_relation)
    assert len(init_graph.node_visit_counts) == 2
    assert { "count": 1, "relation": "rel4", "node1": "nOld", "node2": "n1" } in init_graph.node_visit_counts
    assert { "count": 1, "relation": "rel3", "node1": "ns", "node2": "n1" } in init_graph.node_visit_counts
