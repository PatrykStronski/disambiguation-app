#!/bin/bash

pm2 start ./create_graph.sh --name "graph_creation1" -f -- "29750" "72750"
pm2 start ./create_graph.sh --name "graph_creation2" -f -- "72750" "115333"

pm2 start ./create_graph.sh --name "graph_creation3" -f -- "159050" "202000"
pm2 start ./create_graph.sh --name "graph_creation4" -f -- "202000" "230666"

pm2 start ./create_graph.sh --name "graph_creation5" -f -- "283550" "326500"
pm2 start ./create_graph.sh --name "graph_creation6" -f -- "326500" "346000"
