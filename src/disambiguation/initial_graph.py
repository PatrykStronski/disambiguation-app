import random
import pandas as pd

class InitialGraph:
    initial_node_uri = ""
    current_node_uri = ""
    node_visit_counts = pd.DataFrame(columns = ["count", "node1", "node2", "relation"])
    max_depth = 0
    depth_level = 0
    threshold_visits = 1
    restart_probability = 0.0
    neo4j_mgr = None

    def __init__(self, initial_node_uri, depth, threshold_visits, restart_probability, neo4j_mgr):
        self.initial_node_uri = initial_node_uri
        self.current_node_uri = initial_node_uri
        self.max_depth = depth
        self.threshold_visits = threshold_visits
        self.restart_probability = restart_probability
        self.neo4j_mgr = neo4j_mgr

    def should_restart(self):
        rand = random.random()
        return rand <= self.restart_probability

    def extract_strong_relations(self):
        strong_relations = filter(lambda visit_count: visit_count["count"] >= self.threshold_visits, self.node_visit_counts)
        return [{ "node1": rel["node1"], "node2": rel["node2"], "relation": rel["relation"] } for rel in strong_relations]

    def create_graph(self):
        self.random_walk_with_restart()

    def choose_relation(self, relations):
        return relations.sample(weights = relations["probability"].values).to_dict(orient = "records")[0]

    def increment_visits(self, picked_relation):
        existing_entry = self.node_visit_counts.loc[(self.node_visit_counts["node1"] == picked_relation["node1"]) & (self.node_visit_counts["node2"] == picked_relation["node2"])]
        print(existing_entry)
        if existing_entry.empty:
            return self.node_visit_counts.append({ "count": 1, "relation": picked_relation["relation"], "node1": picked_relation["node1"], "node2": picked_relation["node2"] }, ignore_index = True)
        existing_entry["count"] += 1


    def check_return_cases(self):
        if self.depth_level >= self.max_depth:
            return True
        if self.should_restart():
            self.current_node_uri = self.initial_node_uri
            self.random_walk_with_restart()
            return True
        return False

    def random_walk_with_restart(self):
        self.depth_level += 1
        if self.check_return_cases() is True:
            return
        related_nodes = self.neo4j_mgr.get_related_nodes(self.current_node_uri)
        if not related_nodes:
            if self.current_node_uri == self.initial_node_uri:
                return
            self.current_node_uri = self.initial_node_uri
            return self.random_walk_with_restart()
        relation_weights = []
        weight_sum = 0 
        for node in related_nodes:
            relation = self.neo4j_mgr.get_relation(self.current_node_uri, node.get("uri"))
            weight = self.neo4j_mgr.get_triangle_weight(self.current_node_uri, node.get("uri"))
            weight_sum += weight
            relation_weights.append({ "weight": weight, "relation": (relation[0].type, relation[1].type), "node1": self.current_node_uri, "node2": node.get("uri") })
        relations = pd.DataFrame(relation_weights)
        relations["probability"] = relations["weight"] / weight_sum
        picked_relation = self.choose_relation(relations)
        self.increment_visits(picked_relation)
        self.current_node_uri = picked_relation["node2"]
        self.random_walk_with_restart()

    def get_graph(self):
        print(self.extract_strong_relations())
