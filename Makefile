build:
	DOCKER_BUILDKIT=1 DOCKER_SCAN_SUGGEST=false docker build . -t podcasts-list-to-rss --load

create-env-file:
	echo "TELEGRAM_APP_ID=${TELEGRAM_APP_ID}" > .env
	echo "TELEGRAM_APP_HASH=${TELEGRAM_APP_HASH}" >> .env
	echo "CHANNEL_NAME=${CHANNEL_NAME}" >> .env
	echo 'RSS_NAME="${RSS_NAME}"' >> .env
	echo 'RSS_DESCRIPTION="${RSS_DESCRIPTION}"' >> .env
	echo "RSS_WEBSITE=${RSS_WEBSITE}" >> .env
	echo "RSS_IMAGE_URL=${RSS_IMAGE_URL}" >> .env
	echo "RSS_FILE_NAME=${RSS_FILE_NAME}" >> .env
	echo "RSS_MAX_MESSAGES=${RSS_MAX_MESSAGES}" >> .env
	echo "DB_URL=${DB_URL}" >> .env

decrypt:
	# Decrypt the file
	# --batch to prevent interactive command
	# --yes to assume "yes" for questions
	gpg --quiet --batch --yes --decrypt --passphrase="$(SESSION_SECRET_PASSPHRASE)" --output ./src/user.session user.session.gpg

run:
	docker run podcasts-list-to-rss

run-with-mount:
	docker run -v $$(pwd)/assets:/opt/assets -v $$(pwd)/src:/opt/src podcasts-list-to-rss

bash:
	docker run -v $$(pwd)/assets:/opt/assets -v $$(pwd)/src:/opt/src -it podcasts-list-to-rss bash

bash-without-mount:
	docker run -it podcasts-list-to-rss bash

ipython:
	docker run -v $$(pwd)/assets:/opt/assets -v $$(pwd)/src:/opt/src -it podcasts-list-to-rss ipython

test:
	docker run -v $$(pwd)/assets:/opt/assets -v $$(pwd)/src:/opt/src -i$$([ -t 0 ] && echo t) podcasts-list-to-rss uv run pytest ./tests

gh-run-rss:
	gh workflow run main.yaml --ref $$(git rev-parse --abbrev-ref HEAD)

gh-watch-last-run:
	gh run watch $$(gh run list --workflow main.yaml -L 1 --json databaseId --jq ".[0].databaseId")
