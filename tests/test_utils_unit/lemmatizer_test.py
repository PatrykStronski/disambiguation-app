from utils.lemmatizer import Lemmatizer

def test_english_word():
    word = "becoming"
    lem = Lemmatizer()
    assert lem.lemmatize_en(word) == ["become"]

def test_english_sentence():
    sentence = "I have always dreamed about becoming a hero"
    lem = Lemmatizer()
    assert lem.lemmatize_en(sentence) == ["-PRON-", "have", "always", "dream", "about", "become", "a", "hero"]

def test_polish_word():
    word = "robiłem"
    lem = Lemmatizer()
    assert lem.lemmatize_pl(word) == ["robić"]

def test_polish_sentence():
    word = "Ja robiłem dużo zadań."
    lem = Lemmatizer()
    assert lem.lemmatize_pl(word) == ["-PRON-", "robić", "dużo", "zadania"]
