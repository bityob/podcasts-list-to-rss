from telegram import TelegramReader

if __name__ == '__main__':
    reader = TelegramReader()

    for message in reader:
        print(message)