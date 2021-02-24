import discord
import random
from discord.ext import commands

from cogs.database import Database
from cogs.canal import Canal

class Dado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rolagem')
    async def rolagem(self, ctx, personagem, dados, lados):
        try:
            personagem_id = Database.personagem_id(personagem)
            if personagem_id != False:
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
                usuario = Database.discord_user(personagem_id)
                await Dado.rolagem_pronta(self.bot, canal, personagem, usuario, dados, lados)
            else:
                await ctx.send("Este personagem não existe.")
        except ValueError:
            await ctx.send("Canal do jogador não registrado ou informações do dado erradas.")

    @commands.command(name='rolldice')
    async def rolldice(self, ctx):
        quant_dados = 0
        lados = 0
        await ctx.send("Quantos dados?")
        msg = await self.bot.wait_for('message')
        mensagem = msg.content
        try:
            quant_dados = int(mensagem)
        except ValueError:
            await ctx.send("Incorrect parameter.")
        if quant_dados > 0 and quant_dados < 25:
            await ctx.send("Digite a quantidade de lados:")
            msg = await self.bot.wait_for('message')
            mensagem = msg.content
            try:
                lados = int(mensagem)
            except ValueError:
                await ctx.send("Parâmetro incorreto.")
        await self.gerar_dado_solto(ctx, lados, quant_dados)

    @commands.command(name='roll', aliases=['r'])
    async def fast_rolldice(self, ctx, dado):
        quant_dados = 0
        lados = 0
        try:
            for i in range(len(dado)):
                if dado[i].upper() == "D":
                    posicao_x = i
                    quant_dados = int(dado[:posicao_x])
                    if quant_dados > 0 and quant_dados < 25:
                        lados = int(dado[posicao_x + 1:len(dado)])
                    break
            await self.gerar_dado_solto(ctx, lados, quant_dados)
        except:
            await ctx.send("Parâmetros incorretos. Quantidade de dados deve ser entre 1 e 25 / Quantidade de lados deve ser um inteiro maior que 0.")

    @classmethod
    async def rolagem_pronta(self, bot, canal, personagem, usuario, dados, lados):
        if (dados > 0 and dados < 25) and (lados > 0):
            dado = discord.Embed(
                title=f'Rolagem de {dados} D{lados} por {personagem} :game_die: ',
                description="Clique no dado abaixo para rodar o dado.",
                colour=discord.Colour.greyple()
            )
            embed_dado = await canal.send(embed=dado)
            await embed_dado.add_reaction(emoji='🎲')
            rolagem = 0
            while rolagem == 0:
                reaction, user = await bot.wait_for('reaction_add')
                if str(reaction.emoji) == '🎲' and str(user) == usuario:
                    rolagem = 1
                    await embed_dado.delete()
                    total = 0
                    soma = ""
                    dado1 = discord.Embed(
                        title=f'Rolagem de {dados} D{lados} por {personagem} :game_die: ',
                        colour=discord.Colour.greyple()
                    )
                    for i in range(dados):
                        num = random.randint(1, lados)
                        dado1.add_field(name=f'Dice #{i + 1}', value=num, inline=True)
                        total += num
                        soma += str(num) + " + "
                    soma = soma[:len(soma) - 2]
                    dado1.description = f'SUM: {soma} = **{total}**'
                    await canal.send(embed=dado1)
                    return total
        else:
            await canal.send("Parâmetros incorretos.")

    async def gerar_dado_solto(self, ctx, lados, quant_dados):
        if lados > 0:
            dado = discord.Embed(
                title=f'Rolagem de {quant_dados} D{lados} por {str(ctx.author)} :game_die: ',
                colour=discord.Colour.greyple()
            )
            total = 0
            soma = ""
            for i in range(quant_dados):
                num = random.randint(1, lados)
                dado.add_field(name=f'Dice #{i + 1}', value=num, inline=True)
                total += num
                soma += str(num) + " + "
            soma = soma[:len(soma) - 2]
            dado.description = f'SUM: {soma} = **{total}**'
            await ctx.send(embed=dado)
        else:
            await ctx.send("Você falhou em rodar o(s) dado(s), tente novamente.")

def setup(bot):
    bot.add_cog(Dado(bot))