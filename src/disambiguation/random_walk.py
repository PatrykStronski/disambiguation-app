import random
import pandas as pd
from config import SUPPORTED_LANGUAGES, LANGUAGE_ALIAS, PHRASE_SEPARATOR, DIRECTED_RELATIONS, DIRECTED_RELATIONS_ACCELERATION

class RandomWalk:
    initial_node_uri = ""
    current_node_uri = ""
    node_properties = {}
    node_visit_counts = pd.DataFrame()
    max_iterations = 0
    depth = 0
    iterations_count = 0
    threshold_visits = 1
    restart_probability = 0.0
    neo4j_src = None
    neo4j_new = None
    lemmatizer = None
    princeton = "all"

    def __init__(self, initial_node_uri, node_properties, max_iterations, threshold_visits, restart_probability, neo4j_src, neo4j_new, lemmatizer):
        self.lemmatizer = lemmatizer
        self.polish_lemmatization_code = None
        self.initial_node_uri = initial_node_uri
        self.current_node_uri = initial_node_uri
        self.node_properties = self.prepare_language_labels(node_properties)
        self.max_iterations = max_iterations
        self.threshold_visits = threshold_visits
        self.restart_probability = restart_probability
        self.neo4j_src = neo4j_src
        self.neo4j_new = neo4j_new
        self.princeton = self.extract_princeton()
        self.create_lemmatized_labels()
        self.node_visit_counts = pd.DataFrame(columns = ["count", "node2"])

    def prepare_language_labels(self, node_properties):
        for lang in SUPPORTED_LANGUAGES:
            node_properties["labels_" + lang] = ""
        return node_properties

    def detect_langauge(self, label):
        for lang in SUPPORTED_LANGUAGES:
            if label.endswith(LANGUAGE_ALIAS[lang]):
                return lang
        return None

    def align_labels(self, labels):
        joined = " ".join(labels)
        return joined.replace(PHRASE_SEPARATOR+" ", PHRASE_SEPARATOR).replace(" "+PHRASE_SEPARATOR, PHRASE_SEPARATOR)

    def extract_labels(self, temporary_languages, prop):
        if "label" in prop.lower() and type(self.node_properties[prop]) is list:
            for label in self.node_properties[prop]:
                language = self.detect_langauge(label)
                if language:
                    if " " in label:
                        temporary_languages[language + "_lemmatize"] += PHRASE_SEPARATOR + label[:-3].lower() + PHRASE_SEPARATOR
                    else:
                        temporary_languages[language] += PHRASE_SEPARATOR + label[:-3].lower() + PHRASE_SEPARATOR
        return temporary_languages

    def get_lemmatized_trigger_lemmatization(self, temporary_languages, lang):
        self.node_properties["labels_" + lang] = ""

        if temporary_languages[lang]:
            self.node_properties["labels_" + lang] += "".join(temporary_languages[lang])

        if temporary_languages[lang + "_lemmatize"]:
            if lang != "polish":
                self.node_properties["labels_" + lang] += self.align_labels(
                    self.lemmatizer.lemmatize(temporary_languages[lang + "_lemmatize"], lang, False))
            else:
                self.polish_lemmatization_code = self.lemmatizer.lemmatizer_initiate_task(
                    temporary_languages["polish_lemmatize"])

    def create_lemmatized_labels(self):
        temporary_languages = {}

        for lang in SUPPORTED_LANGUAGES:
            temporary_languages[lang] = ""
            temporary_languages[lang+"_lemmatize"] = ""

        for prop in self.node_properties.keys():
            temporary_languages = self.extract_labels(temporary_languages, prop)

        for lang in SUPPORTED_LANGUAGES:
            self.get_lemmatized_trigger_lemmatization(temporary_languages, lang)

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

    def increment_visits(self, picked_node):
        existing_entry = self.node_visit_counts.loc[(self.node_visit_counts["node2"] == picked_node)]
        if existing_entry.empty:
            self.node_visit_counts = self.node_visit_counts.append({ "count": 1, "node2": picked_node }, ignore_index = True)
        else:
            self.node_visit_counts.loc[(self.node_visit_counts["node2"] == picked_node), ["count"]] += 1

    def random_walk_with_restart(self):
        if self.iterations_count >= self.max_iterations:
            return
        if self.should_restart():
            self.depth = 0
            self.iterations_count += 1
            self.current_node_uri = self.initial_node_uri

        is_directed = DIRECTED_RELATIONS

        relations = pd.DataFrame(self.neo4j_src.get_related_nodes_weighted(self.current_node_uri, self.princeton, self.initial_node_uri, is_directed), columns = ["node2", "weight"])

        if relations.empty and DIRECTED_RELATIONS_ACCELERATION and is_directed:
            print("Accelerate choice")
            is_directed = False
            relations = pd.DataFrame(self.neo4j_src.get_related_nodes_weighted(self.current_node_uri, self.princeton, self.initial_node_uri, is_directed), columns = ["node2", "weight"])

        if relations.empty:
            if self.current_node_uri == self.initial_node_uri:
                return
            else:
                self.iterations_count += 1
                self.current_node_uri = self.initial_node_uri
                return self.random_walk_with_restart()
        self.depth += 1

        next_node = self.choose_relation(relations)["node2"]
        if next_node == self.initial_node_uri:
            self.depth = 0
        self.increment_visits(next_node)
        self.current_node_uri = next_node
        self.iterations_count += 1

        return self.random_walk_with_restart()

    def get_graph(self):
        strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
        return strong_relations

    def insert_graph(self):
        if self.polish_lemmatization_code:
            self.node_properties["labels_polish"] += self.align_labels(self.lemmatizer.download_lemmatization(self.polish_lemmatization_code, PHRASE_SEPARATOR)[0])
        self.neo4j_new.create_node(self.node_properties)
        strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
        self.neo4j_new.create_relations(self.initial_node_uri, strong_relations["node2"].values)
