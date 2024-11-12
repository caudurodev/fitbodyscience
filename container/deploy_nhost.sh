#!/bin/sh
# SERVICE_ID="2503b290-249c-42f5-b89e-fd9a98980e22" ??
IMAGE="registry.eu-central-1.nhost.run/b303e71b-16b5-4163-96ce-256a07a02267"
PAT="64190396-99ef-4bb9-8db6-b1d0bd5b49ff"
VERSION="1.0.0"
CONFIGURATION_FILE="nhost-service.toml"

# this only needs to be done once in each environment
# but usually CIs start with a clean environment each time
#
# you can also login with your regular email/password
# credentials if you prefer
nhost login --pat $PAT

# this only needs to be done once in each environment
# but usually CIs start with a clean environment each time
nhost docker-credentials configure --no-interactive

docker buildx build \
    --push \
    --platform linux/amd64,linux/arm64 \
    -t $IMAGE:$VERSION \
    .

nhost run config-deploy \
    --config $CONFIGURATION_FILE \
    --service-id $SERVICE_ID
