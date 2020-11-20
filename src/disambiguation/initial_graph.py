import random
import pandas as pd

class InitialGraph:
    initial_node_uri = ""
    current_node_uri = ""
    initial_node_properties = {}
    node_visit_counts = pd.DataFrame()
    max_iterations = 0
    depth = 0
    iterations_level = 0
    threshold_visits = 1
    restart_probability = 0.0
    neo4j_mgr = None
    neo4j_new = None
    language = "all"
    depth_distribution = []

    def __init__(self, initial_node_uri, initial_node_properties, depth, threshold_visits, restart_probability, neo4j_mgr, neo4j_new):
        self.initial_node_uri = initial_node_uri
        self.current_node_uri = initial_node_uri
        self.initial_node_properties = initial_node_properties
        self.max_iterations = depth
        self.threshold_visits = threshold_visits
        self.restart_probability = restart_probability
        self.neo4j_mgr = neo4j_mgr
        self.neo4j_new = neo4j_new
        self.depth_distribution = [0] * 20
        self.language = self.extract_language()
        self.node_visit_counts = pd.DataFrame(columns = ["count", "node1", "node2", "relation"])

    def extract_language(self):
        preflabel = self.initial_node_properties.get("skos__prefLabel")
        if type(preflabel) is list:
            ispl = any("@pl" in label for label in preflabel)
            isen = any("@en" in label for label in preflabel)
            if ispl == True and isen == False:
                return "@pl"
            elif ispl == False and isen == True:
                return "@en"
        elif type(preflabel) is str:
            if "@pl" in preflabel:
                return "@pl"
            elif "@en" in preflabel:
                return "@en"
        return "all"

    def should_restart(self):
        probability = 1-((1-self.restart_probability)**self.depth)
        #print("Depth: " + str(self.depth) + " probability of restart: " + str(probability))
        rand = random.random()
        return rand <= probability

    def create_graph(self):
        self.random_walk_with_restart()

    def choose_relation(self, relations):
        return relations.sample(weights = relations["weight"].values).to_dict(orient = "records")[0]

    def increment_visits(self, picked_relation):
        existing_entry = self.node_visit_counts.loc[(self.node_visit_counts["node1"] == picked_relation["node1"]) & (self.node_visit_counts["node2"] == picked_relation["node2"])]
        if existing_entry.empty:
            self.node_visit_counts = self.node_visit_counts.append({ "count": 1, "journey_length": self.depth, "relation": picked_relation["relation"], "node1": picked_relation["node1"], "node2": picked_relation["node2"] }, ignore_index = True)
        else:
            self.node_visit_counts.loc[(self.node_visit_counts["node1"] == picked_relation["node1"]) & (self.node_visit_counts["node2"] == picked_relation["node2"]), ["count"]] += 1

    def random_walk_with_restart(self):
        if self.iterations_level >= self.max_iterations:
            strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
            return (strong_relations.shape[0], self.depth_distribution)
        if self.should_restart():
            self.depth = 0
            self.current_node_uri = self.initial_node_uri
        self.depth_distribution[self.depth] +=1
        relations = pd.DataFrame(self.neo4j_mgr.get_related_nodes_weighted(self.current_node_uri, self.language))
        if relations.empty:
            if self.current_node_uri == self.initial_node_uri:
                strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
                return (strong_relations.shape[0], self.depth_distribution)
            else:
                self.iterations_level += 1
                self.current_node_uri = self.initial_node_uri
                self.random_walk_with_restart()
                strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
                return (strong_relations.shape[0], self.depth_distribution)
        initial_node_in_vicinity = self.initial_node_uri in relations.node2
        self.depth += 1
        if initial_node_in_vicinity:
            self.depth = 1
        picked_relation = self.choose_relation(relations)
        self.increment_visits(picked_relation)
        self.current_node_uri = picked_relation["node2"]
        self.iterations_level += 1
        return self.random_walk_with_restart()

    def get_graph(self):
        strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
        print(strong_relations)

    def insert_graph(self):
        self.neo4j_new.create_node(self.initial_node_properties)
        strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
        [self.neo4j_new.create_relation(node1, node2, relations) for node1, node2, relations in zip(strong_relations["node1"], strong_relations["node2"], strong_relations["relation"])]