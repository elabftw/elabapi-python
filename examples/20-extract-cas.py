#!/usr/bin/env python

###############################################################################################################
# In this example script, we want to extract the extra field "CAS" from the resources "Chemical Compounds"    #
# This can then be used to re-import the compounds in the compounds table and complete them with pubchem data #
# The first step is to export all entries from the Admin panel, as CSV. This is what we will process.         #
###############################################################################################################

import elabapi_python
import argparse
import csv
import json
import sys

# use the locally defined client.py module to get the api_client object, fully configured and ready to be used to instantiate api objects
from client import api_client


items_client = elabapi_python.ItemsApi(api_client)

parser = argparse.ArgumentParser(
       description="This script extracts the CAS extra field from an eLabFTW CSV export of a resources category and saves it into a new csv file."
   )
parser.add_argument(
   "csv_path",
   type=str,
   help="Path to the input CSV file"
)
args = parser.parse_args()
cas_list = []
try:
    with open(args.csv_path, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        if "metadata" not in reader.fieldnames:
            print("Error: 'metadata' column not found in CSV.", file=sys.stderr)
            sys.exit(1)

        for i, row in enumerate(reader, start=1):
            raw = row["metadata"]
            try:
                metadata = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"Row {i}: could not parse JSON: {e}", file=sys.stderr)
                continue

            print(f"Row {i} metadata:", metadata)
            extra = metadata.get("extra_fields", {})
            cas_entry = extra.get("CAS")
            if cas_entry and "value" in cas_entry:
                cas_value = cas_entry["value"]
                print(f"Row {i} CAS value: {cas_value}")
                cas_list.append(cas_value)
            else:
                print(f"Row {i}: no CAS field found", file=sys.stderr)

except FileNotFoundError:
    print(f"Error: file '{args.file_path}' does not exist.", file=sys.stderr)
    sys.exit(1)

# Write the collected CAS values to the output CSV
try:
    out_path = args.csv_path + "-cas.csv"
    with open(out_path, mode="w", newline="", encoding="utf-8") as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["cas"])
        for cas in cas_list:
            writer.writerow([cas])
    print(f"Wrote {len(cas_list)} CAS values to {out_path}")
except IOError as e:
    print(f"Error writing to '{out_path}': {e}", file=sys.stderr)
    sys.exit(1)
