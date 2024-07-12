# elabapi-python

[![release](https://img.shields.io/pypi/v/elabapi-python.svg)](https://pypi.org/project/elabapi-python/)
[![wheel](https://img.shields.io/pypi/wheel/elabapi-python.svg)](https://pypi.org/project/elabapi-python/)

Python library for eLabFTW REST API.

# Description

This repository allows generating a python library to interact with [eLabFTW](https://github.com/elabftw/elabftw) REST API v2. It uses [Swagger Codegen](https://github.com/swagger-api/swagger-codegen/tree/3.0.0) to generate it based on the OpenApi specification of [eLabFTW REST API v2](https://doc.elabftw.net/api/v2/).

As such, it doesn't contain the generated code, but only instructions on how to generate it for local development.

Users should install the library with `pip`, as described below.

# Installation

~~~bash
# create a virtual environment
python -m venv elab
# activate it
source elab/bin/activate
# on Windows
# C:\> elab\Scripts\activate.bat
# install the library
pip install elabapi-python
~~~

# Usage

See the [examples folder](./examples).

# Unofficial documentation

From TU Graz, Shared RDM Project:

* https://github.com/sharedRDM/elabftw_api_support

# Dev

## Using the helper script

~~~bash
# generate the library
./helper.sh generate
# generate from local file: openapi.yaml must be in current dir
./helper.sh generate-from-local
# build packages
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
