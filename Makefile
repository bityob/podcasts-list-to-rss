build:
	DOCKER_SCAN_SUGGEST=false docker build . -t podcasts-list-to-rss

create-env-file:
	echo "TELEGRAM_APP_ID=${TELEGRAM_APP_ID}" > .env
	echo "TELEGRAM_APP_HASH=${TELEGRAM_APP_HASH}" >> .env
	echo "CHANNEL_NAME=${CHANNEL_NAME}" >> .env
	echo "RSS_NAME=${RSS_NAME}" >> .env
	echo "RSS_DESCRIPTION=${RSS_DESCRIPTION}" >> .env
	echo "RSS_WEBSITE=${RSS_WEBSITE}" >> .env
	echo "RSS_IMAGE_URL=${RSS_IMAGE_URL}" >> .env
	echo "RSS_FILE_NAME=${RSS_FILE_NAME}" >> .env
	echo "RSS_MAX_MESSAGES=${RSS_MAX_MESSAGES}" >> .env

decrypt:
	# Decrypt the file
	# --batch to prevent interactive command
	# --yes to assume "yes" for questions
	gpg --quiet --batch --yes --decrypt --passphrase="$(SESSION_SECRET_PASSPHRASE)" --output ./src/user.session user.session.gpg

run:
	docker run podcasts-list-to-rss

run-with-mount:
	docker run -v $$(pwd)/assets:/opt/assets -v $$(pwd)/src:/opt/src podcasts-list-to-rss

ipython:
	docker run -it podcasts-list-to-rss bash
