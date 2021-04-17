from utils.mapper import merge_with_data
from services.neo4j_disambiguation import Neo4jDisambiguation
from utils.tsv_manager import read_input_data
import os


def count_candidate_number(cand_set):
    nmb = 0
    for set in cand_set:
        nmb += len(set)
    return nmb


def test_simple_data_for_quantity():
    data_arr = read_input_data(os.getcwd() + '/tests/fixtures/test_file_pl.conll', 'conll')
    entry_count = 0
    candidate_set_counts = 0
    candidate_meanings_count = 0
    neo4j_mgr = Neo4jDisambiguation('neo4j')

    for data_part in data_arr:
        candidate_sets = [neo4j_mgr.find_word_labels(token, 'polish') for token in data_part["lemma"].tolist()]
        candidate_set_counts += len(candidate_sets)
        candidate_meanings_count += count_candidate_number(candidate_sets)
        merged = merge_with_data(data_part, candidate_sets)
        entry_count += merged.shape[0]

    assert candidate_set_counts == 24
    assert entry_count == candidate_meanings_count
