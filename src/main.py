import sys
from disambiguation.graph_database_creator import GraphDatabaseCreator
from router.index import create_app
from router.cli import initiate_cli
print("Application started")
if len(sys.argv) > 1 and sys.argv[1] == "init-graph":
    print("Start sem signatures creation")
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    gdc = GraphDatabaseCreator(70, 1, 0.15)
    gdc.create_graph(start, end)
elif len(sys.argv) > 1 and sys.argv[1] == "init-server":
    print("Start Flask server")
    create_app()
else:
    initiate_cli()
