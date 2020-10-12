import random
import pandas as pd

class InitialGraph:
    initial_node_uri = ""
    current_node_uri = ""
    node_visit_counts = pd.DataFrame()
    max_depth = 0
    depth_level = 0
    threshold_visits = 1
    restart_probability = 0.0
    neo4j_mgr = None
    neo4j_new = None

    def __init__(self, initial_node_uri, depth, threshold_visits, restart_probability, neo4j_mgr, neo4j_new):
        self.initial_node_uri = initial_node_uri
        self.current_node_uri = initial_node_uri
        self.max_depth = depth
        self.threshold_visits = threshold_visits
        self.restart_probability = restart_probability
        self.neo4j_mgr = neo4j_mgr
        self.neo4j_new = neo4j_new
        self.node_visit_counts = pd.DataFrame(columns = ["count", "node1", "node2", "relation"])

    def should_restart(self):
        rand = random.random()
        return rand <= self.restart_probability

    def create_graph(self):
        self.random_walk_with_restart()

    def choose_relation(self, relations):
        return relations.sample(weights = relations["probability"].values).to_dict(orient = "records")[0]

    def increment_visits(self, picked_relation):
        existing_entry = self.node_visit_counts.loc[(self.node_visit_counts["node1"] == picked_relation["node1"]) & (self.node_visit_counts["node2"] == picked_relation["node2"])]
        if existing_entry.empty:
            self.node_visit_counts = self.node_visit_counts.append({ "count": 1, "relation": picked_relation["relation"], "node1": picked_relation["node1"], "node2": picked_relation["node2"] }, ignore_index = True)
        else:
            self.node_visit_counts.loc[(self.node_visit_counts["node1"] == picked_relation["node1"]) & (self.node_visit_counts["node2"] == picked_relation["node2"]), ["count"]] += 1

    def random_walk_with_restart(self):
        if self.depth_level >= self.max_depth:
            return
        if self.should_restart():
            self.current_node_uri = self.initial_node_uri
        related_nodes = self.neo4j_mgr.get_related_nodes(self.current_node_uri)
        relation_weights = []
        weight_sum = 0
        for (node, relation) in related_nodes:
            weight = self.neo4j_mgr.get_triangle_weight(self.current_node_uri, node.get("uri"))
            weight_sum += weight
            relation_weights.append({ "weight": weight, "relation": (relation[0].type, relation[1].type), "node1": self.current_node_uri, "node2": node.get("uri") })
        relations = pd.DataFrame(relation_weights)
        relations["probability"] = relations["weight"] / weight_sum
        picked_relation = self.choose_relation(relations)
        self.increment_visits(picked_relation)
        self.current_node_uri = picked_relation["node2"]
        self.depth_level += 1
        self.random_walk_with_restart()

    def get_graph(self):
        strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
        print(strong_relations)

    def insert_graph(self):
        strong_relations = self.node_visit_counts.loc[self.node_visit_counts["count"] >= self.threshold_visits]
        #strong_relations.apply(lambda row: self.neo4j_new.create_relation(row["node1"], row["node2"], row["relation"]))