import sys
from disambiguation.graph_database_creator import GraphDatabaseCreator
from router.index import create_app
print("Application started")
if len(sys.argv) > 1 and sys.argv[1] == "init-graph":
    print("Start sem signatures creation")
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    gdc = GraphDatabaseCreator(25, 2, 0.2)
    gdc.create_graph(start, end)
else:
    print("Start Flask server")
    create_app()
