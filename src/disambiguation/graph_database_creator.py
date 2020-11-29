from disambiguation.initial_graph import InitialGraph
from services.neo4j_db import Neo4jDb
from services.redis_checker import RedisChecker
import time

class GraphDatabaseCreator:
    neo4j_mgr = None
    neo4j_new = None
    db_dest_uri = "neo4j://neo_dest:7687"
    db_src_uri = "neo4j://neo_src:7687"
    db_dest = "neo4j"
    db_src = "neo4j"
    max_depth = 0
    threshold_visits = 0
    restart_probability = 0.0
    def __init__(self, depth, threshold_visits, restart_probability):
        self.neo4j_mgr = Neo4jDb(self.db_src_uri, self.db_src)
        self.neo4j_new = Neo4jDb(self.db_dest_uri, self.db_dest)
        self.max_depth = depth
        self.threshold_visits = threshold_visits
        self.restart_probability = restart_probability
        self.redis_checker = RedisChecker()

    def add_depth_distributions(self, dist1, dist2):
        for ind in range(0,20):
            dist1[ind] += dist2[ind]
        return dist1

    def present_depth_distribution(self, dist, node_count):
        output = []
        for ind in range(0,20):
            output.append(str(ind) + ": " + str(dist[ind]/node_count))
        print("Journey length distribution: ")
        print("; ".join(output))

    def create_graph(self, start, end):
        sum_entries = 0
        sum_depth_distribution = [0] * 20
        for node_index in range(start, end):
            (node_uri, node_properties) = self.neo4j_mgr.get_node_by_index(node_index);
            print(node_uri)
            is_processed = self.redis_checker.get_processed_id(node_uri)
            if is_processed == "DONE":
                print("The node has already been processed. Carrying on...")
                continue
            init_graph = InitialGraph(node_uri, node_properties, self.max_depth, self.threshold_visits, self.restart_probability, self.neo4j_mgr, self.neo4j_new)
            ret = init_graph.random_walk_with_restart()
            self.redis_checker.insert_processed_id(node_uri)
            sum_depth_distribution = self.add_depth_distributions(sum_depth_distribution, ret[1])
            print("In SemSign " + str(ret[0]) + " Nodes")
            sum_entries += ret[0]
            #init_graph.get_graph()
            if node_index % 100 == 0:
                print("Graph creted for node " + str(node_index))
                if node_index % 2000 == 0:
                    del self.neo4j_mgr
                    del self.neo4j_new
                    del self.redis_checker
                    time.sleep(0.3)
                    self.neo4j_mgr = Neo4jDb(self.db_src_uri, self.db_src)
                    self.neo4j_new = Neo4jDb(self.db_dest_uri, self.db_dest)
                    self.redis_checker = RedisChecker()
            init_graph.insert_graph()
        print("Avg number of nodes: " + str(sum_entries/(end-start)))
        self.present_depth_distribution(sum_depth_distribution, end-start)
