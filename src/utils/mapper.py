import pandas as pd
from config import CANDIDATES_FIELDS, POLEVAL_EXPORTED_FIELDS, EXPORTED_FIELDS

def to_tsv(disambiguated):
    pass

def filter_output(data, is_test = False):
    if is_test:
        return [{ key: row[key] for key in POLEVAL_EXPORTED_FIELDS } for row in data]
    return [{ key: row[key] for key in EXPORTED_FIELDS } for row in data]

def extract_wn_id(uri):
    return "s"+str(uri.split('/')[-1])

def map_candidates(ind, t_id, word, token, cand_set):
    rows = []
    for cand in cand_set:
        rows.append({
            "order_id": ind,
            "token_id": t_id,
            "orth": word,
            "lemma": token,
            "uri": cand["uri"],
            "ctag": "",
            "wn_id": extract_wn_id(cand["uri"]),
            "from": -1,
            "to": -1,
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
    t_id = 0
    for ind in range(0,len(words)):
        to_insert_set = map_candidates(ind, t_id, words[ind], tokens[ind], candidate_sets[ind])
        if words[0] == ".":
            t_id = 0
        else:
            t_id += 1
        candidates = candidates.append(to_insert_set, ignore_index=True)
    return candidates