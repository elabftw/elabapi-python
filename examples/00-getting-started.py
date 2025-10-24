#!/usr/bin/env python

##############################################################################################
# Welcome to the first example of using elabapi_python in a script                           #
# This file is heavily commented and will show you various examples of using the API library #
##############################################################################################

import elabapi_python

# first, use the locally defined client.py module to get the api_client object. (see /examples/client.py)
# it is fully configured and ready to be used to instantiate api objects
from client import api_client

# add pprint to pretty print python objects
from pprint import pprint

# Note:
# In order to make it easier to run only specific parts, the parts are grouped in functions that are called at the end of the script

def part1():
    ##############################
    # Part 1: the /info endpoint #
    ##############################
    # Doc: https://doc.elabftw.net/api/v2/#/Info/get-info
    # Let's start with a very simple endpoint: /info. It only has a GET method and replies with information about the instance.
    # It's an easy way to validate if all is working as expected.
    # Everytime we want to use an endpoint, we need to create the corresponding object and give it the api_client (which itself holds the configuration)
    info_client = elabapi_python.InfoApi(api_client)
    api_response = info_client.get_info()
    # Print the full response
    print("\n------------------------ START PART 1 ------------------------\n")
    print("[request] GET /info")
    pprint(api_response)
    print("")
    # Example usage
    print(f"[*] The instance at {api_client.configuration.host} has {api_response.teams_count} teams and {api_response.all_users_count} users.")
    print(f"[*] Total size of uploaded files: {api_response.uploads_filesize_sum_formatted}")
    print("\n------------------------ END PART 1 ------------------------\n")

def part2():
    ####################################
    # Part 2: manipulating experiments #
    ####################################
    # For this we need an "experiments" endpoint client object
    exp_client = elabapi_python.ExperimentsApi(api_client)

    print("\n------------------------ START PART 2 ------------------------\n")
    print("[request] POST /experiments")
    # Let's create our first experiment through the API
    # Doc: https://doc.elabftw.net/api/v2/#/Experiments/post-experiment
    # We will use the post_experiment_with_http_info() method so we can have something in the response
    # If you use post_experiment(), it works but doesn't send back the response headers (which contain the ID of the newly created entry)
    # This method returns a tuple with 3 components, so we assign them to 3 variables
    response_data, status_code, headers = exp_client.post_experiment_with_http_info()
    # the Location response header will point to the newly created entry
    location = headers.get('Location')
    # extract the ID as an integer from the Location string: it is simply the last part of the URL
    exp_id = int(location.split('/').pop())
    # A status code of 201 means the entry was created
    if status_code == 201:
        print(f"[*] We created an experiment. The status code is {status_code} and the experiment is at: {location}")

    # Let's try and delete it now!
    print(f"[request] DELETE /experiments/{exp_id}")
    response_data, status_code, headers = exp_client.delete_experiment_with_http_info(exp_id)
    if status_code == 204:
        print(f"[*] We deleted the experiment with id: {exp_id}")

    # Ok, now we will create another experiment but this time we will provide some information during creation
    # This dictionary will hold the values that we send during creation
    exp_data = {
        "title": "This experiment was created from the API with Python!",
        "body": "<h1>Some title</h1><p>Some content.<p>",
        "tags": ["created from api", "pythonftw", "tests"],
    }
    # Now we send the request with the "body" keyword parameter set to exp_data
    print("[request] POST /experiments")
    response_data, status_code, headers = exp_client.post_experiment_with_http_info(body=exp_data)
    exp_id = int(headers.get('Location').split('/').pop())
    if status_code == 201:
        print(f"[*] We created another experiment with ID: {exp_id}")

    # Let's verify that the title is correct. For that, we will GET the experiment to read it
    # Note that this time we do not use the _with_http_info function, but simply get_experiment()
    # It returns a pre-processed Entity object
    print(f"[request] GET /experiments/{exp_id}")
    experiment = exp_client.get_experiment(exp_id)
    print(f"[*] Our experiment has this title: {experiment.title}")

    # Ok let's change that title now, with a PATCH request
    print(f"[request] PATCH /experiments/{exp_id}")
    experiment = exp_client.patch_experiment(exp_id, body={"title": "Now the title was changed from the API!"})
    print(f"[*] Our experiment now has this title: {experiment.title}")
    print(f"[*] Check it out on the web interface: {experiment.sharelink}")

    print("\n------------------------ END PART 2 ------------------------\n")


# This is where the script really starts: we simply call the different functions representing parts of this tutorial one after the other
part1()
part2()
