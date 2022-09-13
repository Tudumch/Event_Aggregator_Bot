import threading
import time


from config import (token_discord, refresh_time)
import bot_discord
import parsers 
import db_handler 


def start_bots():
    KlinParkParser = parsers.KlinParkParser()

    db_handler.put_list_of_events(
            KlinParkParser.get_list_of_new_events()) # update DB

    thread_discord = threading.Thread(target=bot_discord.bot.run(token_discord),
            name='thrd-DiscordBot', daemon=True)
    thread_discord.start()

    time.sleep(refresh_time)

    thread_discord.cancel() # TODO: need to fix that


while True:
    start_bots()


