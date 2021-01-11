LANGUAGE_ALIAS = {
    "polish": "@pl",
    "english": "@en"
}
PHRASE_SEPARATOR = "*"

###LEMMATIZATION

SUPPORTED_LANGUAGES = ["polish", "english"]
SUPPORTED_LANGUAGES_SUFFIXES = ["@en", "@pl"]

###DISAMBIGUATION

DISAMBIGUATION_THRESHOLD = 0.2
AMBIGUITY_LEVEL = 5
CANDIDATES_FIELDS = ["word", "basic_form", "uri", "deg", "semantic_interconnections", "score", "sign", "labels"]
