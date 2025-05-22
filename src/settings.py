from envparse import env

env.read_envfile()

TELEGRAM_APP_ID = env("TELEGRAM_APP_ID", cast=str)
TELEGRAM_APP_HASH = env("TELEGRAM_APP_HASH", cast=str)

CHANNEL_NAME = env("CHANNEL_NAME")
PUBLIC_DOWNLOAD_URL_BOT = env("PUBLIC_DOWNLOAD_URL_BOT", default="DirectLinkGenerator_Bot")

RSS_NAME = env("RSS_NAME")
RSS_DESCRIPTION = env("RSS_DESCRIPTION", default="")
RSS_WEBSITE = env("RSS_WEBSITE", default="")
RSS_IMAGE_URL = env("RSS_IMAGE_URL")
RSS_FILE_NAME = env("RSS_FILE_NAME")
RSS_MAX_MESSAGES = env("RSS_MAX_MESSAGES", cast=int, default=50)

DB_URL = env("DB_URL", default="::memory:")
