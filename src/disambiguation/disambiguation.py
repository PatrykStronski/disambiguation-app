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
            cand_set = candidates[candidates.lemma == frequent_token]
            if cand_set.shape[0] <= self.ambiguity_level:
                return candidates
            minimal_score = cand_set.score.min()
            candidates = candidates.drop(candidates[(candidates.score <= minimal_score) & (candidates.lemma == frequent_token)].index)
        return candidates

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

    def contains_uri(self, uri, semsign):
        if not semsign:
            return False
        return uri in semsign

    def align_output(self, candidates, tokens):
        out = []
        ind = 0
        for token in tokens:
            candidates_token = candidates[candidates.lemma == token]
            if candidates_token.empty:
                empt = { key: "N#A" for key in CANDIDATES_FIELDS }
                empt["lemma"] = token
                empt["token_id"] = ind
                out.append(empt)
            else:
                idx = candidates_token["score"].argmax()
                out.append(candidates.iloc[idx].to_dict())
            ind += 1
        return out

    def count_interconnections_candidate(self, cand, candidates):
        uri = cand["uri"]
        token = cand["lemma"]
        boolean_mask = candidates.sign.apply(lambda c: self.contains_uri(uri,c))
        semsign_children = candidates[boolean_mask]
        semsign_children = semsign_children[semsign_children.lemma != token]
        cand.at["semantic_interconnections"] += semsign_children.shape[0]
        semsign_children["semantic_interconnections"] += 1 + semsign_children["semantic_interconnections"]
        return cand

    def calculate_semantic_interconnections(self, candidates):
        candidates["semantic_interconnections"] = 0
        return candidates.apply(lambda cand: self.count_interconnections_candidate(cand, candidates), axis=1)

    def disambiguate_text(self, text, lang, is_test = False): #lang must be 'polish' or 'english'
        tokens = self.lemmatizer.lemmatize(text, lang, False)
        candidates = merge_into_dataframe(tokens, tokens, [self.neo4j_mgr.find_word_labels(token, lang) for token in tokens])
        print(candidates.shape)
        if candidates.empty:
            return { "data": [] }
        candidates = self.calculate_semantic_interconnections(candidates)
        candidates = self.calculate_score(candidates)
        candidates = self.filter_candidates(candidates)
        candidates = self.densest_subgraph(candidates)
        proposed_candidates = self.align_output(candidates, tokens)
        return {
            "data": filter_output(proposed_candidates, is_test)
        }

    def disambiguate_from_data(self, input_data, lang):  # lang must be 'polish' or 'english'
        candidates = merge_with_data(input_data, [self.neo4j_mgr.find_word_labels(token, lang) for token in input_data["lemma"].values()])
        print(candidates.shape)
        if candidates.empty:
            return {"data": []}
        candidates = self.calculate_semantic_interconnections(candidates)
        candidates = self.calculate_score(candidates)
        candidates = self.filter_candidates(candidates)
        candidates = self.densest_subgraph(candidates)
        proposed_candidates = self.align_output(candidates, tokens)
        return {
            "data": filter_output(proposed_candidates, True)
        }
