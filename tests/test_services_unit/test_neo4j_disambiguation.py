""" Bewaore, this uses neo4j dest database in Docker connection. It needs to have the correct working dataset"""

from services.neo4j_disambiguation import Neo4jDisambiguation

neo_mgr = Neo4jDisambiguation("neo4j")

def test_find_words_labels_polish():
    label = "ocean"
    lang = "polish"
    candidates = neo_mgr.find_word_labels(label, lang)
    assert len(candidates) == 1

def test_find_words_labels_polish_weak():
    label = "ocean"
    lang = "polish"
    candidates = neo_mgr.find_word_labels_weak(label, lang)
    assert len(candidates) == 28

def test_find_words_labels_english():
    label = "ocean"
    lang = "english"
    candidates = neo_mgr.find_word_labels(label, lang)
    assert len(candidates) == 3

def test_find_words_labels_english_weak():
    label = "ocean"
    lang = "english"
    candidates = neo_mgr.find_word_labels_weak(label, lang)
    assert len(candidates) == 43
