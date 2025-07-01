#!/usr/bin/env bash
# This script will generate a python library from the openapi definition file.
# Note: if running into this error: library initialization failed - unable to allocate file descriptor table - out of memory
# Edit docker systemd service file and add "--default-ulimit nofile=65536:65536" on the ExecStart line
# then systemctl daemon-reload and systemctl restart docker

# default generator
generator_tool="${GENERATOR_TOOL:-swagger}"

# generator can be 'swagger' or 'openapi'
if [ "$generator_tool" = "swagger" ]; then
    docker_image="swaggerapi/swagger-codegen-cli-v3:3.0.68"
    generator_flag="-l"
else
    # releases: https://github.com/OpenAPITools/openapi-generator/releases
    generator_version="v7.13.0"
    docker_image="openapitools/openapi-generator-cli:$generator_version"
    generator_flag="-g"
fi

# the docker image used to generate the client code
# pinning version to avoid unexpected bugs
docker_image="openapitools/openapi-generator-cli:$generator_version"
# where to grab the definition file
openapi_yaml_url="https://raw.githubusercontent.com/elabftw/elabftw/master/apidoc/v2/openapi.yaml"
# folder with the generated python code
lib="generated"
html="html"

function cleanup {
    rm -rfv "$lib"
    rm -rfv "$html"
}

# generate the lib from remote spec
function generate {
    cleanup
    docker run --user "$(id -u)":"$(id -u)" --rm -v "${PWD}":/local "$docker_image" generate -i "$openapi_yaml_url" $generator_flag python -o /local/"$lib" -c /local/config.json --git-user-id elabftw --git-repo-id elabapi-python
}

function generate-html {
    cleanup
    docker run --user "$(id -u)":"$(id -u)" --rm -v "${PWD}":/local "$docker_image" generate -i "$openapi_yaml_url" $generator_flag html2 -o /local/"$html" -c /local/config.json --git-user-id elabftw --git-repo-id elabapi-python
}

# don't use user/group ids in GH actions
function generate-ci {
    docker run --rm -v "${PWD}":/local "$docker_image" generate -i "$openapi_yaml_url" $generator_flag python -o /local/"$lib" -c /local/config.json --git-user-id elabftw --git-repo-id elabapi-python
    # fix permissions
    sudo chown -R "$(id -u)":"$(id -gn)" "$lib"
}

# generate the lib from a local file in current directory
function generate-from-local {
    cleanup
    docker run --user "$(id -u)":"$(id -g)" --rm -v "${PWD}":/local "$docker_image" generate -i /local/openapi.yaml $generator_flag python -o /local/"$lib" -c /local/config.json --git-user-id elabftw --git-repo-id elabapi-python
}

function venv {
    rm -rf venv
    python -m venv venv
    source venv/bin/activate
}

function build {
    cd "$lib" || exit 1
    pip install uv
    uv build
}

function publish {
    generate
    build
    cd "$lib" || exit 1
    twine upload dist/*
}

function install-dev {
    venv
    pip install -e generated
}

function build-ci {
    generate-ci
    build
}

"$1"
