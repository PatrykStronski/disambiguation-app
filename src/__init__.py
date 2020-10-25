from disambiguation.graph_database_creator import GraphDatabaseCreator
print("Application started")
gdc = GraphDatabaseCreator(25, 2, 0.3)
gdc.create_graph()
