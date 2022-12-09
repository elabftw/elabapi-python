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
# publish new version (after editing config.json, with twine installed, use __token__ as username)
./helper.sh publish
~~~

## Installing the library for dev

~~~bash
cd generated && python setup.py develop --user
~~~

# License

MIT, see [license file](./LICENSE).
