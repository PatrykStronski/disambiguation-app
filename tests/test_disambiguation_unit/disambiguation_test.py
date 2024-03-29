import pandas as pd
from disambiguation.disambiguation import Disambiguation

def test_narrow_semantic_signature_sets_simple():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": [], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.narrow_semantic_signature_sets(candidates)
    assert candidates.iloc[0]["sign"] == ["http://a/w2"]
    assert candidates.iloc[1]["sign"] == []
    assert candidates.iloc[2]["sign"] == []

def test_narrow_semantic_signature_sets_simple2():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": [], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w1", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.narrow_semantic_signature_sets(candidates)
    assert candidates.iloc[0]["sign"] == ["http://a/w2"]
    assert candidates.iloc[1]["sign"] == []
    assert candidates.iloc[2]["sign"] == ["http://a/w1"]

def test_narrow_semantic_signature_sets_complex():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w1", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.narrow_semantic_signature_sets(candidates)
    assert candidates.iloc[0]["sign"] == ["http://a/w2"]
    assert candidates.iloc[1]["sign"] == ["http://a/w1"]
    assert candidates.iloc[2]["sign"] == ["http://a/w1"]

def test_narrow_semantic_signature_sets_complex():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5, 0.2)
    candidates = dis.narrow_semantic_signature_sets(candidates)
    assert candidates.iloc[0]["sign"] == ["http://a/w2"]
    assert candidates.iloc[1]["sign"] == ["http://a/w1"]
    assert candidates.iloc[2]["sign"] == []
    assert candidates.iloc[3]["sign"] == ["http://a/w2"]

def test_calculate_semantic_interconnections_simple():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": [], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 0
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[0]["semantic_in_connections"] == 0
    assert candidates.iloc[1]["semantic_in_connections"] == 1
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[0]["deg"] == 1
    assert candidates.iloc[1]["deg"] == 1
    assert candidates.iloc[2]["deg"] == 0

def test_calculate_semantic_interconnections_bidirectional():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_in_connections"] == 1
    assert candidates.iloc[1]["semantic_in_connections"] == 1
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 1
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[0]["deg"] == 2
    assert candidates.iloc[1]["deg"] == 2
    assert candidates.iloc[2]["deg"] == 0

def test_calculate_semantic_interconnections_bidirectional_more_complex():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_in_connections"] == 1
    assert candidates.iloc[1]["semantic_in_connections"] == 2
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[3]["semantic_in_connections"] == 0
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 1
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[3]["semantic_interconnections"] == 1
    assert candidates.iloc[0]["deg"] == 2
    assert candidates.iloc[1]["deg"] == 3
    assert candidates.iloc[2]["deg"] == 0
    assert candidates.iloc[3]["deg"] == 1

def test_calculate_semantic_interconnections_bidirectional_more_complex2():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "sign": ["http://a/w22", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_in_connections"] == 1
    assert candidates.iloc[1]["semantic_in_connections"] == 1
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[3]["semantic_in_connections"] == 0
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 1
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[3]["semantic_interconnections"] == 0
    assert candidates.iloc[0]["deg"] == 2
    assert candidates.iloc[1]["deg"] == 2
    assert candidates.iloc[2]["deg"] == 0
    assert candidates.iloc[3]["deg"] == 0


def test_calculate_semantic_interconnections_lemma_simple():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "deg": 0.0, "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0, "semantic_in_connections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2",  "deg": 0.0, "sign": [], "semantic_interconnections": 0, "semantic_in_connections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3",  "deg": 0.0, "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0, "semantic_in_connections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections_lemma(candidates, "w1")
    assert candidates.iloc[0]["semantic_in_connections"] == 0
    assert candidates.iloc[1]["semantic_in_connections"] == 0
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 0
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[0]["deg"] == 1
    assert candidates.iloc[1]["deg"] == 0
    assert candidates.iloc[2]["deg"] == 0
    candidates = dis.calculate_semantic_interconnections_lemma(candidates, "w2")
    assert candidates.iloc[0]["semantic_in_connections"] == 0
    assert candidates.iloc[1]["semantic_in_connections"] == 1
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[0]["semantic_interconnections"] == 0
    assert candidates.iloc[1]["semantic_interconnections"] == 0
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[0]["deg"] == 0
    assert candidates.iloc[1]["deg"] == 1
    assert candidates.iloc[2]["deg"] == 0

def test_calculate_semantic_interconnections_lemma_bidirectional():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0, "semantic_in_connections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0, "semantic_in_connections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0, "semantic_in_connections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections_lemma(candidates, "w1")
    assert candidates.iloc[0]["semantic_in_connections"] == 1
    assert candidates.iloc[1]["semantic_in_connections"] == 0
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 0
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[0]["deg"] == 2
    assert candidates.iloc[1]["deg"] == 0
    assert candidates.iloc[2]["deg"] == 0
    candidates = dis.calculate_semantic_interconnections_lemma(candidates, "w3")
    assert candidates.iloc[0]["semantic_in_connections"] == 0
    assert candidates.iloc[1]["semantic_in_connections"] == 0
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[0]["semantic_interconnections"] == 0
    assert candidates.iloc[1]["semantic_interconnections"] == 0
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[0]["deg"] == 0
    assert candidates.iloc[1]["deg"] == 0
    assert candidates.iloc[2]["deg"] == 0
    candidates = dis.calculate_semantic_interconnections_lemma(candidates, "w2")
    assert candidates.iloc[0]["semantic_in_connections"] == 0
    assert candidates.iloc[1]["semantic_in_connections"] == 1
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[0]["semantic_interconnections"] == 0
    assert candidates.iloc[1]["semantic_interconnections"] == 1
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[0]["deg"] == 0
    assert candidates.iloc[1]["deg"] == 2
    assert candidates.iloc[2]["deg"] == 0

def test_calculate_semantic_interconnections_lemma_bidirectional_more_complex():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections_lemma(candidates, "w2")
    assert candidates.iloc[0]["semantic_in_connections"] == 0
    assert candidates.iloc[1]["semantic_in_connections"] == 2
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[3]["semantic_in_connections"] == 0

def test_calculate_semantic_interconnections_lemma_bidirectional_more_complex2():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "sign": ["http://a/w22", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections_lemma(candidates, "w3")
    assert candidates.iloc[0]["semantic_in_connections"] == 0
    assert candidates.iloc[1]["semantic_in_connections"] == 0
    assert candidates.iloc[2]["semantic_in_connections"] == 0
    assert candidates.iloc[3]["semantic_in_connections"] == 0

def test_calculate_score_simple():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "semantic_interconnections": 1, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_score(candidates)
    assert candidates.iloc[0]["score"] == 1.0
    assert candidates.iloc[1]["score"] == 1.0
    assert candidates.iloc[2]["score"] == 0.0
    assert candidates.iloc[3]["score"] == 1.0

def test_calculate_score_complex():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2.1", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "semantic_interconnections": 1, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_score(candidates)
    assert candidates.iloc[0]["score"] == 1.0
    assert candidates.iloc[1]["score"] == 0.5
    assert candidates.iloc[2]["score"] == 0.5
    assert candidates.iloc[3]["score"] == 0.0
    assert candidates.iloc[4]["score"] == 1.0

def test_calculate_score_complex2():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2.1", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.2", "semantic_interconnections": 3, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_score(candidates)
    assert candidates.iloc[0]["score"] == 1.0
    assert candidates.iloc[1]["score"] == 0.5
    assert candidates.iloc[2]["score"] == 0.5
    assert candidates.iloc[3]["score"] == 0.0
    assert candidates.iloc[4]["score"] == 0.25
    assert candidates.iloc[5]["score"] == 0.75


def test_calculate_score_lemma_simple():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "semantic_interconnections": 1, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_score_lemma(candidates, "w1")
    assert candidates.iloc[0]["score"] == 1.0
    assert candidates.iloc[1]["score"] == 0.0
    assert candidates.iloc[2]["score"] == 0.0
    assert candidates.iloc[3]["score"] == 0.0

def test_calculate_score_lemma_complex():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2.1", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "semantic_interconnections": 1, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_score_lemma(candidates, "w1")
    candidates = dis.calculate_score_lemma(candidates, "w2")
    assert candidates.iloc[0]["score"] == 1.0
    assert candidates.iloc[1]["score"] == 0.5
    assert candidates.iloc[2]["score"] == 0.5
    assert candidates.iloc[3]["score"] == 0.0
    assert candidates.iloc[4]["score"] == 0.0

def test_calculate_score_lemma_complex2():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2.1", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.2", "semantic_interconnections": 3, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_score_lemma(candidates, "w3")
    assert candidates.iloc[0]["score"] == 0.0
    assert candidates.iloc[1]["score"] == 0.0
    assert candidates.iloc[2]["score"] == 0.0
    assert candidates.iloc[3]["score"] == 0.0
    assert candidates.iloc[4]["score"] == 0.25
    assert candidates.iloc[5]["score"] == 0.75

def test_densest_subgraph_simple():
    candidates = pd.DataFrame([
        {"orth": "w1", "lemma": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w3.3", "http://a/w3.5", "http://a/w3.6"], "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2", "sign": ["http://a/w8", "http://a/w3.2", "http://a/w3.6"], "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w2", "lemma": "w2", "uri": "http://a/w2.1", "sign": ["http://a/w1", "http://a/w3.1", "http://a/w3.6"], "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3", "sign": [], "semantic_in_connections": 0, "deg": 15, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.1", "sign": [], "semantic_in_connections": 1, "deg": 10, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.2", "sign": [],  "semantic_in_connections": 1, "deg": 22, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.3", "sign": [],  "semantic_in_connections": 1, "deg": 50, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.4", "sign": [],  "semantic_in_connections": 0, "deg": 100, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.5", "sign": [],  "semantic_in_connections": 1, "deg": 15, "score": 0.0},
        {"orth": "w3", "lemma": "w3", "uri": "http://a/w3.6", "sign": [],  "semantic_in_connections": 3, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5, 0.4)
    candidates = dis.densest_subgraph(candidates)
    assert candidates.shape[0] == 3
    assert candidates[candidates.lemma == "w3"].shape[0] == 0
