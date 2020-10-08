import sys
sys.path.append('./disambiguation/')
from GraphDatabaseCreatorClass import GraphDatabaseCreator

gdc = GraphDatabaseCreator(50, 2, 0.3)
gdc.create_graph()
