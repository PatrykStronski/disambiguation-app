from disambiguation.disambiguation import Disambiguation
from utils.tsv_manager import read_input_data
import os
dis = Disambiguation(20, 0.05)

def test_disambiguation_both_simple():
    sentence_pl = "Opaska przewiązana przez jej włosy była koloru czerwonego"
    sentence_en = "The frontlet tied on her forehead was colored red"
    disambiguation_pl = dis.disambiguate_text(sentence_pl, "polish")["data"]
    disambiguation_en = dis.disambiguate_text(sentence_en, "english")["data"]
    assert len(disambiguation_pl) == 8
    assert disambiguation_pl[7]["uri"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/104114"
    assert len(disambiguation_en) == 9
    assert disambiguation_en[6]["uri"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/380378"
    assert disambiguation_en[7]["uri"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/368337"
    assert disambiguation_en[8]["uri"] == "http://plwordnet.pwr.wroc.pl/wordnet/synset/312334"


def test_disambiguation_pl():
    data_arr = read_input_data(os.getcwd() + '/tests/fixtures/test_file_pl.conll', 'conll')
    disambiguation_pl = []

    for data_set in data_arr:
        disambiguation_pl += dis.disambiguate_from_data(data_set, 'polish')

    assert len(disambiguation_pl) == 24