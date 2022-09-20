import threading
import time


from config import token_discord, refresh_time
from log_handler import logger
import bot_discord
import parser_master 
import db_handler 


logger.debug("MAIN: run.")

def start_bots():
    """
    Infinetly restartable function for refreshing DB and bots. By restrting, 
    bots notify users about new evevnts.
    """

    logger.info("MAIN: starting DB refresh and bot-threads...")
    ParserMaster = parser_master.ParserMaster()
    db_handler.put_list_of_events(
            ParserMaster.parse_urls_from_config()) # update DB
    logger.info("MAIN: DB has been refreshed successfuly.")

    thread_discord = threading.Thread(target=bot_discord.bot.run(token_discord),
            name='thrd-DiscordBot', daemon=True)
    thread_discord.start()
    logger.info("MAIN: discord bot thread has been run.")

    time.sleep(refresh_time)
    logger.info("MAIN: refresh time is out - initiate restarting process...")

    logger.info("MAIN: closing bot-threads...")
    thread_discord.cancel() # TODO: need to fix that
    logger.info("MAIN: bot-threads closed successfuly.")


while True:
    start_bots()


