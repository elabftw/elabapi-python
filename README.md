# elabapi-python

[![release](https://img.shields.io/pypi/v/elabapi-python.svg)](https://pypi.org/project/elabapi-python/)
[![wheel](https://img.shields.io/pypi/wheel/elabapi-python.svg)](https://pypi.org/project/elabapi-python/)

Python library for eLabFTW REST API.

# Description

This repository allows generating a python library to interact with [eLabFTW](https://github.com/elabftw/elabftw) REST API v2. It uses [Swagger Codegen](https://github.com/swagger-api/swagger-codegen/tree/3.0.0) to generate it based on the OpenApi specification of [eLabFTW REST API v2](https://doc.elabftw.net/api/v2/).

Alternatively, it supports using [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator) as an optional code generation tool.

As such, it doesn't contain the generated code, but only instructions on how to generate it for local development.

Users should install the library with `pip` or any other python dependency management tool, as described below.

# Installation

~~~bash
# create a virtual environment
python -m venv venv
# activate it
source venv/bin/activate
# on Windows
# C:\> venv\Scripts\activate.bat
# install the library
pip install elabapi-python
~~~

# Usage

## Getting started
The easiest way to get started is to look at an example script: [00-getting-started.py](./examples/00-getting-started.py).

Find more examples in the [examples folder](./examples).

## Basic concepts

~~~python
import elabapi_python
# Initialize a configuration object from the library
configuration = elabapi_python.Configuration()
# Set the host
configuration.host = "https://eln.example.org/api/v2"
# Create an API client object with our configuration
api_client = elabapi_python.ApiClient(configuration)
# Set the Api Key in Authorization header
api_client.set_default_header(header_name='Authorization', header_value=5-abc123...)

# Depending on your needs, instantiate the correct object with api_client as argument
info_client = elabapi_python.InfoApi(api_client)
exp_client = elabapi_python.ExperimentsApi(api_client)
items_client = elabapi_python.ItemsApi(api_client)
~~~

## Using a proxy

If you need to route your API traffic through a proxy (for example, to inspect requests with `mitmproxy` or to access eLabFTW behind a corporate network), you can configure it directly in the API client.

### Using environment variables

The simplest way is to define proxy settings via standard environment variables before running your script:
~~~bash
export HTTP_PROXY="http://127.0.0.1:8080"
export HTTPS_PROXY="http://127.0.0.1:8080"
export NO_PROXY=localhost,127.0.0.1
~~~

Open a new terminal and run a proxy (e.g., mitmproxy)

~~~bash
pip install mitmproxy
mitmdump --listen-host 0.0.0.0 --listen-port 8080 --ssl-insecure
~~~

Now run your script and confirm requests go through the proxy.

### Using the Configuration object

Alternatively, you can set the proxy directly in your code:

~~~python
import elabapi_python
# Initialize a configuration object from the library
configuration = elabapi_python.Configuration()
# Set the host
configuration.host = "https://eln.example.org/api/v2"
# Set a proxy URL (supports HTTP and HTTPS)
configuration.proxy = "http://127.0.0.1:8080"
# or using Docker, something like "http://host.docker.internal:8080"
# Optionally, specify a path to a custom CA certificate (e.g. mitmproxy)
configuration.ssl_ca_cert = "/path/to/mitmproxy-ca.pem"
# Create an API client object with the configuration
api_client = elabapi_python.ApiClient(configuration)
~~~

# Unofficial documentation

From TU Graz, Shared RDM Project:

* https://github.com/sharedRDM/elabftw_api_support

# Dev

## Using the helper script

### Generate the library using Code Generators

The primary tool for generating the library is swagger-codegen. However, you can also use OpenAPI Generator as an alternative, if it better suits your requirements or you encounter issues with the default.

~~~bash
# Option 1: Generate using Swagger Codegen
./helper.sh generate

# Option 2: Generate using OpenAPI Generator
GENERATOR_TOOL=openapi ./helper.sh generate
~~~

### Or Generate from a local OpenAPI Specification
Ensure the `openapi.yaml` file is located in the current working directory, then run:
~~~bash
./helper.sh generate-from-local
~~~

### Build packages
~~~bash
./helper.sh build
~~~

## Installing the library for dev

~~~bash
./helper.sh install-dev
~~~

## Publishing a new version

1. Bump version in config.json
2. Commit and push
3. Tag and push --tags
4. Create release on GitHub

# License

MIT, see [license file](./LICENSE).
