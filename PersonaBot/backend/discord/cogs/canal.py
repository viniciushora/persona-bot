import discord
import pickle
from discord.ext import commands

from cogs.database import Database

class Canal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def checar_canais(self):
        try:
            with open('canais.pickle', 'rb') as handle:
                canais = pickle.load(handle)
        except EOFError:
            canais = {"jogadores": {}, "inimigos": 0, "grupo": 0, "mestre": 0, "suporte": 0}
            with open('canais.pickle', 'wb') as handle:
                pickle.dump(canais, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()
            print("Canais criados pela primeira vez")

    @classmethod
    def carregar_canais(self):
        try:
            with open('canais.pickle', 'rb') as handle:
                canais = pickle.load(handle)
            return canais
        except:
            print("Erro nos canais")

    @classmethod
    def carregar_canais_jogadores(self):
        try:
            with open('canais.pickle', 'rb') as handle:
                canais = pickle.load(handle)
            canais_jogadores = canais["jogadores"]
            return canais_jogadores
        except:
            print("Erro nos canais.")

    @classmethod
    def carregar_canal_jogador(self, personagem):
        try:
            with open('canais.pickle', 'rb') as handle:
                canais = pickle.load(handle)
            canais_jogadores = canais["jogadores"]  
            return canais_jogadores[personagem]
        except:
            print("Erro nos canais.")

    @classmethod
    def carregar_canal_inimigos(self):
        try:
            with open('canais.pickle', 'rb') as handle:
                canais = pickle.load(handle)
            canais_inimigos = canais["inimigos"]
            return canais_inimigos
        except:
            print("Erro nos canais.")

    @classmethod
    def carregar_canal_grupo(self):
        try:
            with open('canais.pickle', 'rb') as handle:
                canais = pickle.load(handle)
            canal_grupo = canais["grupo"]  
            return canal_grupo
        except:
            print("Erro nos canais.")
    
    @classmethod
    def carregar_canal_mestre(self):
        try:
            with open('canais.pickle', 'rb') as handle:
                canais = pickle.load(handle)
            canal_mestre = canais["mestre"]
            return canal_mestre
        except:
            print("Erro nos canais.")
    
    @classmethod
    def carregar_canal_suporte(self):
        try:
            with open('canais.pickle', 'rb') as handle:
                canais = pickle.load(handle)
            canal_suporte = canais["suporte"]
            return canal_suporte
        except:
            print("Erro nos canais.")

    @commands.command(name='canal_jogador')
    async def mod_canal_jogador(self, ctx, personagem, canal : discord.TextChannel):
        personagem_id = Database.personagem_id(personagem)
        if personagem_id != False:
            canais = self.carregar_canais()
            canais_jogadores = canais["jogadores"]
            canal_inimigos = canais["inimigos"]
            canal_mestre = canais["mestre"]
            canal_grupo = canais["grupo"]
            canal_suporte = canais["suporte"]
            canais_jogadores[personagem] = canal.id
            await ctx.send(f"""O canal de **{personagem}** agora é o <#{canal.id}>""")
            canais = {"jogadores": canais_jogadores, "inimigos": canal_inimigos, "grupo": canal_grupo, "mestre": canal_mestre, "suporte": canal_suporte}
            self.atualizacao_canal(canais)
        else:
            await ctx.send("Este personagem não existe.")
    
    @commands.command(name='canal_geral')
    async def mod_canal_geral(self, ctx, tipo_canal, canal : discord.TextChannel):
        try:
            canais = self.carregar_canais()
            canais_jogadores = canais["jogadores"]
            canal_inimigos = canais["inimigos"]
            canal_mestre = canais["mestre"]
            canal_grupo = canais["grupo"]
            canal_suporte = canais["suporte"]
            if tipo_canal == "grupo":
                canal_grupo = canal.id
            elif tipo_canal == "inimigos":
                canal_inimigos = canal.id
            elif tipo_canal == "mestre":
                canal_mestre = canal.id
            elif tipo_canal == "suporte":
                canal_suporte = canal.id
            await ctx.send(f"""O canal do {tipo_canal} agora é o <#{canal.id}>""")
            canais = {"jogadores": canais_jogadores, "inimigos": canal_inimigos, "grupo": canal_grupo, "mestre": canal_mestre, "suporte": canal_suporte}
            self.atualizacao_canal(canais)
        except:
            await ctx.send("Canal incorreto.")

    def atualizacao_canal(self, canais):
        with open('canais.pickle', 'wb') as handle:
            pickle.dump(canais, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()
        
    @commands.command(name='canais')
    async def canais(self, ctx):
        canais = self.carregar_canais()
        canais_jogadores = canais["jogadores"]
        canal_inimigos = canais["inimigos"]
        canal_mestre = canais["mestre"]
        canal_grupo = canais["grupo"]
        canal_suporte = canais["suporte"]
        i = 0
        embed = discord.Embed(
            title="Lista dos canais",
            colour=discord.Colour.blue()
        )
        if canais_jogadores != {}:
            i += 1
            texto = ""
            for jogador in canais_jogadores:
                texto += f"""**{jogador}**: <#{canais_jogadores[jogador]}>\n"""
            texto = texto[:-1]
            embed.add_field(name="Jogadores", value=texto, inline=False)
        if canal_grupo != 0:
            i += 1
            embed.add_field(name="Grupo", value=f"""<#{canal_grupo}>""", inline=False)
        if canal_inimigos != 0:
            i += 1
            embed.add_field(name="Inimigos", value=f"""<#{canal_inimigos}>""", inline=False)
        if canal_mestre != 0:
            i += 1
            embed.add_field(name="Mestre", value=f"""<#{canal_mestre}>""", inline=False)
        if canal_suporte != 0:
            i += 1
            embed.add_field(name="Suporte", value=f"""<#{canal_suporte}>""", inline=False)
        if i > 0:
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Canal(bot))