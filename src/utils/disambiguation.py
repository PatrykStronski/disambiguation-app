import pandas as pd
from config import CANDIDATES_FIELDS


def map_candidates(word, token, cand_set):
    rows = []
    for cand in cand_set:
        rows.append({
            "word": word,
            "basic_form": token,
            "uri": cand["uri"],
            "deg": cand["deg"],
            "semantic_interconnections": 0,
            "score": 0.0,
            "sign": cand["sign"],
            "labels": cand["labels"]
        })
    return rows

def merge_into_dataframe(words, tokens, candidate_sets):
    if len(words) != len(tokens) or len(words) != len(candidate_sets):
        print("[ERROR] The amounts of tokens do not match!!!!")
    candidates = pd.DataFrame(columns=CANDIDATES_FIELDS)
    for ind in range(0,len(words)):
        to_insert_set = map_candidates(words[ind], tokens[ind], candidate_sets[ind])
        candidates = candidates.append(to_insert_set, ignore_index=True)
    return candidates