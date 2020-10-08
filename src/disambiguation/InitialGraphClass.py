import random

class InitialGraph:
    initial_node = None
    current_node = None
    node_visit_counts = []
    max_depth = 0
    depth_level = 0
    threshold_visits = 1
    restart_probability = 0.0
    neo4j_mgr = None

    def __init__(self, initial_node, depth, threshold_visits, restart_probability, neo4j_mgr):
        self.initial_node = initial_node
        self.current_node = initial_node
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
        sorted_relations = sorted(relations, key = lambda rel: rel["probability"])
        prob_counter = 0.0
        relation_picker_vector = []
        for rel in sorted_relations:
            prob_counter += rel["probability"]
            relation_picker_vector.append({ "max_probability": prob_counter, "relation": { "relation": rel["relation"], "node2": rel["node2"] }})
        rand = random.random()
        for rel in relation_picker_vector:
            if rand < rel["max_probability"]:
                return rel["relation"]
        return None

    def increment_visits(self, picked_relation):
        for count in self.node_visit_counts:
            if count["relation"] == picked_relation["relation"] and count["node2"] == picked_relation["node2"] and count["node1"] == self.current_node:
                count["count"] += 1
                return None
        self.node_visit_counts.append({ "count": 1, "relation": picked_relation["relation"], "node1": self.current_node, "node2": picked_relation["node2"] })

    def random_walk_with_restart(self):
        if self.depth_level >= self.max_depth:
            return
        self.depth_level += 1
        if self.should_restart():
            self.current_node = self.initial_node
            return self.random_walk_with_restart()
        related_nodes = self.neo4j_mgr.get_related_nodes(self.current_node)
        relation_weights = []
        weight_sum = 0 
        for node in related_nodes:
            relation = self.neo4j_mgr.get_relation(self.current_node, node)
            weight = self.neo4j_mgr.get_triangle_weight(self.current_node, node)
            weight_sum += weight
            relation_weights.append({ "weight": weight, "relation": relation, "node2": node, "probability": 0.0 })
        for relation in relation_weights:
            relation["probability"] = relation["weight"]/weight_sum
        picked_relation = self.choose_relation(relation_weights)
        self.increment_visits(picked_relation)
        self.current_node = picked_relation["node2"]
        self.random_walk_with_restart()

    def get_graph(self):
        print(self.extract_strong_relations())
