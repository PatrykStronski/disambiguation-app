from neo4j import GraphDatabase
from config import DIRECTED_RELATIONS

class Neo4jDb:
    URI = 'neo4j://neo_dest:7687/'
    database_name = ''
    session = None
    driver = None

    def __init__(self, uri, database_name):
        self.database_name = database_name
        self.URI = uri
        self.driver = GraphDatabase.driver(self.URI)
        self.session = self.driver.session(database = self.database_name)

    def get_related_nodes_weighted(self, node, princeton, initial_uri):
        query = 'MATCH (n:Resource {uri: "' + node + '"}) -[r]-> (b:Resource) WHERE b.uri <> "' + initial_uri + '" \
            OPTIONAL MATCH (b) --> (c: Resource), \
            (c) -[r_triangle]-> (n) \
            RETURN b.uri AS node2, COUNT(r_triangle) AS weight'
        if princeton != "ALL":
            if DIRECTED_RELATIONS:
                query = 'MATCH (n:Resource {uri: "' + node + '"}) -[r]-> (b:Resource) WHERE b.princeton = '+ princeton +' AND b.uri <> "' + initial_uri + '"  \
                    OPTIONAL MATCH (b) --> (c: Resource), \
                    (c) -[r_triangle]-> (n) WHERE c.princeton = '+ princeton +'\
                    RETURN b.uri AS node2, COUNT(r_triangle) AS weight'
            else:
                query = 'MATCH (n:Resource {uri: "' + node + '"}) -[r]- (b:Resource) WHERE b.princeton = '+ princeton +' AND b.uri <> "' + initial_uri + '"  \
                    OPTIONAL MATCH (b) -- (c: Resource), \
                    (c) -[r_triangle]- (n) WHERE c.princeton = '+ princeton +' \
                    WHERE c.uri <> b.uri AND c.uri <> n.uri \
                    RETURN b.uri AS node2, COUNT(r_triangle) AS weight'
        result = self.session.run(query)
        return [{'node2': record['node2'], 'weight': record['weight'] + 1} for record in result]

    def get_number_of_nodes(self):
        result = self.session.run('MATCH (n:Resource) RETURN COUNT(n) AS qty')
        return [record['qty'] for record in result][0]

    def get_node_by_index(self, ind):
        result = self.session.run('MATCH (n:Resource) WHERE NOT n:skos__Concept RETURN n.uri AS resource, properties(n) AS properties SKIP ' + str(ind) + ' LIMIT 1')
        return [(record['resource'], record['properties'] ) for record in result][0]

    def compose_props(self, properties):
        props = []
        for prop in properties.keys():
            if type(properties[prop]) == str:
                props.append('n.'+prop + '= "' + str(properties[prop]) + '"')
            else:
                props.append('n.'+prop + '= ' + str(properties[prop]).replace('\\x', '?'))
        separator = ', '
        return separator.join(props)

    def create_node(self, properties):
        props_string = self.compose_props(properties)
        self.session.run('MERGE (n:Resource {uri: "' + properties['uri'] + '"}) SET ' + props_string)

    def create_relation(self, node1_uri, node2_list):
        if len(node2_list) == 0:
            print('No semsigns in ' + node1_uri);
            return
        for node2 in node2_list:
            query = 'MATCH (start: Resource {uri: "' + node1_uri + '"}) MERGE (end: Resource {uri: "'+ node2 +'"}) MERGE (start) -[:relatesTo]->(end)'
            self.session.run(query)

    def __del__(self):
        self.session.close()
        self.driver.close()
