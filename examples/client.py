# This file is there to avoid having to replicate the same code in all examples

# We will use the standard "os" module to read values from environment
import os
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

# PROXY CONFIG
# Typical usage:
#   export HTTP_PROXY="http://127.0.0.1:8080"
#   export HTTPS_PROXY="http://127.0.0.1:8080"
#   export NO_PROXY=localhost,127.0.0.1
#   export REQUESTS_CA_BUNDLE=/path/to/mitmproxy-ca.pem
# Many libraries (e.g. 'requests') read HTTP(S)_PROXY from the environment automatically.
# However the generated elabapi_python client uses a generated Configuration + urllib3
# which may not read those env vars. That is why we set the env vars along with 'configuration.proxy'
# and 'configuration.ssl_ca_cert' so the generated client itself uses the proxy and trust bundle.
proxy_url = os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
if proxy_url:
    configuration.proxy = proxy_url

# set CA for both requests and the elabapi-client
ca_path = os.getenv("CA_PATH") or os.getenv("REQUESTS_CA_BUNDLE")
if ca_path:
    configuration.ssl_ca_cert = ca_path
    if not os.getenv("REQUESTS_CA_BUNDLE"):
        os.environ["REQUESTS_CA_BUNDLE"] = ca_path

# Create an API client object with our configuration
api_client = elabapi_python.ApiClient(configuration)

# Set the Api Key in Authorization header
api_client.set_default_header(header_name='Authorization', header_value=API_KEY)
