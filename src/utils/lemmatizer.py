import spacy
import requests
import copy
import time
import ast
import json
import xmltodict

#spacy.prefer_gpu()

class Lemmatizer:
    nlp_en = None
    nlp_pl = None
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
        self.nlp_pl = spacy.load("pl_core_news_sm")

    def check_if_lemmatized(self, task_id):
        retries_used = 0
        while retries_used < self.MAX_RETRIES:
            time.sleep(0.1)
            retries_used += 1
            req = requests.get(self.URI_CHECKSTATUS + task_id)
            status = ast.literal_eval(req.text)
            if status.get("status") == "DONE":
                return status.get("value")[0].get("fileID")
        return False

    def download_extract_lemmatization(self, download_id):
        lemmatized_xml = requests.get(self.URI_GETLEMMATIZED + download_id)
        lemmatization_data = json.loads(json.dumps(xmltodict.parse(lemmatized_xml.text)))
        if type(lemmatization_data["chunkList"]["chunk"]["sentence"]["tok"]) is not list:
            return [lemmatization_data["chunkList"]["chunk"]["sentence"]["tok"].get("lex").get("base")]
        return [tok.get("lex").get("base") for tok in lemmatization_data["chunkList"]["chunk"]["sentence"]["tok"]]


    def lemmatize_pl(self, text):
        body =  copy.deepcopy(self.BODY_STARTTASK)
        body["text"] = text
        task_id = requests.post(self.URI_STARTTASK, data = json.dumps(body))
        download_id = self.check_if_lemmatized(task_id.text)
        if download_id is False:
            return text
        return self.download_extract_lemmatization(download_id)

    def lemmatize_en(self, text):
        doc = self.nlp_en(text)
        return [token.lemma_ for token in doc]

    def lemmatize(self, text, language):
        if language == "polish":
            return self.lemmatize_pl(text)
        return self.lemmatize_en(text)

    def lemmatize_detect_language(self, word):
        if word.endswith("@en"):
            return " ".join(self.lemmatize_en(word[:-3]))+"@en"
        elif word.endswith("@pl"):
            return " ".join(self.lemmatize_pl(word[:-3]))+"@pl"
        return word

    def lemmatize_labels(self, label_list = []):
        return [self.lemmatize_detect_language(word) for word in label_list]