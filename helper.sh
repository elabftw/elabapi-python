#!/usr/bin/env bash
# This script will generate a python library from the openapi definition file.
# Note: if running into this error: library initialization failed - unable to allocate file descriptor table - out of memory
# Edit docker systemd service file and add "--default-ulimit nofile=65536:65536" on the ExecStart line
# then systemctl daemon-reload and systemctl restart docker


# the docker image used to generate the client code
# pinning version to avoid unexpected bugs
# see https://github.com/swagger-api/swagger-codegen/releases for updating version below
docker_image="swaggerapi/swagger-codegen-cli-v3:3.0.54"
# where to grab the definition file
openapi_yaml_url="https://raw.githubusercontent.com/elabftw/elabftw/hypernext/apidoc/v2/openapi.yaml"
# folder with the generated python code
lib="generated"
html="html"

function cleanup {
    rm -rfv "$lib"
    rm -rfv "$html"
}

# generate the lib from remote hypernext spec
function generate {
    cleanup
    docker run --user "$(id -u)":"$(id -u)" --rm -v "${PWD}":/local "$docker_image" generate -i "$openapi_yaml_url" -l python -o /local/"$lib" -c /local/config.json --git-user-id elabftw --git-repo-id elabapi-python
}

function generate-html {
    cleanup
    docker run --user "$(id -u)":"$(id -u)" --rm -v "${PWD}":/local "$docker_image" generate -i "$openapi_yaml_url" -l html2 -o /local/"$html" -c /local/config.json --git-user-id elabftw --git-repo-id elabapi-python
}

# don't use user/group ids in GH actions
function generate-ci {
    docker run --rm -v "${PWD}":/local "$docker_image" generate -i "$openapi_yaml_url" -l python -o /local/"$lib" -c /local/config.json --git-user-id elabftw --git-repo-id elabapi-python
    # fix permissions
    sudo chown -R "$(id -u)":"$(id -gn)" "$lib"
}

# generate the lib from a local file in current directory
function generate-from-local {
    cleanup
    docker run --user "$(id -u)":"$(id -g)" --rm -v "${PWD}":/local "$docker_image" generate -i /local/openapi.yaml -l python -o /local/"$lib" -c /local/config.json --git-user-id elabftw --git-repo-id elabapi-python
}

function build {
    cd "$lib" || exit 1
    python setup.py sdist bdist_egg bdist_wheel
    cd ..
}

function publish {
    generate
    build
    cd "$lib" || exit 1
    twine upload dist/*
    cd ..
}

function install-dev {
    cd "$lib" || exit 1
    python setup.py develop --user
    cd ..
}


function build-ci {
    generate-ci
    cd "$lib" || exit 1
    python -m build --sdist --wheel --outdir ../dist
}

"$1"
