from disambiguation.disambiguation import Disambiguation

Disamb = Disambiguation()

def initiate_cli():
    while True:
        lang = input("Insert language: polish or english")
        if lang != "polish":
            lang = "english"
        text = input("Provide text for disambiguation")
        print("Your disambiguation is on the way")
        print(Disamb.disambiguate_text(text, lang))