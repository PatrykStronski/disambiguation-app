#!/bin/bash

pm2 start ./__init__.py --name "graph_creation4" --watch -f -- "init-graph" 346000 350000

pm2 start ./__init__.py --name "graph_creation5" --watch -f -- "init-graph" 350000 364000

pm2 start ./__init__.py --name "graph_creation6" --watch -f -- "init-graph" 364000 368000
