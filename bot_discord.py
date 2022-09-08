import discord

import bot_master
import config


bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    channel = bot.get_channel(config.discord_bot_channel_id)
    message = bot_master.get_new_events()
    if len(message) > 0:
        await channel.send(content=message)


@bot.slash_command()
async def start(ctx):
    await ctx.respond(bot_master.greetings_message)


@bot.slash_command()
async def week(ctx):
    await ctx.respond(bot_master.get_weekly_list())

