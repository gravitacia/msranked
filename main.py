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


lobby_count = 1
max_players = 4
players_queue = []


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command(name='ranked_search')
async def ranked_search(ctx):
    author = ctx.author
    if author in players_queue:
        await ctx.send("You are already in the queue!")
        return
    players_queue.append(author)
    await ctx.send("You have been added to the queue.")

    if len(players_queue) >= max_players:
        global lobby_count
        lobby_name = f'ranked_loby {lobby_count}'
        lobby_count += 1

        role = await ctx.guild.create_role(name=lobby_name, mentionable=True)

        for player in players_queue:
            await player.add_roles(role)

        category = discord.utils.get(ctx.guild.categories, name='private')
        channel = await category.create_text_channel(lobby_name)
        await channel.set_permissions(role, read_messages=True, send_messages=True)

        players_queue.clear()
        await ctx.send(f'A room has been formed {channel.mention} for playing {lobby_name}.')


@bot.command(name='delete_lobby')
@commands.has_permissions(manage_channels=True)
async def delete_lobby(ctx, lobby_name: str):
    channel = discord.utils.get(ctx.guild.text_channels, name=lobby_name)
    role = discord.utils.get(ctx.guild.roles, name=lobby_name)
    if channel and role:
        await channel.delete()
        await role.delete()
        await ctx.send(f'Room {lobby_name} has been deleted.')
    else:
        await ctx.send(f'The room {lobby_name} was not found or could not be deleted.')


bot.run('MTEyMjc4NjgxMjcwNDg2MjI2MA.GOjpKk.oS9wbTSJ4bSsx6O18dWqyA600t0tvxRNpGc3Fo')
