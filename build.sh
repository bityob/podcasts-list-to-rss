export DOCKER_SCAN_SUGGEST=false

docker build . -t podcasts-list-to-rss --build-arg TELEGRAM_APP_ID=${TELEGRAM_APP_ID} --build-arg TELEGRAM_APP_HASH=${TELEGRAM_APP_HASH} --build-arg TELEGRAM_PUBLIC_CHANNEL_NAME=${TELEGRAM_PUBLIC_CHANNEL_NAME} --build-arg TELEGRAM_PHONE=${TELEGRAM_PHONE} --build-arg TELEGRAM_PASSWORD=${TELEGRAM_PASSWORD}

docker run podcasts-list-to-rss