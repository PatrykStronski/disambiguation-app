import pandas as pd
from disambiguation.random_walk import RandomWalk
from utils.lemmatizer import Lemmatizer

lem = Lemmatizer()

def test_should_restart():
    init_graph = RandomWalk("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 0, 0, None, None, lem)
    ret = init_graph.should_restart()
    assert ret == True or ret == False

def test_choose_relation():
    init_graph = RandomWalk("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None, lem)
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
    init_graph = RandomWalk("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None, lem)
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
    init_graph = RandomWalk("http://dummyurl", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None, lem)
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
    init_graph = RandomWalk("ns", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None, lem)
    picked_node = "n1"
    assert init_graph.node_visit_counts.shape == (0,2)
    init_graph.increment_visits(picked_node)
    assert init_graph.node_visit_counts.shape == (1,2)
    assert { "count": 1, "node2": "n1" } == init_graph.node_visit_counts.loc[0].to_dict()

def test_increment_visits_same_entry():
    init_graph = RandomWalk("ns", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None, lem)
    picked_relation = { "count": 1, "node2": "n1" }
    init_graph.node_visit_counts = pd.DataFrame([picked_relation])
    assert init_graph.node_visit_counts.shape == (1,2)
    init_graph.increment_visits(picked_relation["node2"])
    assert init_graph.node_visit_counts.shape == (1,2)
    assert { "count": 2, "node2": "n1" } == init_graph.node_visit_counts.loc[0].to_dict()

def test_increment_visits_different_entry():
    init_graph = RandomWalk("ns", { "skos__prefLabel": ["Label"]}, 0, 5, 0, None, None, lem)
    old_relation = { "count": 1, "node2": "n1" }
    picked_node = "n1"
    init_graph.node_visit_counts = pd.DataFrame([old_relation])
    assert init_graph.node_visit_counts.shape == (1, 2)
    init_graph.increment_visits(picked_node)
    assert init_graph.node_visit_counts.shape == (1, 2)
    assert { "count": 2, "node2": "n1" } == init_graph.node_visit_counts.loc[0].to_dict()

def test_detect_langauge():
    init_graph = RandomWalk("ns", {"skos__prefLabel": ["Label"]}, 0, 5, 0, None, None, lem)
    label = "label1@bg"
    assert init_graph.detect_langauge(label) is None
    label = "label 1@de"
    assert init_graph.detect_langauge(label) is None
    label = "label1@pl"
    assert init_graph.detect_langauge(label) is "polish"
    label = "label 1@en"
    assert init_graph.detect_langauge(label) is "english"
    
def test_create_lemmatized_labels():
    init_graph = RandomWalk("ns", {"skos__prefLabel": ["Label@en", "metka@pl"], "skos__altLabel": ["znaczenie@pl", "meaning@en"]}, 0, 5, 0, None, None, lem)
    assert init_graph.node_properties["labels_polish"] == "*metka**znaczenie*"
    assert init_graph.node_properties["labels_english"] == "*label**meaning*"

def test_create_lemmatized_labels_deu():
    init_graph = RandomWalk("ns", {"skos__prefLabel": ["Label@en", "metka@pl", "labell@de"], "skos__altLabel": ["znaczenie@pl"]}, 0, 5, 0, None, None, lem)
    assert init_graph.node_properties["labels_polish"] == "*metka**znaczenie*"
    assert init_graph.node_properties["labels_english"] == "*label*"

def test_create_lemmatized_labels_deu_ru():
    init_graph = RandomWalk("ns", {"skos__prefLabel": ["Label@en", "metka@pl", "labell@de"], "rdfs__label": ["znaczenie@pl"], "skos__altLabel": ["метка@ru"]}, 0, 5, 0, None, None, lem)
    assert init_graph.node_properties["labels_polish"] == "*metka**znaczenie*"
    assert init_graph.node_properties["labels_english"] == "*label*"

def test_create_lemmatized_labels_multiword():
    init_graph = RandomWalk("ns", {"skos__prefLabel": ["labelled label@en", "ometkowana metka@pl", "labell@de"], "rdfs__label": ["znaczenie@pl"], "skos__altLabel": ["метка@ru"]}, 0, 5, 0, None, None, lem)
    assert init_graph.node_properties["labels_polish"] == "*znaczenie*"
    assert init_graph.node_properties["labels_english"] == "*label label*"
