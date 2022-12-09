# elabapi-python

Python library to interact with [eLabFTW](https://github.com/elabftw/elabftw) REST API v2.

## Installation

~~~bash
pip install --user elabapi-python
~~~

## Usage

See the [examples folder](./examples).

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
cd generated && python setup.py develop --user
~~~

## Publishing a new version

1. Bump version in config.json
2. Commit and push
3. Tag and push --tags
4. Create release on GitHub

# License

MIT, see [license file](./LICENSE).
