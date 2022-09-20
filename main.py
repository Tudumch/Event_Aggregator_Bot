import threading
import time


from config import token_discord, refresh_time
from log_handler import logger
import bot_discord


def start_bots():
    """
    Infinetly restartable function for refreshing DB and bots. By restrting, 
    bots notify users about new events.
    """

    logger.info("Starting bot-threads...")
    thread_discord = threading.Thread(target=bot_discord.bot.run(token_discord),
            name='thrd-DiscordBot', daemon=True)
    thread_discord.start()
    logger.info("Discord bot thread has been run.")

    time.sleep(refresh_time)
    logger.info("Refresh time is out - initiating restarting process...")

    logger.info("Closing bot-threads...")
    thread_discord.cancel() # TODO: need to fix that
    logger.info("Bot-threads closed successfuly.")


while True:
    start_bots()


