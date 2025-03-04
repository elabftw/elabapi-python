# Examples for using this library

Work in progress!

# [00-read-items.py](./00-read-items.py)

Read all items.

# [01-download-timestamp-archive.py](./01-download-timestamp-archive.py)

Download all the timestamp archive zip created in the past 7 days.

# [02-patch-metadata-per-category.py](./02-patch-metadata-per-category.py)

Look for all items of a particular category and patch the metadata if it is empty.

# [03-experiment-file-handling.py](./03-experiment-file-handling.py)

Upload, download and delete a file in an experiment.

# [04-create-teamgroup-add-user.py](./04-create-teamgroup-add-user.py)

Create a teamgroup and add a user in it.

# [05-create-modify-item.py](./05-create-modify-item.py)

Create an item in the database and modify it.

# [06-create-users.py](./06-create-users.py)

Create users in batch.

# [07-patch-sysadmin-settings.py](./07-patch-sysadmin-settings.py)

Patch instance config: modify the settings of the Sysadmin Panel.

# [08-create-items-add-metadata.py](./08-create-items-add-metadata.py)

Read a CSV file for samples, create them in the database with metadata, tags and links.

# [09-import-csv.py](./09-import-csv.py)

Read a CSV file containing a list of antibodies and import them in the resource database using the metadata/extra fields.

# [10-date-time-conversions.py](./10-date-time-conversions.py)

Work with date-time data formats with a demonstration of doing statistics with experiments data.

# [11-resources-categories.py](./11-resources-categories.py)

Create and edit a Resources Category (Items types).

# [12-experiments-export-pdf.py](./12-experiments-export-pdf.py)

Look for all timestamped experiments last week for a particular user and save a pdf locally.

# [13-events.py](./13-events.py)

Get a list of events (booked slots) for the current team.

# [14-fix-user-exp-permissions.py](./14-fix-user-exp-permissions.py)

Look for all experiments of a given user and adjust permissions of their experiments.

# [15-process-csv-metadata-into-csv-column.py](./15-process-csv-metadata-into-csv-column.py)

Take a CSV file created from eLabFTW export function, and for each row, grab the metadata, and create a new CSV where each Extra Field in the metadata is now a column.

# [16-update-users-emails.py](./16-update-users-emails.py)

Take a CSV file that contains a list of old emails to update and their new value, and generate a .sql file that will update theses values in the database.

# [17-csv-metadata-as-columns.py](./17-csv-metadata-as-columns.py)

Take a CSV file created from eLabFTW export function, and creates a new CSV where it extracts the metadata Extra Fields into a new column.

# [18-archive-users.py](./18-archive-users.py)

Archive users that have been inactive for at least 8 months.
