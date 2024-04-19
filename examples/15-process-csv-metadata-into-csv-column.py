#!/usr/bin/env python

# In this script, we use a CSV that has been created from eLabFTW
# Then loop over all the entries, extract the metadata, and create another CSV
# where each metadata extra field is a column
import json
import csv

# First we import a CSV file that has been created from eLabFTW export function
# Important: use encoding parameter to decode the CSV properly (https://stackoverflow.com/a/49150749)
with open('data/antibodies-export-from-elab.csv', encoding='utf-8-sig') as csvfile:
    # Use the DictReader function to get Dict objects back
    csvreader = csv.DictReader(csvfile)
    # We want all rows as a list of rows
    rows = []
    for row in csvreader:
        rows.append(row)

# This Set will be needed when exporting to csv
fieldnames = set()
for entry in rows:
    # Let's display for each row, the title and its corresponding metadata
    print(f"{entry.get('title')} => {entry.get('metadata')}")
    # Now let's process that metadata
    metadata = json.loads(entry.get('metadata'))
    # Extract fields from 'extra_fields' and add them to the item dictionary
    for key, value in metadata.get('extra_fields').items():
        entry[key] = value.get('value')
    # Remove the original JSON metadata
    del entry['metadata']
    fieldnames.update(entry.keys())

output = 'output.csv'
print(f"[INFO] Writing output to {output}")
with open(output, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
