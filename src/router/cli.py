from disambiguation.disambiguation import Disambiguation
from utils.mapper import to_tsv
from config import BCOLORS, SUPPORTED_LANGUAGES
import pprint


Disamb = Disambiguation()

def debug(text):
    print(BCOLORS["OKCYAN"] + text + BCOLORS["ENDC"])

def successful(text):
    print(BCOLORS["OKGREEN"] + text + BCOLORS["ENDC"])

def warning(text):
    print(BCOLORS["WARNING"] + text + BCOLORS["ENDC"])

def initiate_cli(args):
    if len(args) >= 4:
        if args[1] == "conll_export":
            language = args[2]
            text = args[3]
            file_name = args[4]
            if language not in SUPPORTED_LANGUAGES:
                language = "english"
                warning("default language is english")
            else:
                debug("Disambiguating for " + language)
            disambiguated = Disamb.disambiguate_text(text, language, True)
            to_tsv(disambiguated, file_name)
        elif args[1] == "inline":
            language = args[2]
            text = args[3]
            if language not in SUPPORTED_LANGUAGES:
                language = "english"
                warning("default language is english")
            else:
                debug("Disambiguating for " + language)
            pprint.pprint(Disamb.disambiguate_text(text, language))
    else:
        debug("initiate endless CLI")
        initiate_infinite_cli()

def initiate_infinite_cli():
    while True:
        lang = input("Insert language: polish or english: ").strip()
        if lang != "polish" and lang != "english":
            print("default language - english")
            lang = "english"
        text = input("Provide text for disambiguation: ")
        print("Your disambiguation is on the way...")
        pprint.pprint(Disamb.disambiguate_text(text, lang))

def disambiguate_std(text, lang = "english"):
        pprint.pprint(Disamb.disambiguate_text(text, lang, True))

def disambiguate_std_file(text, lang="english", file = "out.conll"):
    disambiguated = Disamb.disambiguate_text(text, lang, True)
    to_tsv(disambiguated)
