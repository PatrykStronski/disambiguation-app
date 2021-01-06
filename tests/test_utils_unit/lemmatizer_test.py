from utils.lemmatizer import Lemmatizer

lem = Lemmatizer()

def test_polish_word():
    word = "robiłem"
    assert lem.lemmatize_pl(word) == ["robić", "być"]

def test_polish_word():
    word = "mała"
    assert lem.lemmatize_pl(word) == ["mały"]

def test_polish_sentence():
    word = "Ja robiłem dużo zadań."
    assert lem.lemmatize_pl(word) == ["ja", "robić", "być", "dużo", "zadanie", "."]

def test_english_word():
    word = "becoming"
    assert lem.lemmatize_en(word) == ["become"]

def test_english_sentence():
    sentence = "I have always dreamed about becoming a hero"
    assert lem.lemmatize_en(sentence) == ["-PRON-", "have", "always", "dream", "about", "become", "a", "hero"]
