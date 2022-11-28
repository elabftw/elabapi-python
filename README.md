# elabapi-python

Python library to interact with [eLabFTW](https://github.com/elabftw/elabftw) REST API v2.

## Generate
docker run --rm -v /home/ktr/.dev/elabapi-python:/local swaggerapi/swagger-codegen-cli-v3 generate -i https://raw.githubusercontent.com/elabftw/elabftw/hypernext/apidoc/v2/openapi.yaml -l python -o /local/generated
