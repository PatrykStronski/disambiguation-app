from disambiguation.disambiguation import Disambiguation
import pprint

Disamb = Disambiguation()

def initiate_cli():
    while True:
        lang = input("Insert language: polish or english: ")
        if lang != "polish" or lang != "english":
            print("default language - english")
            lang = "english"
        text = input("Provide text for disambiguation: ")
        print("Your disambiguation is on the way")
        pprint.pprint(Disamb.disambiguate_text(text, lang))