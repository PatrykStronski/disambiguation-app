LANGUAGE_ALIAS = {
    "polish": "@pl",
    "english": "@en"
}
PHRASE_SEPARATOR = "*"

###LEMMATIZATION

SUPPORTED_LANGUAGES = ["polish", "english"]
SUPPORTED_LANGUAGES_SUFFIXES = ["@en", "@pl"]
SLEEP_TIME_LEMMATIZER = 0.2

###DISAMBIGUATION

DISAMBIGUATION_THRESHOLD = 0.1
AMBIGUITY_LEVEL = 10
CANDIDATES_FIELDS = ["order_id", "token_id", "orth", "lemma", "uri", "ctag", "from", "to", "wn_id", "deg", "semantic_interconnections", "score", "sign", "labels"]
EXPORTED_FIELDS = ["order_id", "token_id", "orth", "lemma", "uri", "score", "labels"]
POLEVAL_EXPORTED_FIELDS = ["order_id", "token_id", "orth", "lemma", "ctag", "from", "to", "wn_id"]
POLEVAL_EXPORTED_FIELDS_UP = ["ORDER_ID", "TOKEN_ID", "ORTH", "LEMMA", "CTAG", "FROM", "TO", "WN_ID"]
EXPORT_DIR = "/data/"
IS_WEAK = False

CONLL_DELIMITER = "\t"

###COLORS
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
