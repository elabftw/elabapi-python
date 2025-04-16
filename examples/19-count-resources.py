"""
This script connects to an eLabFTW instance via the REST API to retrieve and list all available resource categories (also called item types).
For each category, it prints the category ID and title, followed by the number of entries (items) that belong to that category.

⚙️ Configuration required:
- API_HOST_URL: The URL of your eLabFTW instance.
- API_KEY: Your personal or application-specific API key to authenticate requests.

The script uses the official eLabFTW Python client and urllib3 to handle HTTPS connections.
"""

# Import the necessary library to access the eLabFTW API
import elabapi_python
import urllib3

API_HOST_URL = 'https://elab.local:3148/api/v2'  # <-- URL eLabFTW Goethe Uni or Replace with your instance URL 
API_KEY = 'apiKey4Test'  # <-- Replace with your API key

# Deactivate warnings for self-signed certificates (optional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure the API client
configuration = elabapi_python.Configuration()
configuration.api_key['api_key'] = API_KEY  
configuration.api_key_prefix['api_key'] = 'Authorization'  
configuration.host = API_HOST_URL  
configuration.debug = False  
configuration.verify_ssl = True  # Verify SSL certificate (important for secure communication)

# Create the API client with the above configuration
api_client = elabapi_python.ApiClient(configuration)
api_client.set_default_header(header_name='Authorization', header_value=API_KEY)  

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
