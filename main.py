import threading
import time


from config import (token_discord, refresh_time)
import bot_discord


def start_bots():
    thread_discord = threading.Thread(target=bot_discord.bot.run(token_discord),
            name='thrd-DiscordBot', daemon=True)
    thread_discord.start()

    time.sleep(refresh_time)

    thread_discord.cancel() # TODO: need to fix that


while True:
    start_bots()


