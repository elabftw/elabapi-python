#!/usr/bin/env python

######################################################################################
# In this example script, we add tags from a list: a text file with one tag per line #
######################################################################################

import elabapi_python
import sys

# use the locally defined client.py module to get the api_client object, fully configured and ready to be used to instantiate api objects
from client import api_client

team_tags_api = elabapi_python.TeamTagsApi(api_client)

# REPLACE with your team ID (see /api/v2/teams/current/)
team_id = 2

# REPLACE this too
FILE_PATH = 'data/tags.txt'

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        tag = line.strip()

        if not tag:
            continue

        try:
            team_tags_api.post_team_tag(team_id, body={'tag': tag})
            print(f'Created tag: {tag}')
        except Exception as exc:
            print(
                f'Failed to post tag on line {line_number}: {tag} ({exc})',
                file=sys.stderr,
            )
