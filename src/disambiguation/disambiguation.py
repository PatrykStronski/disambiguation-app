from services.neo4j_disambiguation import Neo4jDisambiguation
from utils.disambiguation import merge_into_dataframe
from utils.lemmatizer import Lemmatizer
import re

LANGUAGE_ALIAS = {
    "polish": "@pl",
    "english": "@en"
}

DISAMBIGUATION_THRESHOLD = 0.4
AMBIGUITY_LEVEL = 5

class Disambiguation:
    neo4j_mgr = None
    lemmatizer = Lemmatizer()

    def __init__(self):
        self.neo4j_mgr = Neo4jDisambiguation('neo4j')

    def get_words(self, text):
        words = re.split(r'\W+', text)
        return list(filter(None, words))

    def densest_subgraph(self, candidates):
        while True:
            candidates = self.calculate_semantic_interconnections(candidates)
            candidates = self.calculate_score(candidates)
            frequent_token = candidates.basic_form.value_counts()[:1].index.values[0]
            cand_set = candidates[candidates.basic_form == frequent_token]
            if cand_set.shape[0] <= AMBIGUITY_LEVEL:
                return candidates
            minimal_score = cand_set.score.min()
            candidates = candidates.drop(candidates[(candidates.score <= minimal_score) & (candidates.basic_form == frequent_token)].index)
        return candidates

    def filter_candidates(self, candidates):
        return candidates.loc[candidates.score >= DISAMBIGUATION_THRESHOLD]

    def calculate_sum_score(self, cand_set, token_nmb):
        if cand_set.empty:
            return 0
        return (cand_set["deg"] * cand_set["semantic_interconnections"] / token_nmb).sum()

    def calculate_entity_score(self, cand, sum_scores, token_number, token):
        deg = cand["deg"]
        sem_con = cand["semantic_interconnections"]
        if cand["basic_form"] != token:
            return cand
        cand.at["score"] = deg * sem_con / token_number / sum_scores
        return cand

    def calculate_score(self, candidates):
        tokens = candidates["basic_form"].unique()
        token_number = len(tokens) -1
        for token in tokens:
            sum_scores = self.calculate_sum_score(candidates.loc[candidates.basic_form == token], token_number)
            if sum_scores > 0:
                candidates = candidates.apply(
                    lambda cand: self.calculate_entity_score(cand, sum_scores, token_number, token), axis=1)
        return candidates

    def contains_uri(self, uri, semsign):
        if not semsign:
            return False
        return uri in semsign

    def count_interconnections_candidate(self, cand, candidates):
        uri = cand["uri"]
        token = cand["basic_form"]
        boolean_mask = candidates.sign.apply(lambda c: self.contains_uri(uri,c))
        semsign_children = candidates[boolean_mask]
        semsign_children = semsign_children[semsign_children.basic_form != token]
        cand.at["semantic_interconnections"] += semsign_children.shape[0]
        semsign_children["semantic_interconnections"] += 1 + semsign_children["semantic_interconnections"]
        return cand

    def count_interconnections_candidate_second(self, cand, candidates):
        uri = cand["uri"]
        uri_list = cand.sign
        if not uri_list:
            return cand
        include_mask = candidates.uri.isin(uri_list)
        include = candidates[include_mask]
        deduplicated_include = include.sign.apply(lambda c: not self.contains_uri(uri, c))
        include = include[deduplicated_include]
        cand["semantic_interconnections"] = cand["semantic_interconnections"] + include.shape[0]
        return cand

    def calculate_semantic_interconnections(self, candidates):
        candidates["semantic_interconnections"] = 0
        candidates = candidates.apply(lambda cand: self.count_interconnections_candidate(cand, candidates), axis=1)
        return candidates.apply(lambda cand: self.count_interconnections_candidate_second(cand, candidates), axis=1)

    def disambiguate_text(self, text, lang): #lang must be 'polish' or 'english'
        words = self.get_words(text)
        tokens = self.lemmatizer.lemmatize(" ".join(words), lang)
        candidates = merge_into_dataframe(words, tokens, [self.neo4j_mgr.find_word_regexp(word, LANGUAGE_ALIAS[lang]) for word in tokens])
        print(candidates.shape)
        if candidates.empty:
            return { "data": [] }
        candidates = self.densest_subgraph(candidates)
        candidates = self.filter_candidates(candidates)
        return {
            "data": candidates.to_dict("records")
        }
