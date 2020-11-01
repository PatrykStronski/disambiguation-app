import sys
from disambiguation.graph_database_creator import GraphDatabaseCreator
from router.index import create_app
print("Application started")
if len(sys.argv) > 1 and sys.argv[1] == "init-graph":
    print("Start sem signatures creation")
    gdc = GraphDatabaseCreator(50, 2, 0.3)
    gdc.create_graph()
else:
    print("Start Flask server")
    create_app()
