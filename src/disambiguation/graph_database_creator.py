from disambiguation.initial_graph import InitialGraph
from services.neo4j_db import Neo4jDb

class GraphDatabaseCreator:
    neo4j_mgr = None
    neo4j_new = None
    max_depth = 0
    threshold_visits = 0
    restart_probability = 0.0
    def __init__(self, depth, threshold_visits, restart_probability):
        self.neo4j_mgr = Neo4jDb("naivefull")
        self.neo4j_new = Neo4jDb("databaseuse2")
        self.max_depth = depth
        self.threshold_visits = threshold_visits
        self.restart_probability = restart_probability

    def create_graph(self, start, end):
        #print("Purge use database")
        #self.neo4j_new.purge()
        #print("Use database purged!")
        #node_count = self.neo4j_mgr.get_number_of_nodes()
        for node_index in range(start, end):
            (node_uri, node_properties) = self.neo4j_mgr.get_node_by_index(node_index);
            print(node_uri)
            init_graph = InitialGraph(node_uri, node_properties, self.max_depth, self.threshold_visits, self.restart_probability, self.neo4j_mgr, self.neo4j_new)
            init_graph.random_walk_with_restart()
            init_graph.get_graph()
            print("next")
            if node_index % 100 == 0:
                print("Graph creted for node " + str(node_index))
            init_graph.insert_graph()

