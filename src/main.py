import sys
from disambiguation.graph_database_creator import GraphDatabaseCreator
from interfaces.cli import initiate_cli
print("Application started")
if len(sys.argv) > 1 and sys.argv[1] == "init-graph":
    print("Start sem signatures creation")
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    gdc = GraphDatabaseCreator(150, 1, 0.05)
    gdc.create_graph(start, end)
else:
    initiate_cli(sys.argv)
