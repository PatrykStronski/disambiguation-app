# src/disambiguation/graph_database_creator.py
from disambiguation.graph_database_creator import GraphDatabaseCreator
print("Application started")
gdc = GraphDatabaseCreator(50, 2, 0.6)
gdc.create_graph()
