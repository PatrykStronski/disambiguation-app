import * from neo4j_db
import random

def should_restart(restart_probability):
    rand = random.seed().random()
    return rand >= restart_probability

def calculate_weight(vertex1, vertex2):
    weight = 0
    weight += len(vertex1.edges)
    weight += len(vertex2.edges)
    return weight

def calculate_surrounding_weights(vertex):
    weight_sum = 0
    for edge in vertex.edges:
        weight_sum += calculate_weight(vertex, edge[1])
    return weight_sum

def probability(vertex1, vertex2):
    primary_edge_weight = calculate_weight(vertex1, vertex2)
    return 1.0 * primary_edge_weight / calculate_surrounding_weights(vertex)

def prepare_graph_for_node(ind, depth, threshold, restart_probability):
    start_node = neo4j_db.get_node_by_index(ind)
    base_nodes = [start_node]
    relations = []
    related_nodes = neo4j_db.get_related_nodes_uri(neo4j_db.get_uri_single_node(start_node))
    for level in range(depth):
        for current_node in base_nodes:
            if (len(related_nodes) == 0 || should_restart(restart_probability)):
                return start_node
            
    


def prepare_graph(depth, threshold, restart_probability):
    print("🏁 Preparation of graph started")
    node_qty = neo4j_db.get_number_of_nodes()
    for ind in range(node_qty):
        unit_graph = prepare_graph_for_node(ind, depth, threshold, restart_probability)
        print(unit_graph)
    print("🏁 Preparation of graph finished")

prepare_graph(4)
