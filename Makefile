build:
	DOCKER_SCAN_SUGGEST=false docker build . -t podcasts-list-to-rss

decrypt:
	# Decrypt the file
	# --batch to prevent interactive command
	# --yes to assume "yes" for questions
	gpg --quiet --batch --yes --decrypt --passphrase="$(SESSION_SECRET_PASSPHRASE)"
	--output user.session user.session.gpg

run:
	docker run podcasts-list-to-rss
	#docker run -v $$(pwd)/assets:/app/assets -v $$(pwd)/src:/opt/src podcasts-list-to-rss

run-with-mount:
	docker run -v $$(pwd)/assets:/app/assets -v $$(pwd)/src:/opt/src podcasts-list-to-rss
