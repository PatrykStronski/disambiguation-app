from math import isnan
from services.neo4j_disambiguation import Neo4jDisambiguation
from utils.mapper import merge_into_dataframe, filter_output, merge_with_data
from utils.lemmatizer import Lemmatizer
from config import DISAMBIGUATION_THRESHOLD, AMBIGUITY_LEVEL, CANDIDATES_FIELDS

class Disambiguation:
    neo4j_mgr = None
    lemmatizer = Lemmatizer()
    ambiguity_level = 0.0
    disambiguation_threshold = 0.0

    def __init__(self, ambiguity_lvl = AMBIGUITY_LEVEL, disambiguation_threshold = DISAMBIGUATION_THRESHOLD):
        self.neo4j_mgr = Neo4jDisambiguation('neo4j')
        self.ambiguity_level = ambiguity_lvl
        self.disambiguation_threshold = disambiguation_threshold

    def densest_subgraph(self, candidates):
        while True:
            frequent_token = candidates.lemma.value_counts()[:1].index.values[0]
            candidates = self.calculate_semantic_interconnections_lemma(candidates, frequent_token)
            candidates = self.calculate_score_lemma(candidates, frequent_token)
            cand_set = candidates[candidates.lemma == frequent_token]
            if cand_set.shape[0] <= self.ambiguity_level:
                return candidates
            minimal_score = cand_set.score.min()
            candidates = candidates.drop(candidates[(candidates.score <= minimal_score) & (candidates.lemma == frequent_token)].index)

    def filter_candidates(self, candidates):
        return candidates.loc[candidates.score >= self.disambiguation_threshold]

    def calculate_sum_score(self, cand_set, token_nmb):
        if cand_set.empty:
            return 0
        return (cand_set["deg"] * cand_set["semantic_interconnections"] / token_nmb).sum()

    def calculate_entity_score(self, cand, sum_scores, token_number, token):
        deg = cand["deg"]
        sem_con = cand["semantic_interconnections"]
        if cand["lemma"] != token:
            return cand
        cand.at["score"] = deg * sem_con / token_number / sum_scores
        return cand

    def calculate_score(self, candidates):
        tokens = candidates["lemma"].unique()
        token_number = len(tokens) -1
        for token in tokens:
            sum_scores = self.calculate_sum_score(candidates.loc[candidates.lemma == token], token_number)
            if sum_scores > 0:
                candidates = candidates.apply(
                    lambda cand: self.calculate_entity_score(cand, sum_scores, token_number, token), axis=1)
        return candidates

    def calculate_score_lemma(self, candidates, lemma):
        tokens = candidates["lemma"].unique()
        token_number = len(tokens) - 1
        sum_scores = self.calculate_sum_score(candidates.loc[candidates.lemma == lemma], token_number)
        if sum_scores > 0:
            candidates = candidates.apply(lambda cand: self.calculate_entity_score(cand, sum_scores, token_number, lemma), axis=1)
        return candidates

    def contains_uri(self, uri, semsign):
        if not semsign:
            return False
        return uri in semsign

    def check_value(self, val):
        if type(val) == float and isnan(val):
            return "_"
        return val

    def check_value_none(self, val):
        if not val:
            return "_"
        return val

    def align_output(self, candidates, input_data):
        out = []
        for ind, input_row in input_data.iterrows():
            token = input_row["lemma"]
            candidates_token = candidates.loc[candidates.lemma == token]
            if candidates_token.empty:
                empt = { key: self.check_value(input_row.get(key)) for key in CANDIDATES_FIELDS }
                out.append(empt)
            else:
                idx = candidates_token["score"].argmax()
                entr = { key: self.check_value(input_row.get(key)) for key in CANDIDATES_FIELDS }
                entr["pwn_id"] = candidates_token.iloc[idx]["pwn_id"]
                entr["wn_id"] = candidates_token.iloc[idx]["wn_id"]
                out.append(entr)
        return out

    def align_output_tokens(self, candidates, tokens, words):
        out = []
        for ind in range(0, len(tokens)):
            token = tokens[ind]
            candidates_token = candidates.loc[candidates.lemma == token]
            if candidates_token.empty:
                out.append({ "lemma": token, "orth": words[ind], "token_id": ind})
            else:
                idx = candidates_token["score"].argmax()
                chosen = candidates_token.iloc[idx].to_dict()
                out.append({ "lemma": token, "orth": words[ind], "token_id": ind, "uri": self.check_value_none(chosen["uri"]),
                             "labels": self.check_value_none(chosen["labels"]), "score": self.check_value_none(chosen["score"])})
        return out

    def count_interconnections_candidate(self, cand, candidates):
        """ This function aims on calculating semantic connections"""
        uri = cand["uri"]
        token = cand["lemma"]
        semsign = cand["sign"]
        candidates_different = candidates.loc[candidates.lemma != token]
        #calculate v' IN SemSign(v)
        boolean_mask = candidates_different.uri.apply(lambda c_uri: self.contains_uri(c_uri, semsign))
        connections_nmb_relates = candidates_different[boolean_mask].shape[0]
        cand.at["semantic_interconnections"] = connections_nmb_relates
        #calculate v IN SemSign(v')
        boolean_mask = candidates_different.sign.apply(lambda candidate_sign: self.contains_uri(uri, candidate_sign))
        connections_nmb_is_related = candidates_different[boolean_mask].shape[0]
        cand.at["semantic_in_connections"] = connections_nmb_is_related
        cand.at["deg"] = connections_nmb_is_related + connections_nmb_relates
        return cand

    def calculate_semantic_interconnections(self, candidates):
        candidates["semantic_interconnections"] = 0
        candidates["semantic_in_connections"] = 0
        return candidates.apply(lambda cand: self.count_interconnections_candidate(cand, candidates), axis=1)

    def calculate_semantic_interconnections_lemma(self, candidates, lemma):
        candidates["semantic_interconnections"] = 0
        candidates["semantic_in_connections"] = 0
        candidates["deg"] = 0
        return candidates.apply(lambda cand: self.count_interconnections_candidate(cand, candidates) if cand["lemma"] == lemma else cand, axis=1)

    def disambiguate_text(self, text, lang): #lang must be 'polish' or 'english'
        lemmatization_data = self.lemmatizer.lemmatize_orth(text, lang)
        tokens = lemmatization_data[0]
        words = lemmatization_data[1]
        candidates = merge_into_dataframe(words, tokens, [self.neo4j_mgr.find_word_labels(token, lang) for token in tokens])
        print(candidates.shape)
        if candidates.empty:
            return { "data": [] }
        candidates = self.densest_subgraph(candidates)
        candidates = self.calculate_semantic_interconnections(candidates)
        candidates = self.calculate_score(candidates)
        candidates = self.filter_candidates(candidates)
        proposed_candidates = self.align_output_tokens(candidates, tokens, words)
        return {
            "data": filter_output(proposed_candidates, False)
        }

    def disambiguate_from_data(self, input_data, lang):  # lang must be 'polish' or 'english'
        candidates = merge_with_data(input_data, [self.neo4j_mgr.find_word_labels(token, lang) for token in input_data["lemma"].tolist()])
        print(candidates.shape)
        if candidates.empty:
            return []
        candidates = self.densest_subgraph(candidates)
        candidates = self.calculate_semantic_interconnections(candidates)
        candidates = self.calculate_score(candidates)
        candidates = self.filter_candidates(candidates)
        proposed_candidates = self.align_output(candidates, input_data)
        if lang == "polish":
            return filter_output(proposed_candidates, True)
        else:
            return filter_output(proposed_candidates, False)
