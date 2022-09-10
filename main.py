import threading
import time


from config import (discord_bot_channel_id, token_discord, refresh_time, 
        use_postgreSQL, use_SQLite)
import bot_discord
from parser_master import parse_urls_from_config
import db_handler 


def start_bots():
    db_handler.put_list_of_events(parse_urls_from_config()) # update db

    thread_discord = threading.Thread(target=bot_discord.bot.run(token_discord),
            name='thrd-DiscordBot', daemon=True).start()

    time.sleep(refresh_time)

    thread_discord.cancel()


while True:
    start_bots()


