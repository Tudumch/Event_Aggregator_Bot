import threading
import time


from config import (token_discord, refresh_time)
import bot_discord
import parser_master 
import db_handler 


def start_bots():
    ParserMaster = parser_master.ParserMaster()

    db_handler.put_list_of_events(
            ParserMaster.parse_urls_from_config()) # update DB

    thread_discord = threading.Thread(target=bot_discord.bot.run(token_discord),
            name='thrd-DiscordBot', daemon=True)
    thread_discord.start()

    time.sleep(refresh_time)

    thread_discord.cancel() # TODO: need to fix that


while True:
    start_bots()


