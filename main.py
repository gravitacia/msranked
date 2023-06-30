import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def ms_ranked(ctx):
    message = await ctx.send('lol')
    await message.add_reaction('👍')


bot.run('privateKey')
