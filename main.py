import threading
import time


from config import token_discord, refresh_time
from log_handler import logger
import bot_discord


logger.debug("MAIN: run.")

def start_bots():
    """
    Infinetly restartable function for refreshing DB and bots. By restrting, 
    bots notify users about new evevnts.
    """

    logger.info("MAIN: starting bot-threads...")
    thread_discord = threading.Thread(target=bot_discord.bot.run(token_discord),
            name='thrd-DiscordBot', daemon=True)
    thread_discord.start()
    logger.info("MAIN: discord bot thread has been run.")

    time.sleep(refresh_time)
    logger.info("MAIN: refresh time is out - initiating restarting process...")

    logger.info("MAIN: closing bot-threads...")
    thread_discord.cancel() # TODO: need to fix that
    logger.info("MAIN: bot-threads closed successfuly.")


while True:
    start_bots()


