import threading

import config
import funcs_discord
import handler_SQLite
import handler_postgreSQL
import parser_master

# Start Thread for Discord-bot
threading.Thread(target=funcs_discord.bot.run(config.token_discord), 
        name='thrd-DiscordBot').start()

