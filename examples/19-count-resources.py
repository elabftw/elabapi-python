"""
This script connects to an eLabFTW instance via the REST API to retrieve and list all available resource categories (also called item types).
For each category, it prints the category ID and title, followed by the number of entries (items) that belong to that category.
"""

import elabapi_python
# use the locally defined client.py module to get the api_client object, fully configured and ready to be used to instantiate api objects
from client import api_client

# Create API instances for fetching categories (ItemsTypes) and items (Entries) for each category
items_api = elabapi_python.ItemsTypesApi(api_client)
items_api2 = elabapi_python.ItemsApi(api_client)

try:
    # Fetch the categories (ItemsTypes) from the API
    item_types = items_api.read_items_types()  # Fetch all categories

    # Print the number of categories
    print(f"Number of categories: {len(item_types)}")

    # Iterate through each category and display the ID and Title
    for item_type in item_types:
        print(f"ID: {item_type.id}, Title: {item_type.title}")

        # Fetch the items (entries) for each category by ID
        entries = items_api2.read_items(cat=item_type.id, limit=100)  # Get the items for the category
        entry_count = len(entries)  # Count the number of items

        # Display the number of items in the current category
        print(f"Number of entries in this category: {entry_count}\n")

# Error handling for API requests
except elabapi_python.rest.ApiException as e:
    print(f"Error fetching categories or entries: {e}")
