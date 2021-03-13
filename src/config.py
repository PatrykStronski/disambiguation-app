LANGUAGE_ALIAS = {
    "polish": "@pl",
    "english": "@en"
}
PHRASE_SEPARATOR = "*"
DIRECTED_RELATIONS = True
DIRECTED_RELATIONS_ACCELERATION = True
CONCURRENT_RELATIONS_CREATION = 15

###LEMMATIZATION

SUPPORTED_LANGUAGES = ["polish", "english"]
SUPPORTED_LANGUAGES_SUFFIXES = ["@en", "@pl"]
SLEEP_TIME_LEMMATIZER = 0.2

###DISAMBIGUATION

DISAMBIGUATION_THRESHOLD = 0.00
AMBIGUITY_LEVEL = 30
CANDIDATES_FIELDS = ["order_id", "token_id", "orth", "lemma", "uri", "ctag", "from", "to", "wn_id", "pwn_id", "deg", "semantic_interconnections", "semantic_in_connections", "score", "sign", "labels"]
EXPORTED_FIELDS = ["token_id", "order_id", "orth", "lemma", "uri", "score", "labels", "pwn_id"]
POLEVAL_EXPORTED_FIELDS = ["order_id", "token_id", "orth", "lemma", "ctag", "from", "to", "wn_id"]
POLEVAL_EXPORTED_FIELDS_UP = ["ORDER_ID", "TOKEN_ID", "ORTH", "LEMMA", "CTAG", "FROM", "TO", "WN_ID"]
EXPORT_DIR = "/data/"
ENGLISH_PRINCETON_ONLY = True
SENTENCE_DISTINCTION = False

SEMEVAL_MAPPING = {
    "@id": "order_id",
    "@lemma": "lemma",
    "@pos": "ctag",
    "#text": "orth"
}

CONLL_DELIMITER = "\t"

BCOLORS = {
    "HEADER": '\033[95m',
    "OKBLUE": '\033[94m',
    "OKCYAN": '\033[96m',
    "OKGREEN": '\033[92m',
    "WARNING": '\033[93m',
    "FAIL": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m'
}
