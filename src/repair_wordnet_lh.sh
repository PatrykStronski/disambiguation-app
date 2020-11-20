#!/bin/bash

pm2 start ./__init__.py --name "graph_creation1" --watch -f -- "init-graph" 29750 115333

pm2 start ./__init__.py --name "graph_creation2" --watch -f -- "init-graph" 159050 230666

pm2 start ./__init__.py --name "graph_creation3" --watch -f -- "init-graph" 283550 346000
