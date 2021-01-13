import random
import pandas as pd
import time
from config import SUPPORTED_LANGUAGES_SUFFIXES, SUPPORTED_LANGUAGES, LANGUAGE_ALIAS, PHRASE_SEPARATOR

class InitialGraph:
    initial_node_uri = ""
    current_node_uri = ""
    node_properties = {}
    node_visit_counts = pd.DataFrame()
    max_iterations = 0
    depth = 0
    iterations_level = 0
    threshold_visits = 1
    restart_probability = 0.0
    neo4j_src = None
    neo4j_new = None
    lemmatizer = None
    princeton = "all"

    def __init__(self, initial_node_uri, node_properties, depth, threshold_visits, restart_probability, neo4j_src, neo4j_new, lemmatizer):
        self.lemmatizer = lemmatizer
        self.initial_node_uri = initial_node_uri
        self.current_node_uri = initial_node_uri
        self.node_properties = self.prepare_language_labels(node_properties)
        self.max_iterations = depth
        self.threshold_visits = threshold_visits
        self.restart_probability = restart_probability
        self.neo4j_src = neo4j_src
        self.neo4j_new = neo4j_new
        self.time = time.time()
        self.princeton = self.extract_princeton()
        self.create_lemmatized_labels()
        self.node_visit_counts = pd.DataFrame(columns = ["count", "node2"])

    def prepare_language_labels(self, node_properties):
        for lang in SUPPORTED_LANGUAGES:
            node_properties["labels_" + lang] = ""
        return node_properties

    def has_language(self, label):
        for suffix in SUPPORTED_LANGUAGES_SUFFIXES:
            if label.endswith(suffix):
                return True
        return False

    def filter_labels_supported_lang(self, labels):
        return list(filter(self.has_language, labels))

    def filter_labels_lang(self, labels, lang):
        return list(filter(lambda label: label.endswith(LANGUAGE_ALIAS[lang]), labels))

    def detect_langauge(self, label):
        for lang in SUPPORTED_LANGUAGES:
            if label.endswith(LANGUAGE_ALIAS[lang]):
                return lang
        return None

    def lemmatize_labels_old(self):
        labels = []
        for prop in self.node_properties.keys():
            if "label" in prop.lower() and type(self.node_properties[prop]) is list:
                labels += self.lemmatizer.lemmatize_labels(self.filter_labels_lang(self.node_properties[prop]))
        return labels

    def create_lemmatized_labels(self):
        temporary_languages = {}
        for lang in SUPPORTED_LANGUAGES:
            temporary_languages[lang] = ""
        for prop in self.node_properties.keys():
            if "label" in prop.lower() and type(self.node_properties[prop]) is list:
                for label in self.node_properties[prop]:
                    language = self.detect_langauge(label)
                    if language:
                        temporary_languages[language] += label[:-3].lower() + " "
        for lang in SUPPORTED_LANGUAGES:
            if temporary_languages[lang]:
                self.node_properties["labels_" + lang] = " ".join(self.lemmatizer.lemmatize(temporary_languages[lang], lang, False))


    def extract_princeton(self):
        princeton = self.node_properties.get("princeton")
        if princeton:
            return "TRUE"
        if self.initial_node_uri.startswith("http://dbpedia.org/resource/"):
            return "ALL"
        return "FALSE"

    def should_restart(self):
        probability = 1-((1-self.restart_probability)**self.depth)
        rand = random.random()
        return rand <= probability

    def create_graph(self):
        self.random_walk_with_restart()

    def choose_relation(self, relations):
        return relations.sample(weights = relations["weight"].values).to_dict(orient = "records")[0]

    def increment_visits(self, picked_relation):
        existing_entry = self.node_visit_counts.loc[(self.node_visit_counts["node2"] == picked_relation["node2"])]
        if existing_entry.empty:
            self.node_visit_counts = self.node_visit_counts.append({ "count": 1, "journey_length": self.depth, "node2": picked_relation["node2"] }, ignore_index = True)
        else:
            self.node_visit_counts.loc[(self.node_visit_counts["node2"] == picked_relation["node2"]), ["count"]] += 1

    def random_walk_with_restart(self):
        if self.iterations_level >= self.max_iterations:
            return
        if self.should_restart():
            self.depth = 0
            self.current_node_uri = self.initial_node_uri

        #self.time = time.time()

        relations = pd.DataFrame(self.neo4j_src.get_related_nodes_weighted(self.current_node_uri, self.princeton, self.initial_node_uri), columns = ["node2", "weight"])
        if self.iterations_level == 0:
            self.node_properties["deg"] = relations.shape[0]

        #new_time = time.time()
        #print("Processing OF relations fetch:" + str(new_time - self.time))
        #self.time = new_time

        if relations.empty:
            if self.current_node_uri == self.initial_node_uri:
                return
            else:
                self.iterations_level += 1
                self.current_node_uri = self.initial_node_uri
                return self.random_walk_with_restart()
        initial_node_in_vicinity = self.initial_node_uri in relations.node2
        self.depth += 1
        if initial_node_in_vicinity:
            self.depth = 1
        picked_relation = self.choose_relation(relations)
        self.increment_visits(picked_relation)
        self.current_node_uri = picked_relation["node2"]
        self.iterations_level += 1

        #new_time = time.time()
        #print("Processing OF calculations PANDAS fetch:" + str(new_time - self.time))

        return self.random_walk_with_restart()

    def get_graph(self):
        strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
        print(strong_relations)

    def insert_graph(self):
        #self.time = time.time()
        self.neo4j_new.create_node(self.node_properties)
        strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
        self.neo4j_new.create_relation(self.initial_node_uri, strong_relations["node2"].values)
        #new_time = time.time()
        #print("Processing OF relation creation:" + str(new_time - self.time))
        #self.time = new_time
