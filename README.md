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

To route API traffic through a proxy, set the standard environment variables before running the script. These variables are used by both the Python HTTP stack and the eLabFTW client.

### Environment configuration

Set the following variables according to your proxy setup:

- `HTTP_PROXY` and `HTTPS_PROXY`: Define the proxy server address, including the protocol and port (for example, `http://127.0.0.1:8080`).
- `NO_PROXY`: Specify hostnames or IPs that should bypass the proxy (for example, localhost or internal domains).
- `REQUESTS_CA_BUNDLE`: Optional path to a custom CA certificate file, required if the proxy intercepts HTTPS traffic with a self-signed certificate.

Example:
~~~bash
export HTTP_PROXY="http://127.0.0.1:8080"
export HTTPS_PROXY="http://127.0.0.1:8080"
export NO_PROXY="localhost,127.0.0.1"
export REQUESTS_CA_BUNDLE="/path/to/proxy-ca.pem"
~~~

### Client configuration

The client automatically detects these environment variables. To set the proxy manually, use the configuration object:

~~~python
configuration.proxy = os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
configuration.ssl_ca_cert = os.getenv("CA_PATH") or os.getenv("REQUESTS_CA_BUNDLE")
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
