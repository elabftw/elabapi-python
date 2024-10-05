#!/usr/bin/env python

###############
# DESCRIPTION #
##############
#
# This script will read a csv file that contains a list of emails to update,
# with a column "old_email" that exist in the database, and a column
# "new_email" with the value that we want to push to the database.
# It will then generate a .sql file to update these values directly in the database.

# we will use the generic csv module
import csv

CSV_PATH = './data/users-emails.csv'
OUTPUT_PATH = './update-emails.sql'
OLD_EMAIL_COLUMN = 'old_email'
NEW_EMAIL_COLUMN = 'new_email'

with open(OUTPUT_PATH, 'w') as outfile:
    pass  # This just to clear any previous content

# Note: use encoding='utf-8-sig' in the open() call if your file has BOM (Byte Order Mark)
# Also make sure that the CSV file was saved as UTF-8 to avoid issues with special characters
with open(CSV_PATH, newline='') as csvfile:
    # let's read the CSV using the standard "csv" library from python. No need for anything fancier.
    csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    with open(OUTPUT_PATH, 'a') as outfile:
    # now we loop over each row in our CSV
        for row in csvreader:
            line = f"UPDATE users SET email = '{row[NEW_EMAIL_COLUMN]}' WHERE email = '{row[OLD_EMAIL_COLUMN]}';\n"
            outfile.write(line)

print(f'SQL file written to {OUTPUT_PATH}')
