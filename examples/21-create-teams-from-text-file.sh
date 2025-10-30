#!/usr/bin/env bash
set -euo pipefail

# This simple text file has one team name per line
INPUT_FILE="teams-to-create.txt"

# Add your APIKEY here
apikey="12-abcdef123..."
# Add your hostname here
host="elab.example.com"

# Loop over each line and create the team
while IFS= read -r line || [[ -n "$line" ]]; do
    curl -vL -H "Authorization: $apikey" -H "Content-Type: application/json" -d "{\"name\":\"$line\"}" -X POST https://${host}/api/v2/teams
done < $INPUT_FILE
