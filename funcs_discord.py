import discord
import funcs_generic

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command()
async def start(ctx):
    await ctx.respond(funcs_generic.greetings_message)

@bot.slash_command()
async def week(ctx):
    await ctx.respond(funcs_generic.get_weekly_list())
