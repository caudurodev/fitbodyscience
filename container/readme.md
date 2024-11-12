# DEPLOY to NHOST

## login to nhost registry (login to nhost):

`$ nhost docker-credentials configure`

## Create a new builder and set it as the current builder

docker buildx create --use

## Inspect the builder and ensure it's ready

docker buildx inspect --bootstrap

## get registry address here

https://app.nhost.io/caudurodev/jobsniper/services

## Your build command (unchanged, but will now use the new builder)

docker buildx build \
 --push \
 --platform linux/amd64,linux/arm64 \
 -t registry.eu-central-1.nhost.run/b303e71b-16b5-4163-96ce-256a07a02267:[tag] \
 .

## Your build command (unchanged, but will now use the new builder)

docker buildx build \
 --push \
 --platform linux/amd64,linux/arm64 \
 -t registry.eu-central-1.nhost.run/b303e71b-16b5-4163-96ce-256a07a02267:78 \
 .
