from utils.lemmatizer import Lemmatizer

lem = Lemmatizer()

def test_polish_word():
    word = "robiłem"
    assert lem.lemmatize(word, "polish") == ["robić", "być"]

def test_polish_word():
    word = "mała"
    assert lem.lemmatize(word, "polish") == ["mały"]

def test_polish_label_multiword():
    label = "*ometkowana metka*"
    assert lem.lemmatize(label, "polish", False) == ["*", "ometkować", "metka", "*"]

def test_polish_sentence():
    word = "Ja robiłem dużo zadań."
    assert lem.lemmatize(word, "polish") == ["ja", "robić", "być", "dużo", "zadanie", "."]

def test_polish_word_orth():
    word = "robiłem"
    assert lem.lemmatize_orth(word, "polish") == (["robić", "być"], ["robiłem", ""])

def test_polish_word_orth():
    word = "mała"
    assert lem.lemmatize_orth(word, "polish") == (["mały"], ["mała"])

def test_polish_label_multiword_orth():
    label = "*ometkowana metka*"
    assert lem.lemmatize_orth(label, "polish") == (["*", "ometkować", "metka", "*"], ["*", "ometkowana", "metka", "*"])

def test_polish_sentence_orth():
    word = "Ja robiłem dużo zadań."
    assert lem.lemmatize_orth(word, "polish") == (["ja", "robić", "być", "dużo", "zadanie", "."], ["Ja", "robił", "em", "dużo", "zadań", "."])

def test_polish_sentence_prep_default():
    word = "Ja robiłem dużo zadań w domu po szkole."
    assert lem.lemmatize(word, "polish") == ["ja", "robić", "być", "dużo", "zadanie", "w", "dom", "po", "szkoła", "."]

def test_english_label():
    sentence = "*labelled label*"
    assert lem.lemmatize(sentence, "english", False) == ["*", "label", "label", "*"]

def test_english_word():
    word = "becoming"
    assert lem.lemmatize(word, "english") == ["become"]

def test_english_sentence():
    sentence = "I have always dreamed about becoming a hero"
    assert lem.lemmatize(sentence, "english") == ["-PRON-", "have", "always", "dream", "about", "become", "a", "hero"]

def test_english_label_orth():
    sentence = "*labelled label*"
    assert lem.lemmatize_orth(sentence, "english") == (["*", "label", "label", "*"], ["*", "labelled", "label", "*"])

def test_english_word_orth():
    word = "becoming"
    assert lem.lemmatize_orth(word, "english") == (["become"], ["becoming"])

def test_english_sentence_orth():
    sentence = "I have always dreamed about becoming a hero"
    assert lem.lemmatize_orth(sentence, "english") == (["-PRON-", "have", "always", "dream", "about", "become", "a", "hero"], ["I", "have", "always", "dreamed", "about", "becoming", "a", "hero"])
