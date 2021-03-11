from cogs.canal import Canal
from cogs.ficha import Ficha
from cogs.database import Database

from discord.ext import commands

bot = commands.Bot(command_prefix=Database.prefix())
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

@bot.command()
async def comandos(ctx):
    await ctx.send("Lista de comandos: https://github.com/ViniciusHora1009/persona-bot/blob/main/comandos.md")

bot.load_extension("cogs.dado")
bot.load_extension("cogs.ficha")
bot.load_extension("cogs.item")
bot.load_extension("cogs.persona")
bot.load_extension("cogs.canal")
bot.load_extension("cogs.combate")
bot.run(Database.token())