build:
	bash ./build.sh

decrypt:
	bash ./decrypt_session.sh

run:
	docker run podcasts-list-to-rss
	#docker run -v $$(pwd)/assets:/app/assets -v $$(pwd)/src:/opt/src podcasts-list-to-rss
