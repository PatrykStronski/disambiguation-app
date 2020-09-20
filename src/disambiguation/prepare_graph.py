import neo4j

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


