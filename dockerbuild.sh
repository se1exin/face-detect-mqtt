docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

# Create a new builder
docker buildx create --use --name multiarch-builder

# Make sure builder is running
docker buildx inspect --bootstrap

docker buildx build \
  --push \
  --platform linux/arm64/v8,linux/amd64 \
  --tag selexin/cvzone-mqtt-tracker:latest .

