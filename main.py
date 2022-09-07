import threading

import config
import bot_discord
import parser_master

if config.use_postgreSQL: 
    import handler_postgreSQL as sql_handler
else: 
    import handler_SQLite as sql_handler

def refresh_db():
    "Refreshes DB with new parsed events."

    list_of_events = parser_master.parse_urls_from_config()
    sql_handler.put_list_of_events(list_of_events)


refresh_db()

# Start Thread for Discord-bot
threading.Thread(target=bot_discord.bot.run(config.token_discord), 
        name='thrd-DiscordBot').start()

# Refresh db every 12h
threading.Timer(43200, refresh_db)
