import time
import multiprocessing

from config import refresh_time
from log_handler import logger
import bot_discord
import bot_telegram


def start_bots():
    """
    Infinetly restartable function for refreshing DB and bots. By restrting, 
    bots notify users about new events.
    """

    logger.info("Starting bot-threads...")
    discord_process = multiprocessing.Process(target=bot_discord.main)
    discord_process.start()
    logger.info("Discord bot thread has been run.")
    telegram_process = multiprocessing.Process(target=bot_telegram.main)
    telegram_process.start()
    logger.info("Telegram bot thread has been run.")
    time.sleep(refresh_time)
    logger.info("Refresh time is out - initiating restart process...")
    logger.info("Closing bot-threads...")
    discord_process.terminate()
    telegram_process.terminate()
    logger.info("All bot-threads have been closed successfuly.")

while True:
    start_bots()
    time.sleep(5) # timeout for sure that all client-bots are closed

