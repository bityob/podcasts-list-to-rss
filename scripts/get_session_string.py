import os
import sys

from envparse import env

try:
    from telethon.sessions import StringSession
    from telethon.sync import TelegramClient
except Exception as err:
    print(err)
    print("\nFailed to import. Please install Telethon.\nRun\n\tpip install telethon")
    sys.exit()


env.read_envfile()


def get_value(of_what: str):
    val = os.getenv(of_what)
    if not val:
        val = input(f"Enter the value of {of_what}:\n>")
        if not val:
            print("Recieved no input. Quitting.")
            sys.exit()
        return val
    return val


print(
    "\nYou are now going to login, and the session string will be displayed on screen. \nYou need to copy that for"
    " future use."
)

input("\nPress [ENTER] to proceed \n?")

phone = input("Enter you phone number in international format: ")

if not phone:
    print("You did not enter your phone number. Quitting.")
    sys.exit()

with TelegramClient(StringSession(), get_value("API_ID"), get_value("API_HASH")).start(phone=phone) as client:
    print("\n\nBelow is your session string ⬇️\n\n")
    print(client.session.save())
    print("\nAbove is your session string ⬆️\n\n")

print(
    """

- Keep this string safe! Dont leak it.

- Anyone with this string can use it to login into your account and do anything they want to to do.

- For more information about Telethon Session Strings
\thttps://docs.telethon.dev/en/latest/concepts/sessions.html#string-sessions

- You can deactivate this session by going to your
\tTelegram App -> Settings -> Devices -> Active sessions

"""
)
