# This file is there to avoid having to replicate the same code in all examples

# We will use the standard "os" module to read values from environment
import os

# You must have elabapi-python installed so it can be imported
# This line will make the library available in our script
# Install it with: 'pip install elabapi-python' or 'uv add elabapi-python'
import elabapi_python

# START CONFIG
# Basic configuration: Api Key and Host URL
# Get the Api Key from the environment or use the default development value
API_KEY = os.getenv('API_KEY') or 'apiKey4Test'
# Get the server address from the environment or use the default development value
API_HOST = os.getenv('API_HOST') or 'https://elab.local:3148/api/v2'

# Initialize a configuration object from the library
configuration = elabapi_python.Configuration()

# Set the host
configuration.host = API_HOST
# Verify the TLS certificate validity: should be set to True in production
configuration.verify_ssl = False
# For convenience, mask the warnings about skipping TLS verification
if not configuration.verify_ssl:
    import urllib3
    urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

# Set this flag to True to get more verbose output
configuration.debug = False

# Create an API client object with our configuration
api_client = elabapi_python.ApiClient(configuration)

# Set the Api Key in Authorization header
api_client.set_default_header(header_name='Authorization', header_value=API_KEY)

# END CONFIG
