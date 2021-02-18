import discord
import random
import pickle
from discord.ext import commands

from cogs.database import *
from cogs.canal import *

class Item(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def add_item(self, quant, item_id):
        contem_item = Database.item_no_inventario2(item_id)
        if contem_item != False:
            soma_item = Database.soma_item_database(item_id, contem_item[1], quant)
        else:
            add_item = Database.add_item_database(item_id, quant)

    @commands.command(name='add_item')
    async def adicionar_item(self, ctx, quant, *item):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            quant = int(quant)
            nome = ""
            for palavra in item:
                nome+=palavra + " "
            nome = nome[:-1]
            item_id = Database.item_id(nome)
            if item_id != False:
                contem_item = Database.item_no_inventario(nome)
                if contem_item != False:
                    soma_item = Database.soma_item_database(item_id, contem_item[1], quant)
                    if soma_item:
                        await canal.send(f"""**{quant} {nome}** adicionado(s) no inventário do grupo. Quantidade atual: ({contem_item[1]+quant})""")
                else:
                    add_item = Database.add_item_database(item_id, quant)
                    if add_item:
                        await canal.send(f"""**{quant} {nome}** adicionado(s) no inventário do grupo.""")
                    else:
                        await ctx.send(f"""**Erro interno**""")
            else:
                await ctx.send(f"""**{nome} não existe.**""")
        except:
            await ctx.send("Canal do grupo não registrado.")
    
    @commands.command(name='del_item')
    async def deletar_item(self, ctx, quant, *item):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            quant = int(quant)
            nome = ""
            for palavra in item:
                nome+=palavra + " "
            nome = nome[:-1]
            item_id = Database.item_id(nome)
            if item_id != False:
                contem_item = Database.item_no_inventario(nome)
                if contem_item != False:
                    if contem_item[1] > quant:
                        subtrai_item = Database.subtrai_item_database(item_id, contem_item[1], quant)
                        print(subtrai_item)
                        await canal.send(f"""**{quant} {nome}** removido(s) no inventário do grupo. Quantidade atual: ({contem_item[1]-quant})""")
                    else:
                        delete_item = Database.del_item_database(item_id)
                        await canal.send(f"""**{nome}** removido completamente do inventário do grupo.""")
                else:
                    await ctx.send(f"""**{nome}** não encontrado no inventário do grupo.""")
            else:
                await ctx.send(f"""**{nome} não existe.**""")
        except:
            await ctx.send("Canal do grupo não registrado.")
    
    @commands.command(name='modificar_dinheiro')
    async def modificar_dinheiro(self, ctx, quant):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            try:
                quant = int(quant)
                dinheiro_inicial = Database.dinheiro_grupo()
                dinheiro_final = dinheiro_inicial + quant
                novo_dinheiro = Database.modificar_dinheiro(dinheiro_final)
                if novo_dinheiro:
                    await canal.send(f"""Adicionado **R$ {quant}**; (Valor anterior: **R$ {dinheiro_inicial}**). O dinheiro do grupo agora é **R$ {dinheiro_final}**""")
                else:
                    await ctx.send(f"""Erro interno""")
            except:
                await ctx.send(f"""Valor incorreto""")
        except:
            await ctx.send("Canal do grupo não registrado.")
    
    @commands.command(name='setar_dinheiro')
    async def setar_dinheiro(self, ctx, quant):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            try:
                quant = int(quant)
                novo_dinheiro = Database.modificar_dinheiro(quant)
                if novo_dinheiro:
                    await canal.send(f"""O dinheiro do grupo agora é **R$ {quant}**""")
                else:
                    await ctx.send(f"""Erro interno""")
            except:
                await ctx.send(f"""Valor incorreto""")
        except:
            await ctx.send("Canal do grupo não registrado.")
    
    @commands.command(name='drop')
    async def drop(self, ctx, *shadow):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            nome = ""
            for palavra in shadow:
                nome+=palavra + " "
            nome = nome[:-1]
            shadow_id = Database.shadow_id(nome)
            drops = Database.itens_drop(shadow_id)
            lista_drops = []
            for item_id, chance in drops:
                dado = random.randint(0, 100)
                if dado <= chance:
                    self.add_item(1, item_id)
                    lista_drops.append(Database.nome_item(item_id))
            dinheiro_exp = Database.dinheiro_exp(shadow_id)
            dinheiro_inicial = dinheiro_exp[0]
            exp = dinheiro_exp[1]
            dinheiro1 = random.randint(dinheiro_inicial * 0.5, dinheiro_inicial)
            dinheiro_grupo = Database.dinheiro_grupo()
            dinheiro = dinheiro_grupo + dinheiro1
            add_dinheiro = Database.modificar_dinheiro(dinheiro)
            embed_drops = discord.Embed(
                    title=f"""**Drops de {nome}**""",
                    description=F"""Dinheiro: R$ {dinheiro1} ; Experiência : {exp}""",
                    colour=discord.Colour.green()
            )
            texto = ""
            if lista_drops != []:
                for drop in lista_drops:
                    texto += drop + "; "
                texto = texto[:-2]
            else:
                texto = "Sem itens dropados"
            embed_drops.add_field(name="Itens dropados", value=texto, inline=False)
            await canal.send(embed=embed_drops)
        except:
            await ctx.send("Canal do grupo não registrado ou informações do dado erradas.")
    
    @commands.command(name='equipar')
    async def equipar(self, ctx, personagem, *item):
        try:
            nome = ""
            for palavra in item:
                nome+=palavra + " "
            nome = nome[:-1]
            personagem_id = Database.personagem_id(personagem)
            if personagem_id != False:
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
                item_id = Database.item_id(nome)
                if item_id != False:
                    contem_item = Database.item_no_inventario(nome)
                    if contem_item != False:
                        tipo_item_id = Database.tipo_item_id(item_id)
                        equip = Database.equipar_item(personagem_id, item_id, tipo_item_id)
                        if equip == False:
                            await canal.send("Este item não é equipável")
                        elif tipo_item_id == 7:
                            await canal.send(f"""**{nome}** agora é a arma corpo-a-corpo equipada de **{personagem}**""")
                        elif tipo_item_id == 8:
                            await canal.send(f"""**{nome}** agora é a arma à distância equipada de **{personagem}**""")
                        elif tipo_item_id == 9:
                            await canal.send(f"""**{nome}** agora é a armadura equipado de **{personagem}**""")
                        else:
                            await canal.send(f"""**{nome}** agora é o acessório equipado de **{personagem}**""")
                    else:
                        await ctx.send("Este item não está no inventário do grupo.")
                else:
                    await ctx.send("Este item não existe.")
            else:
                await ctx.send("Este personagem não existe.")
        except:
            await ctx.send("Canal do jogador não registrado.")
    
    @commands.command(name='desequipar')
    async def desequipar(self, ctx, personagem, *item):
        try:
            nome = ""
            for palavra in item:
                nome+=palavra + " "
            nome = nome[:-1]
            personagem_id = Database.personagem_id(personagem)
            if personagem_id != False:
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
                item_id = Database.item_id(nome)
                if item_id != False:
                    contem_item = Database.item_no_inventario(nome)
                    if contem_item != False:
                        tipo_item_id = Database.tipo_item_id(item_id)
                        item_equipado = Database.item_equipado(personagem_id, item_id, tipo_item_id)
                        if item_equipado:
                            desequip = Database.desequipar_item(personagem_id, tipo_item_id)
                            if desequip == False:
                                await canal.send("Este item não é equipável")
                            elif tipo_item_id == 7:
                                await canal.send(f"""**{nome}** não está mais equipado(a) como arma corpo-a-corpo de **{personagem}**""")
                            elif tipo_item_id == 8:
                                await canal.send(f"""**{nome}** não está mais equipado(a) como arma à distância equipada de **{personagem}**""")
                            elif tipo_item_id == 9:
                                await canal.send(f"""**{nome}** não está mais equipado(a) como armadura equipada de **{personagem}**""")
                            else:
                                await canal.send(f"""**{nome}** não está mais equipado(a) como acessório equipado de **{personagem}**""")
                        else:
                            await ctx.send("Este item não está equipado.")
                    else:
                        await ctx.send("Este item não está no inventário do grupo.")
                else:
                    await ctx.send("Este item não existe.")
            else:
                await ctx.send("Este personagem não existe.")
        except:
            await ctx.send("Canal do jogador não registrado.")

    @commands.command(name='inventario')
    async def inventario(self, ctx):
        global canal_grupo
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            itens = Database.inventario_grupo()
            consumiveis = []
            cartas = []
            materiais = []
            tesouros = []
            essenciais = []
            itens_chave = []
            armas_meelee = []
            armas_ranged = []
            armaduras = []
            acessorios = []
            roupas = []
            for item, tipo_item, quant in itens:
                if tipo_item == "Consumíveis":
                    consumiveis.append((item,quant))
                elif tipo_item == "Cartas de Habilidade":
                    cartas.append((item,quant))
                elif tipo_item == "Materiais":
                    materiais.append((item,quant))
                elif tipo_item == "Tesouros":
                    tesouros.append((item,quant))
                elif tipo_item == "Essenciais":
                    essenciais.append((item,quant))
                elif tipo_item == "Itens-chave":
                    itens_chave.append((item,quant))
                elif tipo_item == "Armas Corpo-a-corpo":
                    armas_meelee.append((item,quant))
                elif tipo_item == "Armas à distância":
                    armas_ranged.append((item,quant))
                elif tipo_item == "Armadura":
                    armaduras.append((item,quant))
                elif tipo_item == "Acessórios":
                    acessorios.append((item,quant))
                else:
                    roupas.append((item,quant))
            dinheiro = Database.dinheiro_grupo()
            inventario = discord.Embed(
                    title=f"""**Inventário do grupo**""",
                    description=F"""Dinheiro: R$ {dinheiro}""",
                    colour=discord.Colour.blue()
            )
            if consumiveis != []:
                texto = ""
                for item, quant in consumiveis:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Consumíveis", value=texto, inline=False)
            if cartas != []:
                texto = ""
                for item, quant in cartas:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Cartas de Habilidade", value=texto, inline=False)
            if materiais != []:
                texto = ""
                for item, quant in materiais:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Materiais", value=texto, inline=False)
            if tesouros != []:
                texto = ""
                for item, quant in tesouros:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Tesouros", value=texto, inline=False)
            if essenciais != []:
                texto = ""
                for item, quant in essenciais:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Essenciais", value=texto, inline=False)
            if itens_chave != []:
                texto = ""
                for item, quant in itens_chave:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Itens-chave", value=texto, inline=False)
            if armas_meelee != []:
                texto = ""
                for item, quant in armas_meelee:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Armas Corpo-a-corpo", value=texto, inline=False)
            if armas_ranged != []:
                texto = ""
                for item, quant in armas_ranged:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Armas à distância", value=texto, inline=False)
            if armaduras != []:
                texto = ""
                for item, quant in armaduras:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Armaduras", value=texto, inline=False)
            if acessorios != []:
                texto = ""
                for item, quant in acessorios:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Acessórios", value=texto, inline=False)
            if roupas != []:
                texto = ""
                for item, quant in roupas:
                    texto += f"""{item} x{quant}; """
                texto = texto[:-2]
                inventario.add_field(name="Roupas", value=texto, inline=False)
            await canal.send(embed=inventario)
        except:
            await ctx.send("Canal do grupo não registrado.")

def setup(bot):
    bot.add_cog(Item(bot))