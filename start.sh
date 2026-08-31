#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Kill existing screens if running
screen -S db_api -X quit 2>/dev/null
screen -S node_server -X quit 2>/dev/null

# Start Python Oracle API
screen -dmS db_api bash -c "cd $PROJECT_DIR && set -a && source .env && set +a && ~/venv/wilsonenv/bin/python db_api.py; echo '--- PROCESS EXITED ---'; read"
echo "db_api started in screen 'db_api'"

# Start Node.js server
screen -dmS node_server bash -c "cd $PROJECT_DIR && /home/wilson/.nvm/versions/node/v16.20.2/bin/node server.js; echo '--- PROCESS EXITED ---'; read"
echo "node_server started in screen 'node_server'"

echo ""
echo "To attach to a screen:"
echo "  screen -r db_api"
echo "  screen -r node_server"
echo ""
echo "To detach from a screen: Ctrl+A then D"
echo "To list screens: screen -ls"
