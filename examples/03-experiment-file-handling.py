#!/usr/bin/env python

####################################################################################
#    In this example script, we will upload a file to an experiment and delete it. #
#        You can comment the 'delete' part to see results in your experiment.      #
####################################################################################

# Doc: https://doc.elabftw.net/api/v2/#/Uploads

# part 1 (upload_file_to_experiment) will upload a file to a target experiment.
# part 2 (download_matching_uploads_locally) will download locally a file from an eLabFTW experiment.
# part 3 (cleanup) will remove the files from both the experiment and locally.
import os
import elabapi_python
from client import api_client

# create an instance of Experiments and another for Uploads
experimentsApi = elabapi_python.ExperimentsApi(api_client)
uploadsApi = elabapi_python.UploadsApi(api_client)

# define the target experiment
EXPERIMENT_ID = 210
# prepare the file. We'll use the 'README.md' present in current folder
SOURCE_FILE = "README.md"
# local downloads for the script
DOWNLOADED_FILENAME = "README.downloaded_with_api.md"

exp = experimentsApi.get_experiment(EXPERIMENT_ID)

# --- part 1: Upload file to experiment ---
def upload_file_to_experiment():
    uploadsApi.post_upload('experiments', EXPERIMENT_ID, file=SOURCE_FILE, comment='Uploaded with APIv2')

# --- part 2: Download uploads locally ---
def download_matching_uploads_locally():
    # display id, name and comment of the uploaded files and download them locally
    for upload in uploadsApi.read_uploads('experiments', exp.id):
        print(upload.id, upload.real_name, upload.comment, upload.state)
        # get and save file
        with open(DOWNLOADED_FILENAME, 'wb') as file:
            # the _preload_content flag is necessary so the api_client doesn't try and deserialize the response
            file.write(uploadsApi.read_upload('experiments', EXPERIMENT_ID, upload.id, format='binary', _preload_content=False).data)

# --- part 3: delete the downloaded file ---
def cleanup():
    # delete all the files where the name is 'README.md'
    for upload in uploadsApi.read_uploads('experiments', exp.id):
        if upload.real_name == SOURCE_FILE:
            uploadsApi.delete_upload('experiments', EXPERIMENT_ID, upload.id)
    # cleanup: delete the downloaded file
    try:
        os.remove(DOWNLOADED_FILENAME)
    except FileNotFoundError:
        pass

upload_file_to_experiment()
download_matching_uploads_locally()
cleanup()
