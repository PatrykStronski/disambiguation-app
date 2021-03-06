from disambiguation.random_walk import RandomWalk
from services.neo4j_db import Neo4jDb
from services.redis_checker import RedisChecker
from utils.lemmatizer import Lemmatizer
import time

class GraphDatabaseCreator:
    neo4j_mgr = None
    neo4j_new = None
    db_dest_uri = "bolt://neo_dest"
    db_src_uri = "bolt://neo_src"
    db_dest = "neo4j"
    db_src = "neo4j"
    max_depth = 0
    threshold_visits = 0
    restart_probability = 0.0
    lemmatizer=  None
    def __init__(self, depth, threshold_visits, restart_probability):
        self.neo4j_mgr = Neo4jDb(self.db_src_uri, self.db_src)
        self.neo4j_new = Neo4jDb(self.db_dest_uri, self.db_dest)
        self.max_depth = depth
        self.threshold_visits = threshold_visits
        self.restart_probability = restart_probability
        self.redis_checker = RedisChecker()
        self.lemmatizer = Lemmatizer()

    def create_graph(self, start, end):
        for node_index in range(start, end):
            (node_uri, node_properties) = self.neo4j_mgr.get_node_by_index(node_index);
            print("IN PROCESSING:" + node_uri)
            is_processed = self.redis_checker.get_processed_id(node_uri)

            if is_processed == "DONE":
                print("The node has already been processed. Carrying on...")
                continue

            init_graph = RandomWalk(node_uri, node_properties, self.max_depth, self.threshold_visits, self.restart_probability, self.neo4j_mgr, self.neo4j_new, self.lemmatizer)
            init_graph.random_walk_with_restart()
            self.redis_checker.insert_processed_id(node_uri)

            if node_index % 100 == 0:
                print("Created semsign for: " + str(node_index))
                if node_index % 2000 == 0:
                    del self.neo4j_mgr
                    del self.neo4j_new
                    del self.redis_checker
                    del self.lemmatizer
                    time.sleep(0.3)
                    self.neo4j_mgr = Neo4jDb(self.db_src_uri, self.db_src)
                    self.neo4j_new = Neo4jDb(self.db_dest_uri, self.db_dest)
                    self.redis_checker = RedisChecker()
                    self.lemmatizer = Lemmatizer()
            init_graph.insert_graph()
