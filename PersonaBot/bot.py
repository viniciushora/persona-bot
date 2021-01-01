import discord
import random
import pickle
from discord.utils import get
import logging
import asyncio
import json

from cogs.database import *
from cogs.dado import *

from discord.ext import commands

f = open('config.json')
data = json.load(f)


bot = commands.Bot(command_prefix=data['prefix'])
bot.remove_command("help")

servers = []

@bot.event
async def on_member_join(member):
    print("Member Join")

@bot.event
async def on_guild_join(guild):
    print("Guild Join")
    info = {}
    shadows = Database.lista_shadows_id()
    print(shadows)
    if shadows:
        for shadow in shadows:
            info[shadow] = [0,0,0,0,0,0,0,0,0,0,0]
        with open('info.pickle', 'wb') as handle:
            pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()

@bot.event
async def on_ready():
    print('Estou funcionando como {0.user}'.format(bot))
    print("Tudo Ok")

@bot.command()
async def mostrar_ficha(ctx, *persona):
    nome = ""
    for palavra in persona:
        nome+=palavra + " "
    nome = nome[:-1]
    try:   
        ficha = Database.ficha_persona(nome)
        nome = ficha[0][0]
        foto = ficha[0][1]
        arcana = ficha[0][2]
        embed = discord.Embed(
            title=f"""**{nome}**""",
            colour=discord.Colour.red()
        )
        embed.set_image(url=foto)
        embed.add_field(name=f"""**Arcana**""", value=arcana, inline=False)
        embed.add_field(name=f"""**{ficha[1][0][0]}**""", value=ficha[1][0][1], inline=False)
        embed.add_field(name=f"""**{ficha[1][1][0]}**""", value=ficha[1][1][1], inline=False)
        embed.add_field(name=f"""**{ficha[1][2][0]}**""", value=ficha[1][2][1], inline=False)
        embed.add_field(name=f"""**{ficha[1][3][0]}**""", value=ficha[1][3][1], inline=False)
        embed.add_field(name=f"""**{ficha[1][4][0]}**""", value=ficha[1][4][1], inline=False)
        embed.add_field(name=f"""**{ficha[1][5][0]}**""", value=ficha[1][5][1], inline=False)
        embed.add_field(name=f"""**{ficha[1][6][0]}**""", value=ficha[1][6][1], inline=False)
        embed2 = discord.Embed(
            title=f"""**Fraquezas**""",
            colour=discord.Colour.red()
        )
        embed2.add_field(name=f"""<:phys:790320130810839101>""", value=ficha[2][0][1], inline=True)
        embed2.add_field(name=f"""<:gun:790320131028287488>""", value=ficha[2][1][1], inline=True)
        embed2.add_field(name=f"""<:fire:790320130483421245>""", value=ficha[2][2][1], inline=True)
        embed2.add_field(name=f"""<:ice:790320130738356224>""", value=ficha[2][3][1], inline=True)
        embed2.add_field(name=f"""<:elec:790320130151809047>""", value=ficha[2][4][1], inline=True)
        embed2.add_field(name=f"""<:wind:790320130521169922>""", value=ficha[2][5][1], inline=True)
        embed2.add_field(name=f"""<:psy:790320130772566046>""", value=ficha[2][6][1], inline=True)
        embed2.add_field(name=f"""<:nuclear:790320130584084532>""", value=ficha[2][7][1], inline=True)
        embed2.add_field(name=f"""<:bless:790320130746744892>""", value=ficha[2][8][1], inline=True)
        embed2.add_field(name=f"""<:curse:790320130387214336>""", value=ficha[2][9][1], inline=True)
        embed2.add_field(name=f"""<:almighty:790320130297954374>""", value=ficha[2][10][1], inline=True)
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)
    except:
        await ctx.send("**Ficha não encontrada, digite novamente e corretamente.**")
    
@bot.command()
async def info_shadow(ctx, *shadow):
    nome = ""
    for palavra in shadow:
        nome += palavra + " "
    nome = nome[:-1]
    with open('info.pickle', 'rb') as handle:
        info = pickle.load(handle)
    try:
        ficha = Database.ficha_shadow(nome)
        shadow_id = ficha[0][0]
        nome = ficha[0][1]
        foto = ficha[0][2]
        arcana = ficha[0][3]
        embed = discord.Embed(
            title=f"""**{nome}**""",
            colour=discord.Colour.red()
        )
        embed.set_image(url=foto)
        fraquezas = ['???','???','???','???','???','???','???','???','???','???','???']
        if info[shadow_id][0] == 1:
            fraquezas[0] = ficha[1][0][1]
        if info[shadow_id][1] == 1:
            fraquezas[1] = ficha[1][1][1]
        if info[shadow_id][2] == 1:
            fraquezas[2] = ficha[1][2][1]
        if info[shadow_id][3] == 1:
            fraquezas[3] = ficha[1][3][1]
        if info[shadow_id][4] == 1:
            fraquezas[4] = ficha[1][4][1]
        if info[shadow_id][5] == 1:
            fraquezas[5] = ficha[1][5][1]
        if info[shadow_id][6] == 1:
            fraquezas[6] = ficha[1][6][1]
        if info[shadow_id][7] == 1:
            fraquezas[7] = ficha[1][7][1]
        if info[shadow_id][8] == 1:
            fraquezas[8] = ficha[1][8][1]
        if info[shadow_id][9] == 1:
            fraquezas[9] = ficha[1][9][1]
        if info[shadow_id][10] == 1:
            fraquezas[10] = ficha[1][10][1]
        embed.add_field(name=f"""<:phys:790320130810839101>""", value=fraquezas[0], inline=True)
        embed.add_field(name=f"""<:gun:790320131028287488>""", value=fraquezas[1], inline=True)
        embed.add_field(name=f"""<:fire:790320130483421245>""", value=fraquezas[2], inline=True)
        embed.add_field(name=f"""<:ice:790320130738356224>""", value=fraquezas[3], inline=True)
        embed.add_field(name=f"""<:elec:790320130151809047>""", value=fraquezas[4], inline=True)
        embed.add_field(name=f"""<:wind:790320130521169922>""", value=fraquezas[5], inline=True)
        embed.add_field(name=f"""<:psy:790320130772566046>""", value=fraquezas[6], inline=True)
        embed.add_field(name=f"""<:nuclear:790320130584084532>""", value=fraquezas[7], inline=True)
        embed.add_field(name=f"""<:bless:790320130746744892>""", value=fraquezas[8], inline=True)
        embed.add_field(name=f"""<:curse:790320130387214336>""", value=fraquezas[9], inline=True)
        embed.add_field(name=f"""<:almighty:790320130297954374>""", value=fraquezas[10], inline=True)
        await ctx.send(embed=embed)
    except:
        await ctx.send("**Shadow não encontrada, digite novamente e corretamente.**")

@bot.command()
async def revelar_afinidade(ctx, *shadow):
    nome = ""
    for palavra in shadow:
        nome+=palavra + " "
    nome = nome[:-1]
    shadow_id = Database.shadow_id(nome)
    info = {}
    if shadow_id != False:
        with open('info.pickle', 'rb') as handle:
            info = pickle.load(handle)
        select = discord.Embed(
            title=f"""**Revelando afinidades elementais de {nome}**""",
            description="Reaja com o elemento desejado (:arrow_up_small: para revelação completa)",
            colour=discord.Colour.blue()
        )
        emb_msg = await ctx.send(embed=select)
        await emb_msg.add_reaction(emoji="<:phys:790320130810839101>")
        await emb_msg.add_reaction(emoji="<:gun:790320131028287488>")
        await emb_msg.add_reaction(emoji="<:fire:790320130483421245>")
        await emb_msg.add_reaction(emoji="<:ice:790320130738356224>")
        await emb_msg.add_reaction(emoji="<:elec:790320130151809047>")
        await emb_msg.add_reaction(emoji="<:wind:790320130521169922>")
        await emb_msg.add_reaction(emoji="<:psy:790320130772566046>")
        await emb_msg.add_reaction(emoji="<:nuclear:790320130584084532>")
        await emb_msg.add_reaction(emoji="<:bless:790320130746744892>")
        await emb_msg.add_reaction(emoji="<:curse:790320130387214336>")
        await emb_msg.add_reaction(emoji="<:almighty:790320130297954374>")
        await emb_msg.add_reaction(emoji="🔼")
        await emb_msg.add_reaction(emoji="❌")
        ok = 0
        mensagem = ""
        while ok == 0:
            reaction, user = await bot.wait_for('reaction_add', timeout=None)
            if str(reaction.emoji) == "<:phys:790320130810839101>" and str(user) != "Persona Bot#0708":
                print(info)
                info[shadow_id][0] = 1
                ok = 1
                mensagem = f"""Afinidade **Física** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:gun:790320131028287488>" and str(user) != "Persona Bot#0708":
                info[shadow_id][1] = 1
                ok = 2
                mensagem = f"""Afinidade de **Arma de Fogo** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:fire:790320130483421245>" and str(user) != "Persona Bot#0708":
                info[shadow_id][2] = 1
                ok = 3
                mensagem = f"""Afinidade de **Fogo** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:ice:790320130738356224>" and str(user) != "Persona Bot#0708":
                info[shadow_id][3] = 1
                ok = 4
                mensagem = f"""Afinidade de **Gelo** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:elec:790320130151809047>" and str(user) != "Persona Bot#0708":
                info[shadow_id][4] = 1
                ok = 5
                mensagem = f"""Afinidade **Elétrica** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:wind:790320130521169922>" and str(user) != "Persona Bot#0708":
                info[shadow_id][5] = 1
                ok = 6
                mensagem = f"""Afinidade de **Vento** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:psy:790320130772566046>" and str(user) != "Persona Bot#0708":
                info[shadow_id][6] = 1
                ok = 7
                mensagem = f"""Afinidade de **Psy** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:nuclear:790320130584084532>" and str(user) != "Persona Bot#0708":
                info[shadow_id][7] = 1
                ok = 8
                mensagem = f"""Afinidade **Nuclear** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:bless:790320130746744892>" and str(user) != "Persona Bot#0708":
                info[shadow_id][8] = 1
                ok = 9
                mensagem = f"""Afinidade de **Benção** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:curse:790320130387214336>" and str(user) != "Persona Bot#0708":
                info[shadow_id][9] = 1
                ok = 10
                mensagem = f"""Afinidade de **Maldição** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "<:almighty:790320130297954374>" and str(user) != "Persona Bot#0708":
                info[shadow_id][10] = 1
                ok = 11
                mensagem = f"""Afinidade de **Onipotência** de {nome} agora é conhecida pelo grupo"""
            if str(reaction.emoji) == "🔼" and str(user) != "Persona Bot#0708":
                info[shadow_id][0] = 1
                info[shadow_id][1] = 1
                info[shadow_id][2] = 1
                info[shadow_id][3] = 1
                info[shadow_id][4] = 1
                info[shadow_id][5] = 1
                info[shadow_id][6] = 1
                info[shadow_id][7] = 1
                info[shadow_id][8] = 1
                info[shadow_id][9] = 1
                info[shadow_id][10] = 1
                ok = 12
            if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                ok = 13
        await emb_msg.delete()
        confirmacao = discord.Embed(
            title=f"""**Afinidades conhecidas de {nome} atualizadas**""",
            description=mensagem,
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=confirmacao)
    else:
        await ctx.send("**Shadow não existente**")
    if info != {}:
        with open('info.pickle', 'wb') as handle:
            pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()
    
@bot.command()
async def esconder_afinidade(ctx, *shadow):
    nome = ""
    for palavra in shadow:
        nome+=palavra + " "
    nome = nome[:-1]
    shadow_id = Database.shadow_id(nome)
    info = {}
    if shadow_id != False:
        with open('info.pickle', 'rb') as handle:
            info = pickle.load(handle)
        select = discord.Embed(
            title=f"""**Escondendo afinidades elementais de {nome}**""",
            description="Reaja com o elemento desejado (:arrow_up_small: para desconhecimento completo)",
            colour=discord.Colour.blue()
        )
        emb_msg = await ctx.send(embed=select)
        await emb_msg.add_reaction(emoji="<:phys:790320130810839101>")
        await emb_msg.add_reaction(emoji="<:gun:790320131028287488>")
        await emb_msg.add_reaction(emoji="<:fire:790320130483421245>")
        await emb_msg.add_reaction(emoji="<:ice:790320130738356224>")
        await emb_msg.add_reaction(emoji="<:elec:790320130151809047>")
        await emb_msg.add_reaction(emoji="<:wind:790320130521169922>")
        await emb_msg.add_reaction(emoji="<:psy:790320130772566046>")
        await emb_msg.add_reaction(emoji="<:nuclear:790320130584084532>")
        await emb_msg.add_reaction(emoji="<:bless:790320130746744892>")
        await emb_msg.add_reaction(emoji="<:curse:790320130387214336>")
        await emb_msg.add_reaction(emoji="<:almighty:790320130297954374>")
        await emb_msg.add_reaction(emoji="🔼")
        await emb_msg.add_reaction(emoji="❌")
        ok = 0
        mensagem = ""
        while ok == 0:
            reaction, user = await bot.wait_for('reaction_add', timeout=None)
            if str(reaction.emoji) == "<:phys:790320130810839101>" and str(user) != "Persona Bot#0708":
                print(info)
                info[shadow_id][0] = 0
                ok = 1
                mensagem = f"""Afinidade **Física** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:gun:790320131028287488>" and str(user) != "Persona Bot#0708":
                info[shadow_id][1] = 0
                ok = 2
                mensagem = f"""Afinidade de **Arma de Fogo** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:fire:790320130483421245>" and str(user) != "Persona Bot#0708":
                info[shadow_id][2] = 0
                ok = 3
                mensagem = f"""Afinidade de **Fogo** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:ice:790320130738356224>" and str(user) != "Persona Bot#0708":
                info[shadow_id][3] = 0
                ok = 4
                mensagem = f"""Afinidade de **Gelo** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:elec:790320130151809047>" and str(user) != "Persona Bot#0708":
                info[shadow_id][4] = 0
                ok = 5
                mensagem = f"""Afinidade **Elétrica** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:wind:790320130521169922>" and str(user) != "Persona Bot#0708":
                info[shadow_id][5] = 0
                ok = 6
                mensagem = f"""Afinidade de **Vento** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:psy:790320130772566046>" and str(user) != "Persona Bot#0708":
                info[shadow_id][6] = 0
                ok = 7
                mensagem = f"""Afinidade de **Psy** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:nuclear:790320130584084532>" and str(user) != "Persona Bot#0708":
                info[shadow_id][7] = 0
                ok = 8
                mensagem = f"""Afinidade **Nuclear** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:bless:790320130746744892>" and str(user) != "Persona Bot#0708":
                info[shadow_id][8] = 0
                ok = 9
                mensagem = f"""Afinidade de **Benção** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:curse:790320130387214336>" and str(user) != "Persona Bot#0708":
                info[shadow_id][9] = 0
                ok = 10
                mensagem = f"""Afinidade de **Maldição** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "<:almighty:790320130297954374>" and str(user) != "Persona Bot#0708":
                info[shadow_id][10] = 0
                ok = 11
                mensagem = f"""Afinidade de **Onipotência** de {nome} agora é desconhecida pelo grupo"""
            if str(reaction.emoji) == "🔼" and str(user) != "Persona Bot#0708":
                info[shadow_id][0] = 0
                info[shadow_id][1] = 0
                info[shadow_id][2] = 0
                info[shadow_id][3] = 0
                info[shadow_id][4] = 0
                info[shadow_id][5] = 0
                info[shadow_id][6] = 0
                info[shadow_id][7] = 0
                info[shadow_id][8] = 0
                info[shadow_id][9] = 0
                info[shadow_id][10] = 0
                ok = 12
            if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                ok = 13
        await emb_msg.delete()
        confirmacao = discord.Embed(
            title=f"""**Afinidades conhecidas de {nome} atualizadas**""",
            description=mensagem,
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=confirmacao)
    else:
        await ctx.send("**Shadow não existente**")
    if info != {}:
        with open('info.pickle', 'wb') as handle:
            pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()

@bot.command()
async def add_item(ctx, quant, *item):
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
                await ctx.send(f"""**{quant} {nome}** adicionado(s) no inventário do grupo. Quantidade atual: ({contem_item[1]+quant})""")
        else:
            add_item = Database.add_item_database(item_id, quant)
            if add_item:
                await ctx.send(f"""**{quant} {nome}** adicionado(s) no inventário do grupo.""")
            else:
                await ctx.send(f"""**Erro interno**""")
    else:
        await ctx.send(f"""**{nome} não existe.**""")

@bot.command()
async def del_item(ctx, quant, *item):
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
                await ctx.send(f"""**{quant} {nome}** removido(s) no inventário do grupo. Quantidade atual: ({contem_item[1]-quant})""")
            else:
                delete_item = Database.del_item_database(item_id)
                await ctx.send(f"""**{nome}** removido completamente do inventário do grupo.""")
        else:
            await ctx.send(f"""**{nome}** não encontrado no inventário do grupo.""")
    else:
        await ctx.send(f"""**{nome} não existe.**""")
    
@bot.command()
async def inventario(ctx):
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
    await ctx.send(embed=inventario)

@bot.command()
async def modificar_dinheiro(ctx, quant):
    try:
        quant = int(quant)
        dinheiro_inicial = Database.dinheiro_grupo()
        dinheiro_final = dinheiro_inicial + quant
        novo_dinheiro = Database.modificar_dinheiro(dinheiro_final)
        if novo_dinheiro:
            await ctx.send(f"""Adicionado **R$ {quant}**; (Valor anterior: **R$ {dinheiro_inicial}**). O dinheiro do grupo agora é **R$ {dinheiro_final}**""")
        else:
            await ctx.send(f"""Erro interno""")
    except:
        await ctx.send(f"""Valor incorreto""")

@bot.command()
async def setar_dinheiro(ctx, quant):
    try:
        quant = int(quant)
        novo_dinheiro = Database.modificar_dinheiro(quant)
        if novo_dinheiro:
            await ctx.send(f"""O dinheiro do grupo agora é **R$ {quant}**""")
        else:
            await ctx.send(f"""Erro interno""")
    except:
        await ctx.send(f"""Valor incorreto""")
    
@bot.command()
async def testar_rolagem(ctx):
    dado = await Dado.rolagem_pronta(bot,ctx,"João","Freefes#9639",1,100)

@bot.command()
async def drop(ctx, *shadow):
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
            add_item(1, item_id)
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
    await ctx.send(embed=embed_drops)        


def add_item(quant, item_id):
    contem_item = Database.item_no_inventario2(item_id)
    if contem_item != False:
        soma_item = Database.soma_item_database(item_id, contem_item[1], quant)
    else:
        add_item = Database.add_item_database(item_id, quant)

@bot.command()
async def equipar(ctx, personagem, *item):
    nome = ""
    for palavra in item:
        nome+=palavra + " "
    nome = nome[:-1]
    personagem_id = Database.personagem_id(personagem)
    if personagem_id != False:
        item_id = Database.item_id(nome)
        if item_id != False:
            contem_item = Database.item_no_inventario(nome)
            if contem_item != False:
                tipo_item_id = Database.tipo_item_id(item_id)
                equip = Database.equipar_item(personagem_id, item_id, tipo_item_id)
                if equip == False:
                    await ctx.send("Este item não é equipável")
                elif tipo_item_id == 7:
                    await ctx.send(f"""**{nome}** agora é a arma corpo-a-corpo equipada de **{personagem}**""")
                elif tipo_item_id == 8:
                    await ctx.send(f"""**{nome}** agora é a arma à distância equipada de **{personagem}**""")
                elif tipo_item_id == 9:
                    await ctx.send(f"""**{nome}** agora é a armadura equipada de **{personagem}**""")
                else:
                    await ctx.send(f"""**{nome}** agora é o acessório equipado de **{personagem}**""")
            else:
                await ctx.send("Este item não está no inventário do grupo.")
        else:
            await ctx.send("Este item não existe.")
    else:
        await ctx.send("Este personagem não existe.")

bot.load_extension("cogs.dado")
bot.run(data['token'])