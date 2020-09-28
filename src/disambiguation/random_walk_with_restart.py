import sys
sys.path.append('../services/')
import neo4j_db
import random

def should_restart(restart_probability):
    rand = random.seed().random()
    return rand >= restart_probability

# weight depicts what cardinality has the graph which is introduced by the relation
def calculate_weight(base_node, node2):
    return neo4j_db.get_relation_cardinality(base_node, node2) + 1

def weight_sum(relations):
    overall_weight = 0
    for rel in relations:
        overall_weight += rel["weight"]
    return overall_weight

def extract_strong_relations(relations, threshold_probability):
    return list(filter(lambda rel: rel["cardinality"] > threshold_probability, relations))

def get_relations_probabilities(current_node, related_nodes):
    relation_weights = []
    for related_node in related_nodes:
        rel = neo4j_db.get_relation(current_node, related_node)
        print(rel)
        if (rel):
            relation_weights.append({ "relation": rel, "weight": calculate_weight(current_node, related_node) })
    overall_weight = weight_sum(relation_weights)
    return [{ "relation": weight["relation"], "probability": weight["weight"]/overall_weight } for weight in relation_weights]

# relation entry in relations should be of format: {relation: Rel(in neo4j format), probability: number}
def prepare_graph_for_node(ind, depth, threshold_probability, restart_probability):
    start_node = neo4j_db.get_node_by_index(ind)
    base_nodes = [start_node]
    relations = []
    for level in range(depth):
        related_nodes = []
        for current_node in base_nodes:
            related_nodes = neo4j_db.get_related_nodes(current_node)
            print(related_nodes)
            if (len(related_nodes) == 0):
                continue
            #if (len(related_nodes) == 0 || should_restart(restart_probability)):
            #    return extract_strong_relations(relations, threshold_probability)
            relations = relations + get_relations_probabilities(current_node, related_nodes)
            print(relations)
        base_nodes = related_nodes
    return extract_strong_relations(relations, threshold_probability)

def prepare_graph(depth, threshold_probability, restart_probability):
    print("🏁 Preparation of graph started")
    node_qty = neo4j_db.get_number_of_nodes()
    for ind in range(1,node_qty):
        unit_graph = prepare_graph_for_node(ind, depth, threshold_probability, restart_probability)
        print("Graph for " + str(ind) + " done")
        print(unit_graph)
    print("🏁 Preparation of graph finished")

prepare_graph(3, 0.2, 0.2)
