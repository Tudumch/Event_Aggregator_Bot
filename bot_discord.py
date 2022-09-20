import discord

from bot_master import Bot_Master_Parent
import config


bot = discord.Bot()
bot_master = Bot_Master_Parent


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    channel = bot.get_channel(config.discord_bot_channel_id)
    message = bot_master.get_message_with_new_events()
    if len(message) > 0:
        await channel.send(content=message)


@bot.slash_command()
async def start(ctx):
    await ctx.respond(bot_master.greetings_message)


@bot.slash_command()
async def week(ctx):
    message = bot_master.get_message_with_weekly_events()
    if len(message) > 0:
        await ctx.respond(message)
    else:
        await ctx.respond(bot_master.weekly_events_not_found_message)

