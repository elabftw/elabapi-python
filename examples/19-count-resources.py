#!/usr/bin/env python
"""
This script connects to an eLabFTW instance via the REST API to retrieve and list all available resource categories (also called item types).
For each category, it prints the category ID and title, followed by the number of entries (items) that belong to that category.
"""

import elabapi_python
# use the locally defined client.py module to get the api_client object, fully configured and ready to be used to instantiate api objects
from client import api_client

# In this example, categories will be linked to the current team.
TEAM_ID = "current"

# Create API instances for fetching resources categories and items (Entries) for each category
resourcesCategoriesApi = elabapi_python.ResourcesCategoriesApi(api_client)
itemsApi = elabapi_python.ItemsApi(api_client)

try:
    # Fetch the resources categories from the API
    resources_categories = resourcesCategoriesApi.read_team_resources_categories(TEAM_ID)

    # Print the number of categories
    print(f"Number of categories: {len(resources_categories)}")

    # Iterate through each category and display the ID and Title
    for resource_category in resources_categories:
        print(f"ID: {resource_category.id}, Title: {resource_category.title}")

        # Fetch the items (entries) for each category by ID
        entries = itemsApi.read_items(cat=resource_category.id, limit=100)  # Get the items for the category
        entry_count = len(entries)  # Count the number of items

        # Display the number of items in the current category
        print(f"Number of entries in this category: {entry_count}\n")

# Error handling for API requests
except elabapi_python.rest.ApiException as e:
    print(f"Error fetching categories or entries: {e}")
