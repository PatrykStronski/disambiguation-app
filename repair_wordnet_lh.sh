#!/bin/bash

pm2 start ./create_graph.sh --name "graph_creation1" --watch -f -- 29750 115333

pm2 start ./create_graph.sh --name "graph_creation2" --watch -f -- 159050 230666

pm2 start ./create_graph.sh --name "graph_creation3" --watch -f -- 283550 346000
