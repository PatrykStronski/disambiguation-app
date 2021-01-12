import pandas as pd
from disambiguation.disambiguation import Disambiguation

def test_calculate_semantic_interconnections_simple():
    candidates = pd.DataFrame([
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "sign": [], "semantic_interconnections": 0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 1
    assert candidates.iloc[2]["semantic_interconnections"] == 0

def test_calculate_semantic_interconnections_bidirectional():
    candidates = pd.DataFrame([
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 1
    assert candidates.iloc[2]["semantic_interconnections"] == 0

def test_calculate_semantic_interconnections_bidirectional_more_complex():
    candidates = pd.DataFrame([
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 2
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[3]["semantic_interconnections"] == 1

def test_calculate_semantic_interconnections_bidirectional_more_complex2():
    candidates = pd.DataFrame([
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.1", "sign": ["http://a/w22", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 1
    assert candidates.iloc[2]["semantic_interconnections"] == 0
    assert candidates.iloc[3]["semantic_interconnections"] == 0

def test_calculate_score_simple():
    candidates = pd.DataFrame([
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.1", "semantic_interconnections": 1, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_score(candidates)
    assert candidates.iloc[0]["score"] == 1.0
    assert candidates.iloc[1]["score"] == 1.0
    assert candidates.iloc[2]["score"] == 0.0
    assert candidates.iloc[3]["score"] == 1.0

def test_calculate_score_complex():
    candidates = pd.DataFrame([
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2.1", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.1", "semantic_interconnections": 1, "deg": 10, "score": 0.0}
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
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2.1", "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.1", "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.2", "semantic_interconnections": 3, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.calculate_score(candidates)
    assert candidates.iloc[0]["score"] == 1.0
    assert candidates.iloc[1]["score"] == 0.5
    assert candidates.iloc[2]["score"] == 0.5
    assert candidates.iloc[3]["score"] == 0.0
    assert candidates.iloc[4]["score"] == 0.25
    assert candidates.iloc[5]["score"] == 0.75

def test_densest_subgraph_simple():
    candidates = pd.DataFrame([
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w3.3", "http://a/w3.5", "http://a/w3.6"], "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "sign": ["http://a/w8", "http://a/w3.2", "http://a/w3.6"], "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2.1", "sign": ["http://a/w1", "http://a/w3.1", "http://a/w3.6"], "semantic_interconnections": 2, "deg": 20, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "sign": [], "semantic_interconnections": 0, "deg": 15, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.1", "sign": [], "semantic_interconnections": 1, "deg": 10, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.2", "sign": [],  "semantic_interconnections": 1, "deg": 22, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.3", "sign": [],  "semantic_interconnections": 1, "deg": 50, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.4", "sign": [],  "semantic_interconnections": 0, "deg": 100, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.5", "sign": [],  "semantic_interconnections": 1, "deg": 15, "score": 0.0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3.6", "sign": [],  "semantic_interconnections": 3, "deg": 10, "score": 0.0}
    ])
    dis = Disambiguation(5,0.2)
    candidates = dis.densest_subgraph(candidates)
    assert candidates.shape[0] == 8
    assert candidates[candidates.basic_form == "w3"].shape[0] == 5

#TODO CHeck the Disambiguation(5,0.2) module e2e write e2e