from neo4j import GraphDatabase
from utils.lemmatizer import Lemmatizer

class Neo4jLemmatizer:
    URI = 'neo4j://neo_dest:7687/'
    database_name = ''
    lemmatizer=  None
    session = None
    driver = None

    def __init__(self, uri, database_name):
        self.database_name = database_name
        self.URI = uri
        self.lemmatizer = Lemmatizer()
        self.driver = GraphDatabase.driver(self.URI)
        self.session = self.driver.session(database = self.database_name)

    def get_number_of_nodes(self):
        result = self.session.run('MATCH (n:Resource) RETURN COUNT(n) AS qty')
        return [record['qty'] for record in result][0]

    def lemmatize_node(self, ind):
        pass

    def __del__(self):
        self.session.close()
        self.driver.close()
