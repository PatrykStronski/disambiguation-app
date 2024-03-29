import xmltodict
import json
from config import SENTENCE_DISTINCTION, CANDIDATES_FIELDS, EXPORT_DIR, SEMEVAL_MAPPING
import pandas as pd

def default(val = ""):
    return val

def map_sentence(sentence, text_df):
    for word in sentence["wf"]:
        word_mapped = { SEMEVAL_MAPPING[key]: default(word.get(key)) for key in SEMEVAL_MAPPING }
        text_df = text_df.append(word_mapped, ignore_index=True)
    return text_df

def map_xml_semeval(data):
    parsed = []
    for text in  data["corpus"]["text"]:
        text_df = pd.DataFrame(columns=CANDIDATES_FIELDS)
        if type(text["sentence"]) == list:
            for sent in text["sentence"]:
                text_df = map_sentence(sent, text_df)
        else:
            text_df = map_sentence(text["sentence"], text_df)
        parsed.append(text_df)
    return parsed

def map_xml_semeval_sentences(data):
    parsed = []
    for text in data["corpus"]["text"]:
        if type(text["sentence"]) == list:
            for sent in text["sentence"]:
                parsed.append(map_sentence(sent, pd.DataFrame(columns=CANDIDATES_FIELDS)))
        else:
            parsed.append(map_sentence(text["sentence"], pd.DataFrame(columns=CANDIDATES_FIELDS)))
    return parsed

def read_input_xml(filename):
    xml_file = open(EXPORT_DIR + filename)
    xml = xml_file.read()
    xml_parsed = json.loads(json.dumps(xmltodict.parse(xml)))
    if SENTENCE_DISTINCTION:
        return map_xml_semeval_sentences(xml_parsed)
    return map_xml_semeval(xml_parsed)