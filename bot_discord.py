import discord
import bot_master

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    channel = bot.get_channel(1010249090010988586)
    await channel.send(content=bot_master.get_weekly_list())


@bot.slash_command()
async def start(ctx):
    await ctx.respond(bot_master.greetings_message)

@bot.slash_command()
async def week(ctx):
    await ctx.respond(bot_master.get_weekly_list())

