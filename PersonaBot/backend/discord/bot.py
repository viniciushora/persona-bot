import discord
import json

from cogs.canal import *
from cogs.ficha import *

from discord.ext import commands

f = open('config.json')
data = json.load(f)

bot = commands.Bot(command_prefix=data['prefix'])
bot.remove_command("help")

@bot.event
async def on_guild_join(guild):
    print("Guild Join")
    Ficha.iniciar_info()

@bot.event
async def on_ready():
    print('Estou funcionando como {0.user}'.format(bot))
    Canal.checar_canais()
    print("Tudo Ok")

bot.load_extension("cogs.dado")
bot.load_extension("cogs.ficha")
bot.load_extension("cogs.item")
bot.load_extension("cogs.persona")
bot.load_extension("cogs.canal")
bot.load_extension("cogs.combate")
bot.run(data['token'])