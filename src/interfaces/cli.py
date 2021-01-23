from disambiguation.disambiguation import Disambiguation
from config import SUPPORTED_LANGUAGES
from utils.logger import Logger
from utils.tsv_manager import read_input_data, create_output_file
from utils.xml_manager import read_input_xml
from utils.json_manager import save_json
import pprint

Disamb = Disambiguation()
logger = Logger()

def xml_to_tsv(args):
    if len(args) < 5:
        logger.error("Wrong arguments, stopping...")
        return
    language = args[2]
    input_file = args[3]
    output_file = args[4]
    if language not in SUPPORTED_LANGUAGES:
        language = "english"
        logger.warning("default language is english")
    else:
        logger.debug("Disambiguating for " + language)
    input_data = read_input_xml(input_file)
    disambiguated = [Disamb.disambiguate_from_data(input_text, language) for input_text in input_data]
    create_output_file(output_file, disambiguated, "semeval-tsv")

def inline_to_json(args):
    if len(args) < 5:
        logger.error("Wrong arguments, stopping...")
        return
    language = args[2]
    out_file = args[3]
    text = args[4]
    if language not in SUPPORTED_LANGUAGES:
        language = "english"
        logger.warning("default language is english")
    else:
        logger.debug("Disambiguating for " + language)
    data = Disamb.disambiguate_text(text, language)
    save_json(data, out_file)

def inline(args):
    if len(args) < 4:
        logger.error("Wrong arguments, stopping...")
        return
    language = args[2]
    text = args[3]
    if language not in SUPPORTED_LANGUAGES:
        language = "english"
        logger.warning("default language is english")
    else:
        logger.debug("Disambiguating for " + language)
    pprint.pprint(Disamb.disambiguate_text(text, language))

def conll_export(args):
    if len(args) < 5:
        logger.error("Wrong arguments, stopping...")
        return
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

def initiate_cli(args):
    if len(args) >= 4:
        if args[1] == "conll-export":
            conll_export(args)
        elif args[1] == "inline":
            inline(args)
        elif args[1] == "inline-to-json":
            inline_to_json(args)
        elif args[1] == "xml-to-tsv":
            xml_to_tsv(args)
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
        pprint.pprint(Disamb.disambiguate_text(text, lang))

def disambiguate_std_file(text, lang="english", file = "out.conll"):
    disambiguated = Disamb.disambiguate_text(text, lange)
