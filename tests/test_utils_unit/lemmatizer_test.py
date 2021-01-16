from utils.lemmatizer import Lemmatizer

lem = Lemmatizer()

def test_polish_word():
    word = "robiłem"
    assert lem.lemmatize_pl(word) == ["robić", "być"]

def test_polish_word():
    word = "mała"
    assert lem.lemmatize_pl(word) == ["mały"]

def test_polish_label_multiword():
    label = "*ometkowana metka*"
    assert lem.lemmatize(label, "polish", False) == ["*", "ometkować", "metka", "*"]

def test_polish_sentence():
    word = "Ja robiłem dużo zadań."
    assert lem.lemmatize_pl(word) == ["ja", "robić", "być", "dużo", "zadanie", "."]

#def test_polish_sentence_interp():
#    word = "Ja robiłem dużo zadań."
#    assert lem.lemmatize_pl(word, True) == ["-PPRON-", "robić", "-AGLT-", "dużo", "zadanie", "-INTERP-"]

#def test_polish_sentence_prep():
#    word = "Ja robiłem dużo zadań w domu po szkole."
#    assert lem.lemmatize_pl(word, True) == ["-PPRON-", "robić", "-AGLT-", "dużo", "zadanie", "-PREP-", "dom", "-PREP-", "szkoła", "-INTERP-"]

def test_polish_sentence_prep_default():
    word = "Ja robiłem dużo zadań w domu po szkole."
    assert lem.lemmatize_pl(word) == ["ja", "robić", "być", "dużo", "zadanie", "w", "dom", "po", "szkoła", "."]

def test_english_label():
    sentence = "*labelled label*"
    assert lem.lemmatize(sentence, "english", False) == ["*", "label", "label", "*"]

def test_english_word():
    word = "becoming"
    assert lem.lemmatize_en(word) == ["become"]

def test_english_sentence():
    sentence = "I have always dreamed about becoming a hero"
    assert lem.lemmatize_en(sentence) == ["-PRON-", "have", "always", "dream", "about", "become", "a", "hero"]
