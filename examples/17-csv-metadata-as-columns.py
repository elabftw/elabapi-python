#!/usr/bin/env python
# This script takes an eLabFTW exported CSV file as input
# and processes the metadata into new columns
# it requires the "pandas" library
import pandas as pd
import json

def get_fields(metadata):
    """Extract the name and value of extra field"""
    try:
        metadata_dict = json.loads(metadata)
        return {name: field.get('value', None) for name, field in metadata_dict['extra_fields'].items()}
    except (json.JSONDecodeError, KeyError, TypeError):
        return {}

df = pd.read_csv('data/antibodies-export-from-elab.csv')

for index, row in df.iterrows():
    new_fields = get_fields(row['metadata'])
    for name, value in new_fields.items():
        df.at[index, name] = value

df.to_csv('output.csv', index=False)
