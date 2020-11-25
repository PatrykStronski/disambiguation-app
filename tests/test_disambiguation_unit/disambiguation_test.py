import pandas as pd
from disambiguation.disambiguation import Disambiguation

def test_calculate_semantic_interconnections_simple():
    candidates = pd.DataFrame([
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "sign": [], "semantic_interconnections": 0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation()
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 1
    assert candidates.iloc[2]["semantic_interconnections"] == 0

def test_calculate_semantic_interconnections_non_bidirectional():
    candidates = pd.DataFrame([
        {"word": "w1", "basic_form": "w1", "uri": "http://a/w1", "sign": ["http://a/w2", "http://a/w8"], "semantic_interconnections": 0},
        {"word": "w2", "basic_form": "w2", "uri": "http://a/w2", "sign": ["http://a/w1"], "semantic_interconnections": 0},
        {"word": "w3", "basic_form": "w3", "uri": "http://a/w3", "sign": ["http://a/w9", "http://a/w8"], "semantic_interconnections": 0}
    ])
    dis = Disambiguation()
    candidates = dis.calculate_semantic_interconnections(candidates)
    assert candidates.iloc[0]["semantic_interconnections"] == 1
    assert candidates.iloc[1]["semantic_interconnections"] == 1
    assert candidates.iloc[2]["semantic_interconnections"] == 0
