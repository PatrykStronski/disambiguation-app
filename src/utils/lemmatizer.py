import spacy
import requests
import copy
import time
import ast
import json
import xmltodict

class Lemmatizer:
    nlp_en = None
    URI_STARTTASK = "https://ws.clarin-pl.eu/nlprest2/base/startTask/"
    BODY_STARTTASK = {
        "application": "ws.clarin-pl.eu",
        "lpmn": 'any2txt|morphoDita({"guesser":false, "allforms":false, "model":"XXI"})',
        "text": "<sample string>",
        "user": "242564@student.pwr.edu.pl"
    }
    MAX_RETRIES = 50
    URI_CHECKSTATUS = "https://ws.clarin-pl.eu/nlprest2/base/getStatus/"
    URI_GETLEMMATIZED = "https://ws.clarin-pl.eu/nlprest2/base/download"

    def __init__(self):
        self.nlp_en = spacy.load("en_core_web_sm")

    def check_if_lemmatized(self, task_id):
        retries_used = 0
        while retries_used < self.MAX_RETRIES:
            time.sleep(0.2)
            retries_used += 1
            req = requests.get(self.URI_CHECKSTATUS + task_id)
            status = ast.literal_eval(req.text)
            if status.get("status") == "DONE":
                return status.get("value")[0].get("fileID")
        return False

    def mark_unneeded_part_pl(self, label, should_mark = False):
        base = label.get("base")
        if not should_mark:
            return base
        ctag = label.get("ctag")
        if ctag and ctag.startswith("prep:"):
            return "-PREP-"
        elif ctag and ctag == "interp":
            return "-INTERP-"
        elif ctag and ctag.startswith("ppron"):
            return "-PPRON-"
        elif ctag and ctag.startswith("aglt"):
            return "-AGLT-"
        elif ctag and ctag.startswith("conj"):
            return "-CONJ-"
        elif ctag and ctag.startswith("conj"):
            return "-CONJ-"
        elif ctag and ctag.startswith("comp"):
            return "-COMP-"
        elif ctag and ctag.startswith("qub"):
            return "-QUB-"
        return base

    def mark_unneeded_part_en(self, lemma, pos):
        if pos == "ADP" or pos == "DET":
            return "-"+pos+"-"
        return lemma

    def download_extract_lemmatization(self, download_id, should_mark):
        lemmatized_xml = requests.get(self.URI_GETLEMMATIZED + download_id).text
        if '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">' in lemmatized_xml:
            print("retry 1 for lemmatization")
            time.sleep(0.2)
            lemmatized_xml = requests.get(self.URI_GETLEMMATIZED + download_id).text
            if '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">' in lemmatized_xml:
                print("retry 2 for lemmatization")
                time.sleep(0.2)
                lemmatized_xml = requests.get(self.URI_GETLEMMATIZED + download_id).text
        lemmatization_data = json.loads(json.dumps(xmltodict.parse(lemmatized_xml)))
        if type(lemmatization_data["chunkList"]["chunk"]["sentence"]["tok"]) is not list:
            return [self.mark_unneeded_part_pl(lemmatization_data["chunkList"]["chunk"]["sentence"]["tok"].get("lex"), should_mark)]
        return [self.mark_unneeded_part_pl(tok.get("lex"), should_mark) for tok in lemmatization_data["chunkList"]["chunk"]["sentence"]["tok"]]


    def lemmatize_pl(self, text, should_mark = False):
        body =  copy.deepcopy(self.BODY_STARTTASK)
        body["text"] = text
        task_id = requests.post(self.URI_STARTTASK, data = json.dumps(body))
        download_id = self.check_if_lemmatized(task_id.text)
        if download_id is False:
            return text
        return self.download_extract_lemmatization(download_id, should_mark)

    def lemmatize_en(self, text, mark_unneeded = False):
        doc = self.nlp_en(text)
        if not mark_unneeded:
            return [token.lemma_ for token in doc]
        return [self.mark_unneeded_part_en(token.lemma_, token.pos_) for token in doc]

    def lemmatize(self, text, language, mark_unneeded = False):
        if language == "polish":
            return self.lemmatize_pl(text, mark_unneeded)
        return self.lemmatize_en(text, mark_unneeded)

    def lemmatize_detect_language(self, word):
        """ This method can only be used  by initial graph"""
        if len(word.split(' ')) < 2:
            return word
        if word.endswith("@en"):
            return " ".join(self.lemmatize_en(word[:-3]))+"@en"
        elif word.endswith("@pl"):
            return " ".join(self.lemmatize_pl(word[:-3]))+"@pl"
        return word

    def lemmatize_labels(self, label_list = []):
        return [self.lemmatize_detect_language(word) for word in label_list]