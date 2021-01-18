from disambiguation.disambiguation import Disambiguation
from config import SUPPORTED_LANGUAGES
from utils.logger import Logger
from utils.tsv_manager import read_input_data, create_output_file
import pprint

Disamb = Disambiguation()
logger = Logger()

def initiate_cli(args):
    if len(args) >= 4:
        if args[1] == "conll_export":
            language = args[2]
            input_file = args[3]
            output_file = args[4]
            if language not in SUPPORTED_LANGUAGES:
                language = "english"
                logger.warning("default language is english")
            else:
                logger.debug("Disambiguating for " + language)
            input_data = read_input_data(input_file, "conll")
            disambiguated = Disamb.disambiguate_from_data(input_data, language)
            create_output_file(output_file, disambiguated, "conll")
        elif args[1] == "inline":
            language = args[2]
            text = args[3]
            if language not in SUPPORTED_LANGUAGES:
                language = "english"
                logger.warning("default language is english")
            else:
                logger.debug("Disambiguating for " + language)
            pprint.pprint(Disamb.disambiguate_text(text, language))
    else:
        logger.debug("initiate endless CLI")
        initiate_infinite_cli()

def initiate_infinite_cli():
    while True:
        lang = input("Insert language: polish or english: ").strip()
        if lang != "polish" and lang != "english":
            logger.warning("default language - english")
            lang = "english"
        text = input("Provide text for disambiguation: ")
        logger.debug("Your disambiguation is on the way...")
        pprint.pprint(Disamb.disambiguate_text(text, lang))

def disambiguate_std(text, lang = "english"):
        pprint.pprint(Disamb.disambiguate_text(text, lang, True))

def disambiguate_std_file(text, lang="english", file = "out.conll"):
    disambiguated = Disamb.disambiguate_text(text, lang, True)
    to_tsv(disambiguated)