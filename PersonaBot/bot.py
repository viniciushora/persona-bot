import discord
import random
import pickle
from discord.utils import get
import logging
import asyncio
import json
import math

from cogs.database import *
from cogs.dado import *

from discord.ext import commands

f = open('config.json')
data = json.load(f)

bot = commands.Bot(command_prefix=data['prefix'])
bot.remove_command("help")

global horda, party, horda_mults, party_mults

servers = []
horda = []
party = []
horda_mult_atk = []
party_mult_atk = []
horda_mult_def = []
party_mult_def = []
horda_mult_acc = []
party_mult_acc = []
horda_mult_evs = []
party_mult_evs = []
horda_elem_dano = []
party_elem_dano = []
party_mult_crit = []
horda_mult_crit = []

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
async def mostrar_ficha(ctx,  canal : discord.TextChannel, *persona):
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
        persona_id = Database.persona_id(nome)
        nivel = Database.nivel_persona(persona_id)
        embed.set_image(url=foto)
        embed.add_field(name=f"""**Nível base**""", value=nivel, inline=False)
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
        await canal.send(embed=embed)
        await canal.send(embed=embed2)
    except:
        await ctx.send("**Ficha não encontrada, digite novamente e corretamente.**")
    
@bot.command()
async def info_shadow(ctx, canal : discord.TextChannel, *shadow):
    nome = ""
    for palavra in shadow:
        nome += palavra + " "
    nome = nome[:-1]
    with open('info.pickle', 'rb') as handle:
        info = pickle.load(handle)
    try:
        ficha = Database.ficha_shadow(nome)
        persona_id = Database.persona_id_shadow(nome)
        nivel = Database.nivel_persona(persona_id)
        shadow_id = ficha[0][0]
        nome = ficha[0][1]
        foto = ficha[0][2]
        arcana = ficha[0][3]
        embed = discord.Embed(
            title=f"""**{nome}**""",
            colour=discord.Colour.red()
        )
        embed.set_image(url=foto)
        embed.add_field(name=f"""Nível base""", value=nivel, inline=False)
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
        await canal.send(embed=embed)
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
async def add_item(ctx, canal : discord.TextChannel, quant, *item):
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

@bot.command()
async def del_item(ctx, canal : discord.TextChannel, quant, *item):
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
    
@bot.command()
async def inventario(ctx, canal : discord.TextChannel):
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

@bot.command()
async def modificar_dinheiro(ctx, canal : discord.TextChannel, quant):
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

@bot.command()
async def setar_dinheiro(ctx, canal : discord.TextChannel, quant):
    try:
        quant = int(quant)
        novo_dinheiro = Database.modificar_dinheiro(quant)
        if novo_dinheiro:
            await canal.send(f"""O dinheiro do grupo agora é **R$ {quant}**""")
        else:
            await ctx.send(f"""Erro interno""")
    except:
        await ctx.send(f"""Valor incorreto""")
    
@bot.command()
async def rolagem(ctx, canal : discord.TextChannel, personagem, dados, lados):
    personagem_id = Database.personagem_id(personagem)
    usuario = Database.discord_user()
    dado = await Dado.rolagem_pronta(bot, canal, personagem, usuario, dados, lados)

@bot.command()
async def drop(ctx, canal : discord.TextChannel, *shadow):
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
    await canal.send(embed=embed_drops)        


def add_item(quant, item_id):
    contem_item = Database.item_no_inventario2(item_id)
    if contem_item != False:
        soma_item = Database.soma_item_database(item_id, contem_item[1], quant)
    else:
        add_item = Database.add_item_database(item_id, quant)

@bot.command()
async def equipar(ctx, canal : discord.TextChannel, personagem, *item):
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
    
@bot.command()
async def desequipar(ctx, canal : discord.TextChannel, personagem, *item):
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

@bot.command()
async def ficha(ctx, personagem):
    personagem_id = Database.personagem_id(personagem)
    if personagem_id != False:
        personagem_ficha = discord.Embed(
            title=f"""**Ficha de personagem**""",
            description=F"""Atributos, equipamentos e Persona de **{personagem}**""",
            colour=discord.Colour.red()
        )
        foto = Database.foto_personagem(personagem_id)
        personagem_ficha.set_image(url=foto)
        eh_fool = Database.eh_fool(personagem_id)
        if eh_fool == False:
            persona_id = Database.persona_equipada(personagem_id)
            ficha = Database.ficha_personagem(personagem_id, persona_id)
            skills = Database.skills(personagem_id, persona_id)
            equips = Database.itens_equipados(personagem_id)
            nivel = Database.nivel(personagem_id, persona_id)
            if equips[0] != None:
                item = Database.nome_item(equips[0])
                personagem_ficha.add_field(name="Arma corpo-a-corpo", value=item, inline=False)
            if equips[1] != None:
                item = Database.nome_item(equips[1])
                personagem_ficha.add_field(name="Arma à distância", value=item, inline=False)
            if equips[2] != None:
                item = Database.nome_item(equips[2])
                ficha.add_field(name="Armadura", value=item, inline=False)
            if equips[3] != None:
                item = Database.nome_item(equips[3])
                personagem_ficha.add_field(name="Acessório", value=item, inline=False)
            nome = ficha[0][0]
            foto = ficha[0][1]
            arcana = ficha[0][2]
            embed = discord.Embed(
                title=f"""**{nome}**""",
                colour=discord.Colour.red()
            )
            embed.set_image(url=foto)
            embed.add_field(name=f"""**Arcana**""", value=arcana, inline=False)
            embed.add_field(name=f"""**Nível**""", value=nivel, inline=False)
            atributos = [ficha[1][0][1], ficha[1][1][1], ficha[1][2][1], ficha[1][3][1], ficha[1][4][1], ficha[1][5][1], ficha[1][6][1]]
            atributos_soma = Database.atributos_soma(personagem_id)
            atributos_porcent = Database.atributos_porcent(personagem_id)
            plus = []
            for i in range(len(atributos)):
                a = atributos[i] + atributos_soma[i]
                p = (atributos_porcent[i]/100) * a
                if atributos_soma[i] > 0:
                    plus.append(int(a+p))
                else:
                    plus.append(int(p))
            embed.add_field(name=f"""**{ficha[1][0][0]}**""", value=f"""{atributos[0]} +{plus[0]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][1][0]}**""", value=f"""{atributos[1]} +{plus[1]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][2][0]}**""", value=f"""{atributos[2]} +{plus[2]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][3][0]}**""", value=f"""{atributos[3]} +{plus[3]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][4][0]}**""", value=f"""{atributos[4]} +{plus[4]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][5][0]}**""", value=f"""{atributos[5]} +{plus[5]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][6][0]}**""", value=f"""{atributos[6]} +{plus[6]}""", inline=False)
            texto = ""
            for skill in skills:
                texto += skill + "; "
            texto = texto[:-2]
            embed.add_field(name=f"""**Habilidades**""", value=texto, inline=False)
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
            await ctx.send(embed=personagem_ficha)
            await ctx.send(embed=embed)
            await ctx.send(embed=embed2)
        else:
            persona_id = Database.persona_equipada(personagem_id)
            ficha = Database.ficha_personagem(personagem_id, persona_id)
            skills = Database.skills(personagem_id, persona_id)
            equips = Database.itens_equipados(personagem_id)
            nivel = Database.nivel(personagem_id, persona_id)
            nivel_personagem = Database.nivel_fool(personagem_id)
            atributos = Database.atributos_fool_personagem(personagem_id)
            personagem_ficha.add_field(name="Nível do personagem", value=nivel_personagem, inline=False)
            personagem_ficha.add_field(name="Vida (Hp)", value=atributos[0], inline=False)
            personagem_ficha.add_field(name="Energia Espiritual (Sp)", value=atributos[1], inline=False)
            personagem_ficha.add_field(name="Arcana", value="Fool", inline=False)
            if equips[0] != None:
                item = Database.nome_item(equips[0])
                personagem_ficha.add_field(name="Arma corpo-a-corpo", value=item, inline=False)
            if equips[1] != None:
                item = Database.nome_item(equips[1])
                personagem_ficha.add_field(name="Arma à distância", value=item, inline=False)
            if equips[2] != None:
                item = Database.nome_item(equips[2])
                ficha.add_field(name="Armadura", value=item, inline=False)
            if equips[3] != None:
                item = Database.nome_item(equips[3])
                personagem_ficha.add_field(name="Acessório", value=item, inline=False)
            nome = ficha[0][0]
            foto = ficha[0][1]
            arcana = ficha[0][2]
            embed = discord.Embed(
                title=f"""**{nome}**""",
                colour=discord.Colour.red()
            )
            embed.set_image(url=foto)
            embed.add_field(name=f"""**Nível**""", value=nivel, inline=False)
            atributos = [ficha[1][0][1], ficha[1][1][1], ficha[1][2][1], ficha[1][3][1], ficha[1][4][1], ficha[1][5][1], ficha[1][6][1]]
            atributos_soma = Database.atributos_soma(personagem_id)
            atributos_porcent = Database.atributos_porcent(personagem_id)
            plus = []
            for i in range(2,len(atributos)):
                a = atributos[i] + atributos_soma[i]
                p = (atributos_porcent[i]/100) * a
                if atributos_soma[i] > 0:
                    plus.append(int(a+p))
                else:
                    plus.append(int(p))
            embed.add_field(name=f"""**{ficha[1][2][0]}**""", value=f"""{atributos[2]} +{plus[0]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][3][0]}**""", value=f"""{atributos[3]} +{plus[1]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][4][0]}**""", value=f"""{atributos[4]} +{plus[2]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][5][0]}**""", value=f"""{atributos[5]} +{plus[3]}""", inline=False)
            embed.add_field(name=f"""**{ficha[1][6][0]}**""", value=f"""{atributos[6]} +{plus[4]}""", inline=False)
            texto = ""
            for skill in skills:
                texto += skill + "; "
            texto = texto[:-2]
            embed.add_field(name=f"""**Habilidades**""", value=texto, inline=False)
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
            await ctx.send(embed=personagem_ficha)
            await ctx.send(embed=embed)
            await ctx.send(embed=embed2)
            lista_personas = Database.lista_personas(personagem_id)
            texto = ""
            for persona in lista_personas:
                texto += persona + "; "
            texto = texto[:-2]
            personas = discord.Embed(
                title=f"""Lista de personas de **{personagem}**""",
                colour=discord.Colour.red()
            )
            personas.add_field(name="Personas", value=texto, inline=False)
            await ctx.send(embed=personas)
    else:
        await ctx.send("Personagem não encontrado.")
    
@bot.command()
async def subir_nivel(ctx, canal : discord.TextChannel, personagem):
    personagem_id = Database.personagem_id(personagem)
    eh_fool = Database.eh_fool(personagem_id)
    if eh_fool != True:
        persona_id = Database.persona_equipada(personagem_id)
        subiu_nivel = Database.aumentar_nivel(personagem_id)
        personagem_persona_id = Database.personagem_persona_id(personagem_id, persona_id)
        nivel = Database.nivel(personagem_id, persona_id)
        atributos = Database.atributos_iniciais(persona_id)
        fixos = atributos[:2]
        flex = atributos[2:]
        crescimento_atributo = [0, 0, 0, 0, 0, 0, 0]
        for atributo_id, quant_inicial in fixos:
            if atributo_id == 1:
                hp = random.randint(1,6)
                crescimento_atributo[0] = hp
            elif atributo_id == 2:
                sp = random.randint(1,4)
                crescimento_atributo[1] = sp
        flex.sort(key=takeSecond, reverse=True)
        pontos = 3
        while pontos > 0:
            for atributo_id, quant_inicial in flex:
                valor_criterio = 0
                if quant_inicial == 3:
                    valor_criterio = 90
                elif quant_inicial == 2:
                    valor_criterio = 60
                elif quant_inicial == 1:
                    valor_criterio = 30
                dado = random.randint(1,100)
                if dado < valor_criterio and pontos > 0 and crescimento_atributo[atributo_id - 1] == 0:
                    crescimento_atributo[atributo_id - 1] = 1
                    pontos -= 1
                elif crescimento_atributo[atributo_id - 1] < 1:
                    crescimento_atributo[atributo_id - 1] = 0
        Database.aumentar_status(personagem_persona_id, nivel, crescimento_atributo)
        atributos_aumento = discord.Embed(
            title=f"""**SUBIU DE NÍVEL!**""",
            description=f"""**{personagem}** alcançou o nível ({nivel})""",
            colour=discord.Colour.green()
        )
        atributos_aumento.add_field(name="**HP**", value=f"""+{crescimento_atributo[0]}""")
        atributos_aumento.add_field(name="**SP**", value=f"""+{crescimento_atributo[1]}""")
        atributos_aumento.add_field(name="**St**", value=f"""+{crescimento_atributo[2]}""")
        atributos_aumento.add_field(name="**Ma**", value=f"""+{crescimento_atributo[3]}""")
        atributos_aumento.add_field(name="**En**", value=f"""+{crescimento_atributo[4]}""")
        atributos_aumento.add_field(name="**Ag**", value=f"""+{crescimento_atributo[5]}""")
        atributos_aumento.add_field(name="**Lu**", value=f"""+{crescimento_atributo[6]}""")
        await canal.send(embed=atributos_aumento)
        nivel_skills = Database.nivel_skills(nivel, persona_id)
        if nivel_skills != False:
            skills = Database.skills(personagem_id, persona_id)
            skills_id = []
            for skill in skills:
                skills_id.append(Database.skill_id(skill))
            if len(skills) + len(nivel_skills) < 8:
                for skill in nivel_skills:
                    if skill not in skills_id:
                        aprendeu = Database.add_skill(skill, personagem_persona_id)
                        if aprendeu == True:
                            nome_skill = Database.nome_skill(skill)
                            await canal.send(f"""**{personagem}** aprendeu a habilidade **{nome_skill}**""")
            elif len(skills_id) + len(nivel_skills) > 8 and len(skills) < 8:
                tam = len(skills_id)
                while tam < 8:
                    if nivel_skills[i] not in skills_id:
                        aprendeu = Database.add_skill(nivel_skills[0], personagem_persona_id)
                        if aprendeu == True:
                            nome_skill = Database.nome_skill(nivel_skills[0])
                            await canal.send(f"""**{personagem}** aprendeu a habilidade **{nome_skill}**""")
                            del nivel_skills[i]
                            tam += 1
                if nivel_skills != []:
                    nova_skills = Database.skills(personagem_id, persona_id)
                    skills_id = []
                    for skill in nova_skills:
                        skills_id.append(Database.skill_id(skill))
                    for skill in nivel_skills:
                        nome_skill = Database.nome_skill(skill)
                        embed = discord.Embed(
                            title=f"""**{personagem}** aprendeu uma nova habilidade!""",
                            description=f"""Você já conhece habilidades demais, deseja trocar alguma por **{nome_skill}**?""",
                            colour=discord.Colour.red()
                        )
                        emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
                        emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
                        for i in range(len(nova_skills)):
                            embed.add_field(name=emojis_disc[i], value=Database.nome_skill(skills_id[i]), inline=True)
                        embed_msg = await canal.send(embed=embed)
                        for j in range(len(nova_skills)):
                            await embed_msg.add_reaction(emoji=emojis_raw[j])
                        await embed_msg.add_reaction(emoji="❌")
                        ok = 0
                        while ok == 0:
                            reaction, user = await bot.wait_for('reaction_add', timeout=None)
                            if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                                ok = 1
                            if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                                ok = 2
                            if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                                ok = 3
                            if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                                ok = 4
                            if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                                ok = 5
                            if str(reaction.emoji) == emojis_raw[5] and str(user) != "Persona Bot#0708":
                                ok = 6
                            if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                                ok = 7
                            if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                                ok = 8
                            if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                                ok = 9
                        await embed_msg.delete()
                        if ok < 9:
                            mudou = Database.mod_skill(skills_id[ok-1], skill, personagem_persona_id)
                            if mudou:
                                confirmacao = discord.Embed(
                                    title=f"""Nova habilidade aprendida: **{nome_skill}**""",
                                    description=f"""**{personagem}** esqueceu de **{nova_skills[ok-1]}**""",
                                    colour=discord.Colour.blue()
                                )
                                await canal.send(embed=confirmacao)
                            else:
                                await ctx.send("Erro no aprendizado da habilidade")
                        else:
                            await canal.send(f"""**{personagem}** ignorou a habilidade **{nome_skill}**""")
                        nova_skills = Database.skills(personagem_id, persona_id)
            else:
                nova_skills = Database.skills(personagem_id, persona_id)
                skills_id = []
                for skill in skills:
                    skills_id.append(Database.skill_id(skill))
                for skill in nivel_skills:
                    nome_skill = Database.nome_skill(skill)
                    embed = discord.Embed(
                        title=f"""**{personagem}** aprendeu uma nova habilidade!""",
                        description=f"""Você já conhece habilidades demais, deseja trocar alguma por **{nome_skill}**?""",
                        colour=discord.Colour.red()
                    )
                    emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
                    emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
                    for i in range(len(nova_skills)):
                        embed.add_field(name=emojis_disc[i], value=nova_skills[i], inline=True)
                    embed_msg = await canal.send(embed=embed)
                    for j in range(len(nova_skills)):
                        await embed_msg.add_reaction(emoji=emojis_raw[j])
                    await embed_msg.add_reaction(emoji="❌")
                    ok = 0
                    while ok == 0:
                        reaction, user = await bot.wait_for('reaction_add', timeout=None)
                        if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                            ok = 1
                        if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                            ok = 2
                        if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                            ok = 3
                        if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                            ok = 4
                        if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                            ok = 5
                        if str(reaction.emoji) == emojis_raw[5] and str(user) != "Persona Bot#0708":
                            ok = 6
                        if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                            ok = 7
                        if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                            ok = 8
                        if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                            ok = 9
                    await embed_msg.delete()
                    if ok < 9:
                        mudou = Database.mod_skill(skills_id[ok-1], skill, personagem_persona_id)
                        if mudou:
                            confirmacao = discord.Embed(
                                title=f"""Nova habilidade aprendida: **{nome_skill}**""",
                                description=f"""**{personagem}** esqueceu de **{nova_skills[ok-1]}**""",
                                colour=discord.Colour.blue()
                            )
                            await canal.send(embed=confirmacao)
                        else:
                            await ctx.send("Erro no aprendizado da habilidade")
                    else:
                        await canal.send(f"""**{personagem}** ignorou a habilidade **{nome_skill}**""")
                    nova_skills = Database.skills(personagem_id, persona_id)
    else:
        subiu_nivel = Database.aumentar_nivel_fool(personagem_id)
        nivel = Database.nivel_fool(personagem_id)
        atributos = Database.atributos_iniciais_fool(personagem_id)
        crescimento_atributo = [0, 0]
        hp = random.randint(1,6)
        crescimento_atributo[0] = random.randint(1,6)
        crescimento_atributo[1] = random.randint(1,4)
        Database.aumentar_status_fool(personagem_id, nivel, crescimento_atributo)
        atributos_aumento = discord.Embed(
            title=f"""**SUBIU DE NÍVEL!**""",
            description=f"""**{personagem}** alcançou o nível ({nivel})""",
            colour=discord.Colour.green()
        )
        atributos_aumento.add_field(name="**HP**", value=f"""+{crescimento_atributo[0]}""")
        atributos_aumento.add_field(name="**SP**", value=f"""+{crescimento_atributo[1]}""")
        await canal.send(embed=atributos_aumento)

@bot.command()
async def diminuir_nivel(ctx,  canal : discord.TextChannel, personagem):
    personagem_id = Database.personagem_id(personagem)
    eh_fool = Database.eh_fool(personagem_id)
    if eh_fool == False:
        persona_id = Database.persona_equipada(personagem_id)
        nivel = Database.nivel(personagem_id, persona_id)
        diminuiu_nivel = Database.diminuir_nivel(personagem_id)
        if diminuiu_nivel:
            await canal.send(f"""Nível de **{personagem}** diminuído para {nivel -1}""")
        personagem_persona_id = Database.personagem_persona_id(personagem_id, persona_id)
        apagar = Database.apagar_crecimento(personagem_persona_id, nivel)
        if apagar:
            await canal.send(f"""Atributos de **{personagem}** resetado para os do {nivel -1}""")
        nivel_skills = Database.nivel_skills(nivel, persona_id)
        for skill in nivel_skills:
            desaprendeu = Database.del_skill(skill, personagem_persona_id)
            if desaprendeu:
                await canal.send(f"""Habilidade: **{Database.nome_skill(skill)}** foi desaprendida.""")
    else:
        nivel = Database.nivel_fool(personagem_id)
        diminuiu_nivel = Database.diminuir_nivel_fool(personagem_id)
        if diminuiu_nivel:
            await canal.send(f"""Nível de **{personagem}** diminuído para {nivel -1}""")
        apagar = Database.apagar_crecimento_fool(personagem_id, nivel)
        if apagar:
            await canal.send(f"""Atributos de **{personagem}** resetado para os do {nivel -1}""")

@bot.command()
async def subir_nivel_persona(ctx, canal : discord.TextChannel, personagem):
    personagem_id = Database.personagem_id(personagem)
    eh_fool = Database.eh_fool(personagem_id)
    if eh_fool == True:
        persona_id = Database.persona_equipada(personagem_id)
        subiu_nivel = Database.aumentar_nivel(personagem_id)
        personagem_persona_id = Database.personagem_persona_id(personagem_id, persona_id)
        nivel = Database.nivel(personagem_id, persona_id)
        atributos = Database.atributos_iniciais(persona_id)
        fixos = atributos[:2]
        flex = atributos[2:]
        crescimento_atributo = [0, 0, 0, 0, 0, 0, 0]
        for atributo_id, quant_inicial in fixos:
            if atributo_id == 1:
                hp = random.randint(1,6)
                crescimento_atributo[0] = hp
            elif atributo_id == 2:
                sp = random.randint(1,4)
                crescimento_atributo[1] = sp
        flex.sort(key=takeSecond, reverse=True)
        pontos = 3
        while pontos > 0:
            for atributo_id, quant_inicial in flex:
                valor_criterio = 0
                if quant_inicial == 3:
                    valor_criterio = 90
                elif quant_inicial == 2:
                    valor_criterio = 60
                elif quant_inicial == 1:
                    valor_criterio = 30
                dado = random.randint(1,100)
                if dado < valor_criterio and pontos > 0 and crescimento_atributo[atributo_id - 1] == 0:
                    crescimento_atributo[atributo_id - 1] = 1
                    pontos -= 1
                elif crescimento_atributo[atributo_id - 1] < 1:
                    crescimento_atributo[atributo_id - 1] = 0
        Database.aumentar_status_fool_persona(personagem_persona_id, nivel, crescimento_atributo)
        atributos_aumento = discord.Embed(
            title=f"""**PERSONA SUBIU DE NÍVEL!**""",
            description=f"""**{Database.nome_persona(persona_id)}** alcançou o nível ({nivel})""",
            colour=discord.Colour.green()
        )
        atributos_aumento.add_field(name="**St**", value=f"""+{crescimento_atributo[2]}""")
        atributos_aumento.add_field(name="**Ma**", value=f"""+{crescimento_atributo[3]}""")
        atributos_aumento.add_field(name="**En**", value=f"""+{crescimento_atributo[4]}""")
        atributos_aumento.add_field(name="**Ag**", value=f"""+{crescimento_atributo[5]}""")
        atributos_aumento.add_field(name="**Lu**", value=f"""+{crescimento_atributo[6]}""")
        await canal.send(embed=atributos_aumento)
        nivel_skills = Database.nivel_skills(nivel, persona_id)
        if nivel_skills != False:
            skills = Database.skills(personagem_id, persona_id)
            if len(skills) + len(nivel_skills) < 8:
                for skill in nivel_skills:
                    if skill not in skills:
                        aprendeu = Database.add_skill(skill, personagem_persona_id)
                        if aprendeu == True:
                            nome_skill = Database.nome_skill(skill)
                            await canal.send(f"""**{Database.nome_persona(persona_id)}** aprendeu a habilidade **{nome_skill}**""")
            elif len(skills) + len(nivel_skills) > 8 and len(skills) < 8:
                tam = len(skills)
                while tam < 8:
                    if nivel_skills[i] not in skills:
                        aprendeu = Database.add_skill(nivel_skills[0], personagem_persona_id)
                        if aprendeu == True:
                            nome_skill = Database.nome_skill(nivel_skills[0])
                            await canal.send(f"""**{Database.nome_persona(persona_id)}** aprendeu a habilidade **{nome_skill}**""")
                            del nivel_skills[i]
                            tam += 1
                if nivel_skills != []:
                    nova_skills = Database.skills(personagem_id, persona_id)
                    for skill in nivel_skills:
                        nome_skill = Database.nome_skill(skill)
                        embed = discord.Embed(
                            title=f"""**{Database.nome_persona(persona_id)}** aprendeu uma nova habilidade!""",
                            description=f"""Você já conhece habilidades demais, deseja trocar alguma por **{nome_skill}**?""",
                            colour=discord.Colour.red()
                        )
                        emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
                        emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
                        for i in range(len(nova_skills)):
                            embed.add_field(name=emojis_disc[i], value=Database.nome_skill(nova_skills[i]), inline=True)
                        embed_msg = await canal.send(embed=embed)
                        for j in range(len(nova_skills)):
                            await embed_msg.add_reaction(emoji=emojis_raw[j])
                        await embed_msg.add_reaction(emoji="❌")
                        ok = 0
                        while ok == 0:
                            reaction, user = await bot.wait_for('reaction_add', timeout=None)
                            if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                                ok = 1
                            if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                                ok = 2
                            if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                                ok = 3
                            if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                                ok = 4
                            if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                                ok = 5
                            if str(reaction.emoji) == emojis_raw[5] and str(user) != "Persona Bot#0708":
                                ok = 6
                            if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                                ok = 7
                            if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                                ok = 8
                            if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                                ok = 9
                        await embed_msg.delete()
                        if ok < 9:
                            mudou = Database.mod_skill(nova_skills[ok-1], skill, personagem_persona_id)
                            if mudou:
                                confirmacao = discord.Embed(
                                    title=f"""Nova habilidade aprendida: **{nome_skill}**""",
                                    description=f"""**{Database.nome_persona(persona_id)}** esqueceu de **{Database.nome_skill(nova_skills[ok-1])}**""",
                                    colour=discord.Colour.blue()
                                )
                                await canal.send(embed=confirmacao)
                            else:
                                await ctx.send("Erro no aprendizado da habilidade")
                        else:
                            await canal.send(f"""**{Database.nome_persona(persona_id)}** ignorou a habilidade **{nome_skill}**""")
                        nova_skills = Database.skills(personagem_id, persona_id)
            else:
                for skill in nivel_skills:
                    nome_skill = Database.nome_skill(skill)
                    embed = discord.Embed(
                        title=f"""**{Database.nome_persona(persona_id)}** aprendeu uma nova habilidade!""",
                        description=f"""Você já conhece habilidades demais, deseja trocar alguma por **{nome_skill}**?""",
                        colour=discord.Colour.red()
                    )
                    emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
                    emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
                    for i in range(len(nova_skills)):
                        embed.add_field(name=emojis_disc[i], value=Database.nome_skill(nova_skills[i]), inline=True)
                    embed_msg = await canal.send(embed=embed)
                    for j in range(len(nova_skills)):
                        await embed_msg.add_reaction(emoji=emojis_raw[j])
                    await embed_msg.add_reaction(emoji="❌")
                    ok = 0
                    while ok == 0:
                        reaction, user = await bot.wait_for('reaction_add', timeout=None)
                        if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                            ok = 1
                        if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                            ok = 2
                        if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                            ok = 3
                        if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                            ok = 4
                        if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                            ok = 5
                        if str(reaction.emoji) == emojis_raw[5] and str(user) != "Persona Bot#0708":
                            ok = 6
                        if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                            ok = 7
                        if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                            ok = 8
                        if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                            ok = 9
                    await embed_msg.delete()
                    if ok < 9:
                        mudou = Database.mod_skill(nova_skills[ok-1], skill, personagem_persona_id)
                        if mudou:
                            confirmacao = discord.Embed(
                                title=f"""Nova habilidade aprendida: **{nome_skill}**""",
                                description=f"""**{Database.nome_persona(persona_id)}** esqueceu de **{Database.nome_skill(nova_skills[ok-1])}**""",
                                colour=discord.Colour.blue()
                            )
                            await canal.send(embed=confirmacao)
                        else:
                            await ctx.send("Erro no aprendizado da habilidade")
                    else:
                        await canal.send(f"""**{Database.nome_persona(persona_id)}** ignorou a habilidade **{nome_skill}**""")
                    nova_skills = Database.skills(personagem_id, persona_id)
    else:
        await ctx.send("Este personagem não é da Arcana Fool")
    
@bot.command()
async def diminuir_nivel_persona(ctx, canal : discord.TextChannel, personagem):
    personagem_id = Database.personagem_id(personagem)
    eh_fool = Database.eh_fool(personagem_id)
    if eh_fool == True:
        persona_id = Database.persona_equipada(personagem_id)
        nivel = Database.nivel(personagem_id, persona_id)
        diminuiu_nivel = Database.diminuir_nivel(personagem_id)
        if diminuiu_nivel:
            await canal.send(f"""Nível de **{Database.nome_persona(persona_id)}** diminuído para {nivel -1}""")
        personagem_persona_id = Database.personagem_persona_id(personagem_id, persona_id)
        apagar = Database.apagar_crecimento(personagem_persona_id, nivel)
        if apagar:
            await canal.send(f"""Atributos de **{Database.nome_persona(persona_id)}** resetado para os do {nivel -1}""")
        nivel_skills = Database.nivel_skills(nivel-1, persona_id)
        for skill in nivel_skills:
            desaprendeu = Database.del_skill(skill, personagem_persona_id)
            if desaprendeu:
                await canal.send(f"""Habilidade: **{Database.nome_skill(skill)}** foi desaprendida.""")
        else:
            await ctx.send(f"""Este personagem não é da Arcana Fool""")

@bot.command()
async def equipar_persona(ctx, canal : discord.TextChannel, personagem):
    personagem_id = Database.personagem_id(personagem)
    eh_fool = Database.eh_fool(personagem_id)
    if personagem_id != False:
        if eh_fool == True:
            personas = Database.lista_personas(personagem_id)
            persona_id = Database.persona_equipada(personagem_id)
            persona_nome = Database.nome_persona(persona_id)
            personas.remove(persona_nome)
            if personas != []:
                embed = discord.Embed(
                title=f"""**Troca de Persona**""",
                description=f"""Reaja com a opção da Persona que deseja equipar""",
                colour=discord.Colour.red()
                )
                emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
                emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
                for i in range(len(personas)):
                    embed.add_field(name=emojis_disc[i], value=personas[i], inline=True)
                embed_msg = await canal.send(embed=embed)
                for j in range(len(personas)):
                    await embed_msg.add_reaction(emoji=emojis_raw[j])
                await embed_msg.add_reaction(emoji="❌")
                ok = 0
                while ok == 0:
                    reaction, user = await bot.wait_for('reaction_add', timeout=None)
                    if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                        persona_l_id = personas[0]
                        ok = 1
                    if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                        persona_l_id = personas[1]
                        ok = 2
                    if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                        persona_l_id = personas[2]
                        ok = 3
                    if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                        persona_l_id = personas[3]
                        ok = 4
                    if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                        persona_l_id = personas[4]
                        ok = 5
                    if str(reaction.emoji) == emojis_raw[5] and str(user) != "Persona Bot#0708":
                        persona_l_id = personas[5]
                        ok = 6
                    if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                        persona_l_id = personas[6]
                        ok = 7
                    if str(reaction.emoji) == emojis_raw[7] and str(user) != "Persona Bot#0708":
                        persona_l_id = personas[7]
                        ok = 8
                    if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                        ok = 9
                await embed_msg.delete()
                if ok < 9:
                    p_id = Database.persona_id(personas[ok-1])
                    equipou_persona = Database.equipar_persona(personagem_id, p_id)
                    if equipou_persona:
                        confirmacao = discord.Embed(
                            title="Persona equipada atualizada",
                            description=f"""**A Persona equipada de {personagem} agora é {personas[ok-1]}**""",
                            colour=discord.Colour.blue()
                        )
                        await canal.send(embed=confirmacao)
                    else:
                        await ctx.send("Erro na troca de Persona.")
                else:
                    await canal.send("Troca de Persona cancelada.")
            else:
                await ctx.send(f"""Você só tem uma persona, não tem o que equipar xD""")
        else:
            await ctx.send(f"""Este personagem não possui Arcana Fool""")
    else:
        await ctx.send(f"""Este personagem não existe.""")

@bot.command()
async def tomar_persona(ctx , canal : discord.TextChannel, personagem, *persona):
    personagem_id = Database.personagem_id(personagem)
    eh_fool = Database.eh_fool(personagem_id)
    nome = ""
    for palavra in persona:
        nome+=palavra + " "
    nome = nome[:-1]
    persona_id = Database.persona_id(nome)
    if personagem_id != False:
        if persona_id != False:
            if eh_fool == True:
                persona_habilitada = Database.personagem_persona_id(personagem_id, persona_id)
                print(persona_habilitada)
                if persona_habilitada == False:
                    nova_persona = Database.personagem_add_persona(personagem_id, persona_id)
                    if nova_persona:
                        await canal.send(f"""{nome} agora é bem vindo(a) ao coração de {personagem}""")
                    else:
                        await ctx.send(f"""Erro interno""")
                else:
                    compendium = Database.compendium(persona_habilitada)
                    print(compendium)
                    if compendium == True:
                        reativar_persona = Database.personagem_reativar_persona(personagem_id, persona_id)
                        if reativar_persona:
                            await canal.send(f"""{nome} agora é bem vindo(a) ao coração de {personagem} novamente""")
                    else:
                        await ctx.send(f"""Você já possui essa Persona""")
            else:
                await ctx.send(f"""Este personagem não possui Arcana Fool""")
        else:
            await ctx.send(f"""Esta Persona não existe""")
    else:
        await ctx.send(f"""Este personagem não existe.""")

@bot.command()
async def soltar_persona(ctx, canal : discord.TextChannel, personagem, *persona):
    personagem_id = Database.personagem_id(personagem)
    eh_fool = Database.eh_fool(personagem_id)
    nome = ""
    for palavra in persona:
        nome+=palavra + " "
    nome = nome[:-1]
    persona_id = Database.persona_id(nome)
    if personagem_id != False:
        if persona_id != False:
            if eh_fool == True:
                persona_habilitada = Database.personagem_persona_id(personagem_id, persona_id)
                compendium = Database.compendium(persona_habilitada)
                if persona_habilitada != False and compendium != True:
                    persona_solta = Database.personagem_del_persona(personagem_id, persona_id)
                    if persona_solta:
                        await canal.send(f"""{nome} agora é não é mais bem vindo(a) ao coração de {personagem}""")
                    else:
                        await ctx.send(f"""Erro interno""")
                else:
                    await ctx.send(f"""Você não possui essa Persona""")
            else:
                await ctx.send(f"""Este personagem não possui Arcana Fool""")
        else:
            await ctx.send(f"""Esta Persona não existe""")
    else:
        await ctx.send(f"""Este personagem não existe.""")
    
@bot.command()
async def skills_conhecidas(ctx,  canal : discord.TextChannel, personagem):
    personagem_id = Database.personagem_id(personagem)
    persona_id = Database.persona_equipada(personagem_id)
    nome = Database.nome_persona(persona_id)
    nivel = Database.nivel(personagem_id, persona_id)
    skills = Database.skills_conhecidas(nivel, persona_id)
    texto = ""
    for skill in skills:
        texto += Database.nome_skill(skill) + "\n"
    texto = texto[:-1]
    embed = discord.Embed(
        title=f"""Habilidades conhecidas de **{nome}**""",
        description=texto,
        colour=discord.Colour.blue()
    )
    await canal.send(embed=embed)

@bot.command()
async def aprender_skill(ctx, canal : discord.TextChannel, personagem, *skill):
    nome = ""
    for palavra in skill:
        nome += palavra + " "
    nome = nome[:-1]
    personagem_id = Database.personagem_id(personagem)
    persona_id = Database.persona_equipada(personagem_id)
    nome = Database.nome_persona(persona_id)
    personagem_persona_id = Database.personagem_persona_id(personagem_id, persona_id)
    skills = Database.skills(personagem_id, persona_id)
    skill_id = Database.skill_id(skill)
    skills_id = []
    for skill in skills:
        skills_id.append(Database.skill_id(skill))
    if skill_id != False:
        nome_skill = Database.nome_skill(skill_id)
        if skill_id not in skills:
            if len(skills) < 8:
                aprendeu = Database.add_skill(skill_id, personagem_persona_id)
                if aprendeu == True:
                    await canal.send(f"""**{personagem}** aprendeu a habilidade **{nome_skill}**""")
            else:
                embed = discord.Embed(
                    title=f"""**{personagem}** aprendeu uma nova habilidade!""",
                    description=f"""Você já conhece habilidades demais, deseja trocar alguma por **{nome_skill}**?""",
                    colour=discord.Colour.red()
                )
                emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
                emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
                for i in range(len(skills)):
                    embed.add_field(name=emojis_disc[i], value=Database.nome_skill(skills[i]), inline=True)
                embed_msg = await canal.send(embed=embed)
                for j in range(len(skills)):
                    await embed_msg.add_reaction(emoji=emojis_raw[j])
                await embed_msg.add_reaction(emoji="❌")
                ok = 0
                while ok == 0:
                    reaction, user = await bot.wait_for('reaction_add', timeout=None)
                    if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                        ok = 1
                    if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                        ok = 2
                    if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                        ok = 3
                    if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                        ok = 4
                    if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                        ok = 5
                    if str(reaction.emoji) == emojis_raw[5] and str(user) != "Persona Bot#0708":
                        ok = 6
                    if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                        ok = 7
                    if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
                        ok = 8
                    if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                        ok = 9
                await embed_msg.delete()
                if ok < 9:
                    mudou = Database.mod_skill(skills_id[ok-1], skill_id, personagem_persona_id)
                    if mudou:
                        confirmacao = discord.Embed(
                            title=f"""Nova habilidade aprendida: **{nome_skill}**""",
                            description=f"""**{personagem}** esqueceu de **{skills[ok-1]}**""",
                            colour=discord.Colour.blue()
                        )
                        await canal.send(embed=confirmacao)
                    else:
                        await ctx.send("Erro no aprendizado da habilidade")
                else:
                    await canal.send(f"""**{personagem}** ignorou a habilidade **{nome_skill}**""")
        else:
            await ctx.send(f"""**{personagem}** já conhece essa habildade.""")
    else:
        await ctx.send(f"""Esta habilidade não existe.""")

@bot.command()
async def esquecer_skill(ctx,  canal : discord.TextChannel, personagem):
    personagem_id = Database.personagem_id(personagem)
    persona_id = Database.persona_equipada(personagem_id)
    nome = Database.nome_persona(persona_id)
    personagem_persona_id = Database.personagem_persona_id(personagem_id, persona_id)
    skills = Database.skills(personagem_id, persona_id)
    skills_id = []
    for skill in skills:
        skills_id.append(Database.skill_id(skill))
    embed = discord.Embed(
        title=f"""**{personagem}** deseja esquecer uma habilidade!""",
        description=f"""Reaja com a opção da habilidade que deseja esquecer.""",
        colour=discord.Colour.red()
    )
    emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
    emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
    for i in range(len(skills)):
        embed.add_field(name=emojis_disc[i], value=skills[i], inline=True)
    embed_msg = await canal.send(embed=embed)
    for j in range(len(skills)):
        await embed_msg.add_reaction(emoji=emojis_raw[j])
    await embed_msg.add_reaction(emoji="❌")
    ok = 0
    while ok == 0:
        reaction, user = await bot.wait_for('reaction_add', timeout=None)
        if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
            ok = 1
        if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
            ok = 2
        if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
            ok = 3
        if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
            ok = 4
        if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
            ok = 5
        if str(reaction.emoji) == emojis_raw[5] and str(user) != "Persona Bot#0708":
            ok = 6
        if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
            ok = 7
        if str(reaction.emoji) == emojis_raw[6] and str(user) != "Persona Bot#0708":
            ok = 8
        if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
            ok = 9
    await embed_msg.delete()
    if ok < 9:
        deletou = Database.del_skill(skills_id[ok-1], personagem_persona_id)
        print(deletou)
        if deletou:
            confirmacao = discord.Embed(
                title=f"""Habilidade esquecida: **{nome_skill}**""",
                description=f"""**{personagem}** esqueceu de **{skills[ok-1]}**""",
                colour=discord.Colour.blue()
            )
            await canal.send(embed=confirmacao)
        else:
            await ctx.send("Erro no esquecimento da habilidade")
    else:
        await canal.send(f"""**Esquecimento cancelado**""")

@bot.command()
async def adicionar_horda(ctx, tipo, *personagem):
    nome = ""
    for palavra in personagem:
        nome += palavra + " "
    nome = nome[:-1]
    if tipo == "shadow"  or tipo == "s":
        shadow_id = Database.shadow_id(nome)
        if shadow_id != False:
            horda.append(("s",nome))
            horda_mult_atk.append(0)
            horda_mult_def.append(0)
            horda_mult_acc.append(0)
            horda_mult_evs.append(0)
            horda_mult_crit.append(0)
            horda_elem_dano.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            await ctx.send(f"""**{nome}** foi adicionado à horda.""")
        else:
            await ctx.send("Shadow não existente.")
    elif tipo == "personagem" or tipo == "p":
        personagem_id = Database.personagem_id(nome)
        if personagem_id != False:
            horda.append(("p",nome))
            horda_mult_atk.append(0)
            horda_mult_def.append(0)
            horda_mult_acc.append(0)
            horda_mult_evs.append(0)
            horda_mult_crit.append(0)
            horda_elem_dano.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            await ctx.send(f"""**{nome}** foi adicionado à horda.""")
        else:
            await ctx.send("Personagem não existente.")
    else:
        await ctx.send("Tipo incorreto.")

@bot.command()
async def adicionar_party(ctx, personagem):
    personagem_id = Database.personagem_id(personagem)
    if personagem_id != False:
        party.append(personagem)
        party_mult_atk.append(0)
        party_mult_def.append(0)
        party_mult_acc.append(0)
        party_mult_evs.append(0)
        party_mult_crit.append(0)
        party_elem_dano.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        await ctx.send(f"""**{personagem}** foi adicionado à Party.""")
    else:
        await ctx.send("Personagem não existente.")

@bot.command()
async def remover_party(ctx, personagem):
    if party != []:
        achou = 0
        i = 0
        while i < len(party) and achou == 0:
            if party[i] == personagem:
                del party[i]
                del party_mult_atk[i]
                del party_mult_def[i]
                del party_mult_acc[i]
                del party_mult_evs[i]
                del party_elem_dano[i]
                del party_mult_crit[i]
                await ctx.send(f"""**{personagem}** foi removido da Party.""")
                achou = 1
        if achou == 0:
            await ctx.send("Nome não encontrado.")
    else:
        await ctx.send("Nome não encontrado.")

@bot.command()
async def remover_horda(ctx, *personagem):
    nome = ""
    for palavra in personagem:
        nome += palavra + " "
    nome = nome[:-1]
    if horda != []:
        achou = 0
        i = 0
        while i < len(horda) and achou == 0:
            if horda[i][1] == nome:
                del horda[i]
                del horda_mult_atk[i]
                del horda_mult_def[i]
                del horda_mult_acc[i]
                del horda_mult_evs[i]
                del horda_elem_dano[i]
                del horda_mult_crit[i]
                await ctx.send(f"""**{nome}** foi removido da horda.""")
                achou = 1
        if achou == 0:
            await ctx.send("Nome não encontrado.")
    else:
        await ctx.send("Nome não encontrado.")

@bot.command()
async def mostrar_party(ctx):
    if party != []:
        embed = discord.Embed(
            title=f"""**PARTY**""",
            colour=discord.Colour.blue()
        )
        texto = ""
        i = 1
        for elem in party:
            texto += f"""{i}.**{elem}**\n"""
            i +=1
        texto = texto[:-1]
        embed.add_field(name="Lista dos membros da Party", value=texto, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("A party está vazia")
    
@bot.command()
async def mostrar_horda(ctx):
    if horda != []:
        embed = discord.Embed(
            title=f"""**HORDA**""",
            colour=discord.Colour.blue()
        )
        texto = ""
        i = 1
        for tipo, elem in horda:
            nome = ""
            if tipo == "s":
                nome = "Shadow"
            else:
                nome = "Personagem"
            texto += f"""{i}.**{elem}** ({nome})\n"""
            i += 1
        texto = texto[:-1]
        embed.add_field(name="Lista dos elementos da horda", value=texto, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("A horda está vazia")

@bot.command()
async def calcular_turnos(ctx, canal : discord.TextChannel):
    ordem = []
    if horda != [] and party != []:
        embed = discord.Embed(
            title=f"""Qual a forma de interação pós combate?""",
            description=f"""Reaja com a opção desejada""",
            colour=discord.Colour.blue()
        )
        embed.add_field(name=":one:", value="Emboscada", inline=False)
        embed.add_field(name=":two:", value="Disputa", inline=False)
        embed_msg = await ctx.send(embed=embed)
        emojis_raw = ["1️⃣", "2️⃣"]
        for i in range(2):
            await embed_msg.add_reaction(emoji=emojis_raw[i])
        await embed_msg.add_reaction(emoji="❌")
        ok = 0
        while ok == 0:
            reaction, user = await bot.wait_for('reaction_add', timeout=None)
            if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                ok = 1
            if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                ok = 2
            if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                ok = 3
        await embed_msg.delete()
        if ok == 1:
            next = 0
            while next == 0:
                await ctx.send("**EMBOSCADA**: Qual o valor critério? (0 a 100)")
                msg = await bot.wait_for('message')
                mensagem = msg.content
                try:
                    valor_criterio = int(mensagem)
                    if valor_criterio > 0 and valor_criterio <= 100:
                        next = 1
                except:
                    await ctx.send("Digite um número entre 0 e 100.")
            lider_id = Database.personagem_id(party[0])
            usuario = Database.discord_user(lider_id)
            dado = await Dado.rolagem_pronta(bot, canal, party[0], usuario, 1, 100)
            if dado <= valor_criterio:
                ordem1 = []
                ordem2 = []
                quant1 = []
                quant2 = []
                await canal.send(f"""O grupo tirou um dado de {dado} e conseguiu emboscar a Shadow, vocês atacarão primeiro.""")
                for personagem in party:
                    personagem_id = Database.personagem_id(personagem)
                    persona_id = Database.persona_equipada(personagem_id)
                    atributos = Database.atributos(personagem_id, persona_id)
                    agilidade = atributos[5]
                    ordem1.append(personagem)
                    quant1.append(agilidade)
                insertion_sort(quant1, ordem1)
                for tipo, char in horda:
                    if tipo == "s":
                        shadow_id = Database.shadow_id(char)
                        atributos = Database.atributos_iniciais(shadow_id)
                        agilidade = 0
                        for atributo_id, valor in atributos:
                            if atributo_id == 6:
                                agilidade = valor
                                ordem2.append(char)
                                quant2.append(agilidade)
                    else:
                        personagem_id = Database.personagem_id(char)
                        persona_id = Database.persona_equipada(personagem_id)
                        atributos = Database.atributos(personagem_id, persona_id)
                        agilidade = atributos[5]
                        ordem2.append(personagem_id)
                        quant2.append(agilidade)
                insertion_sort(quant2, ordem2)
                ordem = ordem1 + ordem2
            else:
                ordem1 = []
                quant1 = []
                await canal.send(f"""O grupo tirou um dado de {dado} e falhou em emboscar a shadow, vocês atacarão de acordo com a sua agilidade.""")
                for personagem in party:
                    personagem_id = Database.personagem_id(personagem)
                    persona_id = Database.persona_equipada(personagem_id)
                    atributos = Database.atributos(personagem_id, persona_id)
                    agilidade = atributos[5]
                    ordem1.append(personagem)
                    quant1.append(agilidade)
                for tipo, char in horda:
                    if tipo == "s":
                        shadow_id = Database.shadow_id(char)
                        atributos = Database.atributos_iniciais(shadow_id)
                        agilidade = 0
                        for atributo_id, valor in atributos:
                            if atributo_id == 6:
                                agilidade = valor
                                ordem2.append(char)
                                quant2.append(agilidade)
                    else:
                        personagem_id = Database.personagem_id(char)
                        persona_id = Database.persona_equipada(personagem_id)
                        atributos = Database.atributos(personagem_id, persona_id)
                        agilidade = atributos[5]
                        ordem1.append(personagem_id)
                        quant1.append(agilidade)
                insertion_sort(quant1, ordem1)
                ordem = ordem1
            embed = discord.Embed(
                title=f"""**Ordem de turnos*""",
                colour=discord.Colour.blue()
            )
            texto = ""
            i = 1
            for elem in ordem:
                texto += f"""{i}. {elem}\n"""
                i += 1
            texto[:-1]
            embed.add_field(name="ORDEM:", value=texto, inline=False)
            await canal.send(embed=embed)
        elif ok == 2:
            next = 0
            while next == 0:
                await ctx.send("**DISPUTA**: Qual o valor critério? (0 a 100)")
                msg = await bot.wait_for('message')
                mensagem = msg.content
                try:
                    valor_criterio = int(mensagem)
                    if valor_criterio > 0 and valor_criterio <= 100:
                        next = 1
                except:
                    await ctx.send("Digite um número entre 0 e 100.")
            lider_id = Database.personagem_id(party[0])
            usuario = Database.discord_user(lider_id)
            dado = await Dado.rolagem_pronta(bot, canal, party[0], usuario, 1, 100)
            if dado <= valor_criterio:
                ordem1 = []
                quant1 = []
                await canal.send(f"""O grupo tirou um dado de {dado} e conseguiu evitar ser emboscado, vocês atacarão de acordo co ma sua agilidade.""")
                for personagem in party:
                    personagem_id = Database.personagem_id(personagem)
                    persona_id = Database.persona_equipada(personagem_id)
                    atributos = Database.atributos(personagem_id, persona_id)
                    agilidade = atributos[5]
                    ordem1.append(personagem)
                    quant1.append(agilidade)
                insertion_sort(quant1, ordem1)
                for tipo, char in horda:
                    if tipo == "s":
                        shadow_id = Database.shadow_id(char)
                        atributos = Database.atributos_iniciais(shadow_id)
                        agilidade = 0
                        for atributo_id, valor in atributos:
                            if atributo_id == 6:
                                agilidade = valor
                                ordem1.append(char)
                                quant1.append(agilidade)
                    else:
                        personagem_id = Database.personagem_id(char)
                        persona_id = Database.persona_equipada(personagem_id)
                        atributos = Database.atributos(personagem_id, persona_id)
                        agilidade = atributos[5]
                        ordem1.append(personagem_id)
                        quant1.append(agilidade)
                insertion_sort(quant1, ordem1)
                ordem = ordem1
            else:
                ordem1 = []
                ordem2 = []
                quant1 = []
                quant2 = []
                await canal.send(f"""O grupo tirou um dado de {dado} e falhou em evitar ser emboscado, vocês atacarão por último.""")
                for personagem in party:
                    personagem_id = Database.personagem_id(personagem)
                    persona_id = Database.persona_equipada(personagem_id)
                    atributos = Database.atributos(personagem_id, persona_id)
                    agilidade = atributos[5]
                    ordem1.append(personagem)
                    quant1.append(agilidade)
                insertion_sort(quant1, ordem1)
                for tipo, char in horda:
                    if tipo == "s":
                        shadow_id = Database.shadow_id(char)
                        atributos = Database.atributos_iniciais(shadow_id)
                        agilidade = 0
                        for atributo_id, valor in atributos:
                            if atributo_id == 6:
                                agilidade = valor
                                ordem2.append(char)
                                quant2.append(agilidade)
                    else:
                        personagem_id = Database.personagem_id(char)
                        persona_id = Database.persona_equipada(personagem_id)
                        atributos = Database.atributos(personagem_id, persona_id)
                        agilidade = atributos[5]
                        ordem2.append(personagem_id)
                        quant2.append(agilidade)
                insertion_sort(quant2, ordem2)
                ordem = ordem2 + ordem1
            embed = discord.Embed(
                title=f"""**Ordem de turnos**""",
                colour=discord.Colour.blue()
            )
            texto = ""
            i = 1
            for elem in ordem:
                texto += f"""{i}. {elem}\n"""
                i += 1
            texto[:-1]
            embed.add_field(name="ORDEM:", value=texto, inline=False)
            await canal.send(embed=embed)
        else:
            await ctx.send("Cálculo cancelado.")
    else:
        await ctx.send("Sem requisitos mínimos para iniciar um combate.")

def insertion_sort(arr, ordem): 
    for i in range(1, len(arr)): 
        key = arr[i]
        key2 = ordem[i]
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j]
                ordem[j+1] = ordem[j]
                j -= 1
        arr[j+1] = key 
        ordem[j+1] = key2
    
@bot.command()
async def ataque_fisico(ctx,  canal : discord.TextChannel, sentido, codigo1, codigo2):
    try:
        codigo1 = int(codigo1)
        codigo2 = int(codigo2)
        if sentido == "party":
            personagem_id = Database.personagem_id(party[codigo1-1])
            persona_id = Database.persona_equipada(personagem_id)
            usuario = Database.discord_user(personagem_id)
            equips = Database.itens_equipados(personagem_id)
            meelee = equips[0]
            atributos_atacante = Database.atributos(personagem_id, persona_id)
            for i in range(len(atributos_atacante)):
                    atributos_atacante[i] = atributos_atacante[i][1]
            atributos_soma = Database.atributos_soma(personagem_id)
            atributos_porcent = Database.atributos_porcent(personagem_id)
            for i in range(len(atributos_atacante)):
                a = atributos_atacante[i] + atributos_soma[i]
                p = (atributos_porcent[i]/100) * a
                if atributos_soma[i] > 0:
                    atributos_atacante[i] += int(a+p)
                else:
                    atributos_atacante[i] += int(p)
            if horda[codigo2-1][0] == "s":
                shadow_id = Database.shadow_id(horda[codigo2-1][1])
                fraquezas = Database.fraquezas(shadow_id)
                atributos_defensor = Database.atributos_iniciais(shadow_id)
                for i in range(len(atributos_defensor)):
                    atributos_defensor[i] = atributos_defensor[i][1]
                atributos_soma = Database.atributos_soma(shadow_id)
                atributos_porcent = Database.atributos_porcent(shadow_id)
                for i in range(len(atributos_defensor)):
                    a = atributos_defensor[i] + atributos_soma[i]
                    p = (atributos_porcent[i]/100) * a
                    if atributos_soma[i] > 0:
                        atributos_defensor[i] += int(a+p)
                    else:
                        atributos_defensor[i] += int(p)
                next = 0
                while next == 0:
                    await ctx.send("Qual o valor critério? (0 a 100)")
                    msg = await bot.wait_for('message')
                    mensagem = msg.content
                    try:
                        var = int(mensagem)
                        if var > 0 and var <= 100:
                            next = 1
                    except:
                        await ctx.send("Digite um número entre 0 e 100.")
                valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*party_mult_acc[codigo1-1]) - (10*horda_mult_evs[codigo1-1])
                await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                dado = await Dado.rolagem_pronta(bot, canal, party[codigo1-1], usuario, 1, 100)
                critico = 10 + (party_mult_crit[codigo1-1] * 10)
                if dado <= valor_criterio:
                    valor_arma = Database.valor_item(meelee)
                    dano = int(20 + (math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2])))
                    if party_mult_atk[codigo1-1] > 0:
                        dano = dano + (0,3 * party_mult_atk[codigo1-1] * dano)
                    elif party_mult_atk[codigo1-1] < 0:
                        dano = dano - (0,3 * party_mult_atk[codigo1-1] * dano)
                    dano_mitigado = int(dano / math.sqrt(atributos_defensor[4]*8))
                    if horda_mult_def[codigo2-1] > 0:
                        dano_mitigado = dano + (0,3 * horda_mult_def[codigo2-1] * dano)
                    elif horda_mult_def[codigo2-1] < 0:
                        dano = dano - (0,3 * horda_mult_def[codigo2-1] * dano)
                    dano = dano - dano_mitigado
                    if horda_elem_dano[codigo2-1][0] > 0:
                        if horda_elem_dano[codigo2-1][0] == 1:
                            dano = dano * 2
                            await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                        elif horda_elem_dano[codigo2-1][0] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                        elif horda_elem_dano[codigo2-1][0] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                        elif horda_elem_dano[codigo2-1][0] == 4:
                            await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                        elif horda_elem_dano[codigo2-1][0] == 5:
                            await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano em **{party[codigo1-1]}**!""")
                        else:
                            await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                    elif fraquezas[0] == 1:
                        dano = dano * 2
                        await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                    elif fraquezas[0] == 2:
                        dano = dano / 2
                        await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                    elif fraquezas[0] == 3:
                        dano = 0
                        await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                    elif fraquezas[0] == 4:
                        await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                    elif fraquezas[0] == 5:
                        await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano em **{party[codigo1-1]}**!""")
                    else:
                        if dado <= critico:
                            dado = dano * 2
                            await canal.send(f"""**CRÍTICO! {party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                        else:
                            await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                else:
                    await canal.send(f"""**{party[codigo1-1]}** errou o ataque físico  em **{horda[codigo2-1][1]}**""")
            else:
                defensor_id = Database.personagem_id(party[codigo2-1])
                d_persona_id = Database.persona_equipada(personagem_id)
                equips_defensor = Database.itens_equipados()
                armadura_defensor = equips[2]
                fraquezas = Database.fraquezas(d_persona_id)
                atributos_defensor = Database.atributos(defensor_id, d_persona_id)
                for i in range(len(atributos_defensor)):
                    atributos_defensor[i] = atributos_defensor[i][1]
                atributos_soma = Database.atributos_soma(defensor_id)
                atributos_porcent = Database.atributos_porcent(defensor_id)
                for i in range(len(atributos_defensor)):
                    a = atributos_defensor[i] + atributos_soma[i]
                    p = (atributos_porcent[i]/100) * a
                    if atributos_soma[i] > 0:
                        atributos_defensor[i] += int(a+p)
                    else:
                        atributos_defensor[i] += int(p)
                next = 0
                while next == 0:
                    await ctx.send("Qual o valor critério? (0 a 100)")
                    msg = await bot.wait_for('message')
                    mensagem = msg.content
                    try:
                        var = int(mensagem)
                        if var > 0 and var <= 100:
                            next = 1
                    except:
                        await ctx.send("Digite um número entre 0 e 100.")
                valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*party_mult_acc[codigo1-1]) - (10*horda_mult_evs[codigo1-1])
                await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                dado = await Dado.rolagem_pronta(bot, canal, party[codigo1-1], usuario, 1, 100)
                critico = 10 + (party_mult_crit[codigo1-1] * 10)
                if dado <= valor_criterio:
                    valor_arma = Database.valor_item(meelee)
                    dano = int(20 + math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2]))
                    if party_mult_atk[codigo1-1] > 0:
                        dano = dano + (0,3 * party_mult_atk[codigo1-1] * dano)
                    elif party_mult_atk[codigo1-1] < 0:
                        dano = dano - (0,3 * party_mult_atk[codigo1-1] * dano)
                    if armadura_defensor == None:
                        valor_armadura = 0
                    else:
                        valor_armadura = Database.valor_item(armadura_defensor)
                    dano_mitigado = int(dano / math.sqrt((atributos_defensor[4]*8)+valor_armadura))
                    if horda_mult_def[codigo2-1] > 0:
                        dano_mitigado = dano + (0,3 * horda_mult_def[codigo2-1] * dano)
                    elif horda_mult_def[codigo2-1] < 0:
                        dano = dano - (0,3 * horda_mult_def[codigo2-1] * dano)
                    dano = dano - dano_mitigado
                    if horda_elem_dano[codigo2-1][0] > 0:
                        if horda_elem_dano[codigo2-1][0] == 1:
                            dano = dano * 2
                            await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                        elif horda_elem_dano[codigo2-1][0] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                        elif horda_elem_dano[codigo2-1][0] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                        elif horda_elem_dano[codigo2-1][0] == 4:
                            await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                        elif horda_elem_dano[codigo2-1][0] == 5:
                            await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano em **{party[codigo1-1]}**!""")
                        else:
                            await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                    elif fraquezas[0] == 1:
                        dano = dano * 2
                        await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                    elif fraquezas[0] == 2:
                        dano = dano / 2
                        await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                    elif fraquezas[0] == 3:
                        dano = 0
                        await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                    elif fraquezas[0] == 4:
                        await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                    elif fraquezas[0] == 5:
                        await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano em **{party[codigo1-1]}**!""")
                    else:
                        if dado <= critico:
                            dado = dano * 2
                            await canal.send(f"""**CRÍTICO! {party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                        else:
                            await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                else:
                    await ctx.send(f"""**{party[codigo1-1]}** errou o ataque físico  em **{horda[codigo2-1][1]}**""")
        elif sentido == "horda":
            personagem_id = Database.personagem_id(party[codigo2-1])
            persona_id = Database.persona_equipada(personagem_id)
            usuario = Database.discord_user(personagem_id)
            equips = Database.itens_equipados(personagem_id)
            fraquezas = Database.fraquezas(persona_id)
            armadura = equips[2]
            atributos_defensor = Database.atributos(personagem_id, persona_id)
            for i in range(len(atributos_defensor)):
                atributos_defensor[i] = atributos_defensor[i][1]
            atributos_soma = Database.atributos_soma(personagem_id)
            atributos_porcent = Database.atributos_porcent(personagem_id)
            for i in range(len(atributos_defensor)):
                a = atributos_defensor[i] + atributos_soma[i]
                p = (atributos_porcent[i]/100) * a
                if atributos_soma[i] > 0:
                    atributos_defensor[i] += int(a+p)
                else:
                    atributos_defensor[i] += int(p)
            if horda[codigo1-1][0] == "s":
                shadow_id = Database.shadow_id(horda[codigo1-1][1])
                atributos_atacante = Database.atributos_iniciais(shadow_id)
                for i in range(len(atributos_atacante)):
                    atributos_atacante[i] = atributos_atacante[i][1]
                atributos_soma = Database.atributos_soma(shadow_id)
                atributos_porcent = Database.atributos_porcent(shadow_id)
                for i in range(len(atributos_atacante)):
                    a = atributos_atacante[i] + atributos_soma[i]
                    p = (atributos_porcent[i]/100) * a
                    if atributos_soma[i] > 0:
                        atributos_atacante[i] += int(a+p)
                    else:
                        atributos_atacante[i] += int(p)
                next = 0
                while next == 0:
                    await ctx.send("Qual o valor critério? (0 a 100)")
                    msg = await bot.wait_for('message')
                    mensagem = msg.content
                    try:
                        var = int(mensagem)
                        if var > 0 and var <= 100:
                            next = 1
                    except:
                        await ctx.send("Digite um número entre 0 e 100.")
                valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*horda_mult_acc[codigo1-1])- (10*party_mult_evs[codigo1-1])
                await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                dado = await Dado.rolagem_pronta(bot, canal, "Mestre", "Axuáti#9639", 1, 100)
                critico = 10 + (party_mult_crit[codigo1-1] * 10)
                if dado <= valor_criterio:
                    dano = int(20 * math.sqrt(atributos_atacante[2]))
                    if horda_mult_atk[codigo1-1] > 0:
                        dano = dano + (0,3 * horda_mult_atk[codigo1-1] * dano)
                    elif horda_mult_atk[codigo1-1] < 0:
                        dano = dano - (0,3 * horda_mult_atk[codigo1-1] * dano)
                    if armadura == None:
                        valor_armadura = 0
                    else:
                        valor_armadura = Database.valor_item(armadura)
                    if armadura == None:
                        valor_armadura = 0
                    else:
                        valor_armadura = Database.valor_item(armadur)
                    dano_mitigado = int(dano / math.sqrt((atributos_defensor[4]*8) + valor_armadura))
                    if party_mult_def[codigo2-1] > 0:
                        dano_mitigado = dano + (0,3 *party_mult_def[codigo2-1] * dano)
                    elif party_mult_def[codigo2-1] < 0:
                        dano = dano - (0,3 * party_mult_def[codigo2-1] * dano)
                    dano = dano - dano_mitigado
                    if party_elem_dano[codigo2-1][0] > 0:
                        if party_elem_dano[codigo2-1][0] == 1:
                            dano = dano * 2
                            await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano e derrubou **{party[codigo2-1]}**!""")
                        elif party_elem_dano[codigo2-1][0] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {horda[codigo1-1][1]}** causou **{dano}** de dano em **{party[codigo2-1]}**!""")
                        elif party_elem_dano[codigo2-1][0] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{party[codigo2-1]}** nulificou todo o dano causado!""")
                        elif party_elem_dano[codigo2-1][0] == 4:
                            await canal.send(f"""**DRENOU! **{party[codigo2-1]}** se curou em **{dano}**!""")
                        elif party_elem_dano[codigo2-1][0] == 5:
                            await canal.send(f"""**REFLETIU! **{party[codigo2-1]}** refletiu **{dano}** de dano em **{horda[codigo1-1][1]}**!""")
                        else:
                            await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano em **{party[codigo2-1]}**!""")
                    elif fraquezas[0] == 1:
                        dano = dano * 2
                        await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano e derrubou **{party[codigo2-1]}**!""")
                    elif fraquezas[0] == 2:
                        dano = dano / 2
                        await canal.send(f"""**RESISTIU! {horda[codigo1-1][1]}** causou **{dano}** de dano em **{party[codigo2-1]}**!""")
                    elif fraquezas[0] == 3:
                        dano = 0
                        await canal.send(f"""**NULIFICOU! **{party[codigo2-1]}** nulificou todo o dano causado!""")
                    elif fraquezas[0] == 4:
                        await canal.send(f"""**DRENOU! **{party[codigo2-1]}** se curou em **{dano}**!""")
                    elif fraquezas[0] == 5:
                        await canal.send(f"""**REFLETIU! **{party[codigo2-1]}** refletiu **{dano}** de dano em **{horda[codigo1-1][1]}**!""")
                    else:
                        if dado <= critico:
                            dado = dano * 2
                            await canal.send(f"""**CRÍTICO! {horda[codigo1-1][1]}** causou **{dano}** de dano e derrubou **{party[codigo2-1]}**!""")
                        else:
                            await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano em **{party[codigo2-1]}**!""")
                else:
                    await canal.send(f"""**{horda[codigo1-1][1]}** errou o ataque físico  em **{party[codigo2-1]}**""")
            else:
                atacante_id = Database.personagem_id(horda[codigo1-1])
                a_persona_id = Database.persona_equipada(personagem_id)
                equips_atacante = Database.itens_equipados()
                meelee_atacante = equips[0]
                atributos_atacante = Database.atributos(atacante_id, d_persona_id)
                for i in range(len(atributos_atacante)):
                    atributos_atacante[i] = atributos_atacante[i][1]
                atributos_soma = Database.atributos_soma(atacante_id)
                atributos_porcent = Database.atributos_porcent(atacante_id)
                for i in range(len(atributos_atacante)):
                    a = atributos_atacante[i] + atributos_soma[i]
                    p = (atributos_porcent[i]/100) * a
                    if atributos_soma[i] > 0:
                        atributos_atacante[i] += int(a+p)
                    else:
                        atributos_atacante[i] += int(p)
                next = 0
                while next == 0:
                    await ctx.send("Qual o valor critério? (0 a 100)")
                    msg = await bot.wait_for('message')
                    mensagem = msg.content
                    try:
                        var = int(mensagem)
                        if var > 0 and var <= 100:
                            next = 1
                    except:
                        await ctx.send("Digite um número entre 0 e 100.")
                valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*horda_mult_acc[codigo1-1])- (10*party_mult_evs[codigo1-1])
                await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                dado = await Dado.rolagem_pronta(bot, canal, "Mestre", "Axuáti#9639", 1, 100)
                critico = 10 + (party_mult_crit[codigo1-1] * 10)
                if dado <= valor_criterio:
                    valor_arma = Database.valor_item(meelee_atacante)
                    dano = int(20 + math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2]))
                    if horda_mult_atk[codigo1-1] > 0:
                        dano = dano + (0,3 * horda_mult_atk[codigo1-1] * dano)
                    elif horda_mult_atk[codigo1-1] < 0:
                        dano = dano - (0,3 * horda_mult_atk[codigo1-1] * dano)
                    if armadura == None:
                        valor_armadura = 0
                    else:
                        valor_armadura = Database.valor_item(armadura)
                    dano_mitigado = int(math.sqrt((atributos_defensor[4]*8)+valor_armadura))
                    if party_mult_def[codigo2-1] > 0:
                        dano_mitigado = dano + (0,3 * party_mult_def[codigo2-1] * dano)
                    elif party_mult_def[codigo2-1] < 0:
                        dano = dano - (0,3 * party_mult_def[codigo2-1] * dano)
                    dano = dano - dano_mitigado
                    if party_elem_dano[codigo2-1][0] > 0:
                        if party_elem_dano[codigo2-1][0] == 1:
                            dano = dano * 2
                            await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano e derrubou **{party[codigo2-1]}**!""")
                        elif party_elem_dano[codigo2-1][0] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {horda[codigo1-1][1]}** causou **{dano}** de dano em **{party[codigo2-1]}**!""")
                        elif party_elem_dano[codigo2-1][0] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{party[codigo2-1]}** nulificou todo o dano causado!""")
                        elif party_elem_dano[codigo2-1][0] == 4:
                            await canal.send(f"""**DRENOU! **{party[codigo2-1]}** se curou em **{dano}**!""")
                        elif party_elem_dano[codigo2-1][0] == 5:
                            await canal.send(f"""**REFLETIU! **{party[codigo2-1]}** refletiu **{dano}** de dano em **{horda[codigo1-1][1]}**!""")
                        else:
                            await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano em **{party[codigo2-1]}**!""")
                    elif fraquezas[0] == 1:
                        dano = dano * 2
                        await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano e derrubou **{party[codigo2-1]}**!""")
                    elif fraquezas[0] == 2:
                        dano = dano / 2
                        await canal.send(f"""**RESISTIU! {horda[codigo1-1][1]}** causou **{dano}** de dano em **{party[codigo2-1]}**!""")
                    elif fraquezas[0] == 3:
                        dano = 0
                        await canal.send(f"""**NULIFICOU! **{party[codigo2-1]}** nulificou todo o dano causado!""")
                    elif fraquezas[0] == 4:
                        await canal.send(f"""**DRENOU! **{party[codigo2-1]}** se curou em **{dano}**!""")
                    elif fraquezas[0] == 5:
                        await canal.send(f"""**REFLETIU! **{party[codigo2-1]}** refletiu **{dano}** de dano em **{horda[codigo1-1][1]}**!""")
                    else:
                        if dado <= critico:
                            dado = dano * 2
                            await canal.send(f"""**CRÍTICO! {horda[codigo1-1][1]}** causou **{dano}** de dano e derrubou **{party[codigo2-1]}**!""")
                        else:
                            await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano em **{party[codigo2-1]}**!""")
                else:
                    await canal.send(f"""**{horda[codigo1-1][1]}** errou o ataque físico  em **{party[codigo2-1]}**""")
    except:
        await canal.send("Algo está incorreto.")

@bot.command()
async def tiro(ctx, canal : discord.TextChannel, codigo1, codigo2):
    try:
        codigo1 = int(codigo1)
        codigo2 = int(codigo2)
        personagem_id = Database.personagem_id(party[codigo1-1])
        persona_id = Database.persona_equipada(personagem_id)
        usuario = Database.discord_user(personagem_id)
        equips = Database.itens_equipados(personagem_id)
        ranged = equips[1]
        atributos_atacante = Database.atributos(personagem_id, persona_id)
        for i in range(len(atributos_atacante)):
                atributos_atacante[i] = atributos_atacante[i][1]
        atributos_soma = Database.atributos_soma(personagem_id)
        atributos_porcent = Database.atributos_porcent(personagem_id)
        for i in range(len(atributos_atacante)):
            a = atributos_atacante[i] + atributos_soma[i]
            p = (atributos_porcent[i]/100) * a
            if atributos_soma[i] > 0:
                atributos_atacante[i] += int(a+p)
            else:
                atributos_atacante[i] += int(p)
        if horda[codigo2-1][0] == "s":
            shadow_id = Database.shadow_id(horda[codigo2-1][1])
            fraquezas = Database.fraquezas(shadow_id)
            atributos_defensor = Database.atributos_iniciais(shadow_id)
            for i in range(len(atributos_defensor)):
                atributos_defensor[i] = atributos_defensor[i][1]
            atributos_soma = Database.atributos_soma(shadow_id)
            atributos_porcent = Database.atributos_porcent(shadow_id)
            for i in range(len(atributos_defensor)):
                a = atributos_defensor[i] + atributos_soma[i]
                p = (atributos_porcent[i]/100) * a
                if atributos_soma[i] > 0:
                    atributos_defensor[i] += int(a+p)
                else:
                    atributos_defensor[i] += int(p)
            next = 0
            while next == 0:
                await ctx.send("Qual o valor critério? (0 a 100)")
                msg = await bot.wait_for('message')
                mensagem = msg.content
                try:
                    var = int(mensagem)
                    if var > 0 and var <= 100:
                        next = 1
                except:
                    await ctx.send("Digite um número entre 0 e 100.")
            valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*party_mult_acc[codigo1-1]) - (10*horda_mult_evs[codigo1-1])
            await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
            critico = 10 + (party_mult_crit[codigo1-1] * 10)
            dado = await Dado.rolagem_pronta(bot, canal, party[codigo1-1], usuario, 1, 100)
            if dado <= valor_criterio:
                valor_arma = Database.valor_item(ranged)
                dano = int(math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2]))
                if party_mult_atk[codigo1-1] > 0:
                    dano = dano + (0,3 * party_mult_atk[codigo1-1] * dano)
                elif party_mult_atk[codigo1-1] < 0:
                    dano = dano - (0,3 * party_mult_atk[codigo1-1] * dano)
                dano_mitigado = int(math.sqrt(atributos_defensor[4]*8))
                if horda_mult_def[codigo2-1] > 0:
                    dano_mitigado = dano + (0,3 * horda_mult_def[codigo2-1] * dano)
                elif horda_mult_def[codigo2-1] < 0:
                    dano = dano - (0,3 * horda_mult_def[codigo2-1] * dano)
                dano = dano - dano_mitigado
                if horda_elem_dano[codigo2-1][0] > 0:
                    if horda_elem_dano[codigo2-1][1] == 1:
                        dano = dano * 2
                        await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                    elif horda_elem_dano[codigo2-1][1] == 2:
                        dano = dano / 2
                        await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                    elif horda_elem_dano[codigo2-1][1] == 3:
                        dano = 0
                        await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                    elif horda_elem_dano[codigo2-1][1] == 4:
                        await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                    elif horda_elem_dano[codigo2-1][1] == 5:
                        await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano em **{party[codigo1-1]}**!""")
                    else:
                        await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                elif fraquezas[0] == 1:
                    dano = dano * 2
                    await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                elif fraquezas[0] == 2:
                    dano = dano / 2
                    await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                elif fraquezas[0] == 3:
                    dano = 0
                    await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                elif fraquezas[0] == 4:
                    await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                elif fraquezas[0] == 5:
                    await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano em **{party[codigo1-1]}**!""")
                else:
                    if dado <= critico:
                        dado = dano * 2
                        await canal.send(f"""**CRÍTICO! {party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                    else:
                        await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
            else:
                await canal.send(f"""**{party[codigo1-1]}** errou o tiro em **{horda[codigo2-1][1]}**""")
        else:
            defensor_id = Database.personagem_id(party[codigo2-1])
            d_persona_id = Database.persona_equipada(personagem_id)
            equips_defensor = Database.itens_equipados()
            armadura_defensor = equips[2]
            fraquezas = Database.fraquezas(d_persona_id)
            atributos_defensor = Database.atributos(defensor_id, d_persona_id)
            for i in range(len(atributos_defensor)):
                atributos_defensor[i] = atributos_defensor[i][1]
            atributos_soma = Database.atributos_soma(defensor_id)
            atributos_porcent = Database.atributos_porcent(defensor_id)
            for i in range(len(atributos_defensor)):
                a = atributos_defensor[i] + atributos_soma[i]
                p = (atributos_porcent[i]/100) * a
                if atributos_soma[i] > 0:
                    atributos_defensor[i] += int(a+p)
                else:
                    atributos_defensor[i] += int(p)
            next = 0
            while next == 0:
                await ctx.send("Qual o valor critério? (0 a 100)")
                msg = await bot.wait_for('message')
                mensagem = msg.content
                try:
                    var = int(mensagem)
                    if var > 0 and var <= 100:
                        next = 1
                except:
                    await ctx.send("Digite um número entre 0 e 100.")
            valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*party_mult_acc[codigo1-1]) - (10*horda_mult_evs[codigo1-1])
            await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
            dado = await Dado.rolagem_pronta(bot, canal, party[codigo1-1], usuario, 1, 100)
            critico = 10 + (party_mult_crit[codigo1-1] * 10)
            if dado <= valor_criterio:
                valor_arma = Database.valor_item(ranged)
                dano = int(math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2]))
                if party_mult_atk[codigo1-1] > 0:
                    dano = dano + (0,3 * party_mult_atk[codigo1-1] * dano)
                elif party_mult_atk[codigo1-1] < 0:
                    dano = dano - (0,3 * party_mult_atk[codigo1-1] * dano)
                if armadura_defensor == None:
                    valor_armadura = 0
                else:
                    valor_armadura = Database.valor_item(armadura_defensor)
                dano_mitigado = int(dano / math.sqrt((atributos_defensor[4]*8)+valor_armadura))
                if horda_mult_def[codigo2-1] > 0:
                    dano_mitigado = dano + (0,3 * horda_mult_def[codigo2-1] * dano)
                elif horda_mult_def[codigo2-1] < 0:
                    dano = dano - (0,3 * horda_mult_def[codigo2-1] * dano)
                dano = dano - dano_mitigado
                if horda_elem_dano[codigo2-1][1] > 0:
                    if horda_elem_dano[codigo2-1][1] == 1:
                        dano = dano * 2
                        await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                    elif horda_elem_dano[codigo2-1][1] == 2:
                        dano = dano / 2
                        await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                    elif horda_elem_dano[codigo2-1][1] == 3:
                        dano = 0
                        await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                    elif horda_elem_dano[codigo2-1][1] == 4:
                        await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                    elif horda_elem_dano[codigo2-1][1] == 5:
                        await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano em **{party[codigo1-1]}**!""")
                    else:
                        await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                elif fraquezas[1] == 1:
                    dano = dano * 2
                    await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                elif fraquezas[1] == 2:
                    dano = dano / 2
                    await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
                elif fraquezas[1] == 3:
                    dano = 0
                    await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                elif fraquezas[1] == 4:
                    await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                elif fraquezas[1] == 5:
                    await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano em **{party[codigo1-1]}**!""")
                else:
                    if dado <= critico:
                        dado = dano * 2
                        await canal.send(f"""**CRÍTICO! {party[codigo1-1]}** causou **{dano}** de dano e derrubou **{horda[codigo2-1][1]}**!""")
                    else:
                        await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano em **{horda[codigo2-1][1]}**!""")
            else:
                await canal.send(f"""**{party[codigo1-1]}** errou o tiro em **{horda[codigo2-1][1]}**""")
    except:
        await canal.send("Algo está incorreto.")

@bot.command()
async def habilidade(ctx, canal : discord.TextChannel, sentido, codigo1, codigo2, *habilidade):
    try:
        nome = ""
        for palavra in habilidade:
            nome += palavra + " "
        nome = nome[:-1]
        codigo1 = int(codigo1)
        codigo2 = int(codigo2)
        skill_id = Database.skill_id(nome)
        if skill_id != False:
            nome_skill = Database.nome_skill(skill_id)
            if sentido == "party":
                personagem_id = Database.personagem_id(party[codigo1-1])
                persona_id = Database.persona_equipada(personagem_id)
                skills = Database.skills_id(personagem_id, persona_id)
                if skill_id in skills:
                    intensidade = Database.intensidade(skill_id)
                    elemento = Database.elemento(skill_id)
                    nome_elemento = Database.nome_elemento(elemento)
                    usuario = Database.discord_user(personagem_id)
                    atributos_atacante = Database.atributos(personagem_id, persona_id)
                    for i in range(len(atributos_atacante)):
                            atributos_atacante[i] = atributos_atacante[i][1]
                    atributos_soma = Database.atributos_soma(personagem_id)
                    atributos_porcent = Database.atributos_porcent(personagem_id)
                    for i in range(len(atributos_atacante)):
                        a = atributos_atacante[i] + atributos_soma[i]
                        p = (atributos_porcent[i]/100) * a
                        if atributos_soma[i] > 0:
                            atributos_atacante[i] += int(a+p)
                        else:
                            atributos_atacante[i] += int(p)
                    if horda[codigo2-1][0] == "s":
                        shadow_id = Database.shadow_id(horda[codigo2-1][1])
                        fraquezas = Database.fraquezas(shadow_id)
                        atributos_defensor = Database.atributos_iniciais(shadow_id)
                        for i in range(len(atributos_defensor)):
                            atributos_defensor[i] = atributos_defensor[i][1]
                        atributos_soma = Database.atributos_soma(shadow_id)
                        atributos_porcent = Database.atributos_porcent(shadow_id)
                        for i in range(len(atributos_defensor)):
                            a = atributos_defensor[i] + atributos_soma[i]
                            p = (atributos_porcent[i]/100) * a
                            if atributos_soma[i] > 0:
                                atributos_defensor[i] += int(a+p)
                            else:
                                atributos_defensor[i] += int(p)
                        next = 0
                        while next == 0:
                            await ctx.send("Qual o valor critério? (0 a 100)")
                            msg = await bot.wait_for('message')
                            mensagem = msg.content
                            try:
                                var = int(mensagem)
                                if var > 0 and var <= 100:
                                    next = 1
                            except:
                                await ctx.send("Digite um número entre 0 e 100.")
                        valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*party_mult_acc[codigo1-1]) - (10*horda_mult_evs[codigo1-1])
                        await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                        dado = await Dado.rolagem_pronta(bot, canal, party[codigo1-1], usuario, 1, 100)
                        if dado <= valor_criterio:
                            if elemento < 3:
                                dano = int((intensidade * 25) * math.sqrt(atributos_atacante[2]))
                            else:
                                dano = int((intensidade * 25) + ((intensidade * 25) * (atributos_atacante[3]/30)))
                            if party_mult_atk[codigo1-1] > 0:
                                dano = dano + (0,3 * party_mult_atk[codigo1-1] * dano)
                            elif party_mult_atk[codigo1-1] < 0:
                                dano = dano - (0,3 * party_mult_atk[codigo1-1] * dano)
                            dano_mitigado = int(math.sqrt(atributos_defensor[4]*8))
                            if horda_mult_def[codigo2-1] > 0:
                                dano_mitigado = dano + (0,3 * horda_mult_def[codigo2-1] * dano)
                            elif horda_mult_def[codigo2-1] < 0:
                                dano = dano - (0,3 * horda_mult_def[codigo2-1] * dano)
                            dano = dano - dano_mitigado
                            if horda_elem_dano[codigo2-1][elemento-1] > 0:
                                if horda_elem_dano[codigo2-1][elemento-1] == 1:
                                    dano = dano * 2
                                    await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{horda[codigo2-1][1]}**!""")
                                elif horda_elem_dano[codigo2-1][elemento-1] == 2:
                                    dano = dano / 2
                                    await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{horda[codigo2-1][1]}**!""")
                                elif horda_elem_dano[codigo2-1][elemento-1] == 3:
                                    dano = 0
                                    await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                                elif horda_elem_dano[codigo2-1][elemento-1] == 4:
                                    await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                                elif horda_elem_dano[codigo2-1][elemento-1] == 5:
                                    await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{party[codigo1-1]}**!""")
                                else:
                                    await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{horda[codigo2-1][1]}**!""")
                            elif fraquezas[elemento-1] == 1:
                                dano = dano * 2
                                await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{horda[codigo2-1][1]}**!""")
                            elif fraquezas[elemento-1] == 2:
                                dano = dano / 2
                                await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{horda[codigo2-1][1]}**!""")
                            elif fraquezas[elemento-1] == 3:
                                dano = 0
                                await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                            elif fraquezas[elemento-1] == 4:
                                await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                            elif fraquezas[elemento-1] == 5:
                                await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{party[codigo1-1]}**!""")
                            else:
                                await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{horda[codigo2-1][1]}**!""")
                        else:
                            await canal.send(f"""**{party[codigo1-1]}** errou a habilidade **{nome_skill}** em **{horda[codigo2-1][1]}**""")
                    else:
                        defensor_id = Database.personagem_id(party[codigo2-1])
                        d_persona_id = Database.persona_equipada(personagem_id)
                        equips_defensor = Database.itens_equipados()
                        armadura_defensor = equips[2]
                        fraquezas = Database.fraquezas(d_persona_id)
                        atributos_defensor = Database.atributos(defensor_id, d_persona_id)
                        for i in range(len(atributos_defensor)):
                            atributos_defensor[i] = atributos_defensor[i][1]
                        atributos_soma = Database.atributos_soma(defensor_id)
                        atributos_porcent = Database.atributos_porcent(defensor_id)
                        for i in range(len(atributos_defensor)):
                            a = atributos_defensor[i] + atributos_soma[i]
                            p = (atributos_porcent[i]/100) * a
                            if atributos_soma[i] > 0:
                                atributos_defensor[i] += int(a+p)
                            else:
                                atributos_defensor[i] += int(p)
                        next = 0
                        while next == 0:
                            await ctx.send("Qual o valor critério? (0 a 100)")
                            msg = await bot.wait_for('message')
                            mensagem = msg.content
                            try:
                                var = int(mensagem)
                                if var > 0 and var <= 100:
                                    next = 1
                            except:
                                await ctx.send("Digite um número entre 0 e 100.")
                        valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*party_mult_acc[codigo1-1]) - (10*horda_mult_evs[codigo1-1])
                        await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                        dado = await Dado.rolagem_pronta(bot, canal, party[codigo1-1], usuario, 1, 100)
                        if dado <= valor_criterio:
                            if elemento < 3:
                                dano = int((intensidade * 25) * math.sqrt(atributos_atacante[2]))
                            else:
                                dano = int((intensidade * 25) + ((intensidade * 25) * (atributos_atacante[3]/30)))
                            if party_mult_atk[codigo1-1] > 0:
                                dano = dano + (0,3 * party_mult_atk[codigo1-1] * dano)
                            elif party_mult_atk[codigo1-1] < 0:
                                dano = dano - (0,3 * party_mult_atk[codigo1-1] * dano)
                            valor_armadura = Database.valor_item(armadura_defensor)
                            dano_mitigado = int(math.sqrt((atributos_defensor[4]*8)+valor_armadura))
                            if horda_mult_def[codigo2-1] > 0:
                                dano_mitigado = dano + (0,3 * horda_mult_def[codigo2-1] * dano)
                            elif horda_mult_def[codigo2-1] < 0:
                                dano = dano - (0,3 * horda_mult_def[codigo2-1] * dano)
                            dano = dano - dano_mitigado
                            if horda_elem_dano[codigo2-1][elemento-1] > 0:
                                if horda_elem_dano[codigo2-1][elemento-1] == 1:
                                    dano = dano * 2
                                    await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{horda[codigo2-1][1]}**!""")
                                elif horda_elem_dano[codigo2-1][elemento-1] == 2:
                                    dano = dano / 2
                                    await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{horda[codigo2-1][1]}**!""")
                                elif horda_elem_dano[codigo2-1][elemento-1] == 3:
                                    dano = 0
                                    await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                                elif horda_elem_dano[codigo2-1][elemento-1] == 4:
                                    await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                                elif horda_elem_dano[codigo2-1][elemento-1] == 5:
                                    await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{party[codigo1-1]}**!""")
                                else:
                                    await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{horda[codigo2-1][1]}**!""")
                            elif fraquezas[elemento-1] == 1:
                                dano = dano * 2
                                await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{horda[codigo2-1][1]}**!""")
                            elif fraquezas[elemento-1] == 2:
                                dano = dano / 2
                                await canal.send(f"""**RESISTIU! {party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{horda[codigo2-1][1]}**!""")
                            elif fraquezas[elemento-1] == 3:
                                dano = 0
                                await canal.send(f"""**NULIFICOU! **{horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                            elif fraquezas[elemento-1] == 4:
                                await canal.send(f"""**DRENOU! **{horda[codigo2-1][1]}** se curou em **{dano}**!""")
                            elif fraquezas[elemento-1] == 5:
                                await canal.send(f"""**REFLETIU! **{horda[codigo2-1][1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{party[codigo1-1]}**!""")
                            else:
                                await canal.send(f"""**{party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{horda[codigo2-1][1]}**!""")
                        else:
                            await canal.send(f"""**{party[codigo1-1]}** errou a habilidade **{nome_skill}** em **{horda[codigo2-1][1]}**""")
            elif sentido == "horda":
                personagem_id = Database.personagem_id(party[codigo2-1])
                persona_id = Database.persona_equipada(personagem_id)
                usuario = Database.discord_user(personagem_id)
                equips = Database.itens_equipados(personagem_id)
                fraquezas = Database.fraquezas(persona_id)
                armadura = equips[2]
                atributos_defensor = Database.atributos(personagem_id, persona_id)
                for i in range(len(atributos_defensor)):
                    atributos_defensor[i] = atributos_defensor[i][1]
                atributos_soma = Database.atributos_soma(personagem_id)
                atributos_porcent = Database.atributos_porcent(personagem_id)
                for i in range(len(atributos_defensor)):
                    a = atributos_defensor[i] + atributos_soma[i]
                    p = (atributos_porcent[i]/100) * a
                    if atributos_soma[i] > 0:
                        atributos_defensor[i] += int(a+p)
                    else:
                        atributos_defensor[i] += int(p)
                if horda[codigo1-1][0] == "s":
                    shadow_id = Database.shadow_id(horda[codigo1-1][1])
                    atributos_atacante = Database.atributos_iniciais(shadow_id)
                    nivel = Database.nivel_persona(shadow_id)
                    skills = Database.skills_shadow(shadow_id, nivel)
                else:
                    personagem_id = Database.personagem_id(horda[codigo1-1][1])
                    persona_id = Database.persona_equipada(personagem_id)
                    atributos_atacante = Database.atributos_iniciais(shadow_id)
                    skills = Database.skills_id(personagem_id, persona_id)
                    atributos_atacante = Database.atributos(personagem_id, persona_id)
                    for i in range(len(atributos_atacante)):
                            atributos_atacante[i] = atributos_atacante[i][1]
                    atributos_soma = Database.atributos_soma(personagem_id)
                    atributos_porcent = Database.atributos_porcent(personagem_id)
                    for i in range(len(atributos_atacante)):
                        a = atributos_atacante[i] + atributos_soma[i]
                        p = (atributos_porcent[i]/100) * a
                        if atributos_soma[i] > 0:
                            atributos_atacante[i] += int(a+p)
                        else:
                            atributos_atacante[i] += int(p)
                if skill_id in skills:
                    intensidade = Database.intensidade(skill_id)
                    elemento = Database.elemento(skill_id)
                    nome_elemento = Database.nome_elemento(elemento)
                    for i in range(len(atributos_atacante)):
                        atributos_atacante[i] = atributos_atacante[i][1]
                    atributos_soma = Database.atributos_soma(shadow_id)
                    atributos_porcent = Database.atributos_porcent(shadow_id)
                    for i in range(len(atributos_atacante)):
                        a = atributos_atacante[i] + atributos_soma[i]
                        p = (atributos_porcent[i]/100) * a
                        if atributos_soma[i] > 0:
                            atributos_atacante[i] += int(a+p)
                        else:
                            atributos_atacante[i] += int(p)
                    next = 0
                    while next == 0:
                        await ctx.send("Qual o valor critério? (0 a 100)")
                        msg = await bot.wait_for('message')
                        mensagem = msg.content
                        try:
                            var = int(mensagem)
                            if var > 0 and var <= 100:
                                next = 1
                        except:
                            await ctx.send("Digite um número entre 0 e 100.")
                    valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*horda_mult_acc[codigo1-1])- (10*party_mult_evs[codigo1-1])
                    await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                    dado = await Dado.rolagem_pronta(bot, canal, "Mestre", "Axuáti#9639", 1, 100)
                    if dado <= valor_criterio:
                        if elemento < 3:
                            dano = int((intensidade * 25) * math.sqrt(atributos_atacante[2]))
                        else:
                            dano = int((intensidade * 25) + ((intensidade * 25) * (atributos_atacante[3]/30)))
                        if horda_mult_atk[codigo1-1] > 0:
                            dano = dano + (0,3 * horda_mult_atk[codigo1-1] * dano)
                        elif horda_mult_atk[codigo1-1] < 0:
                            dano = dano - (0,3 * horda_mult_atk[codigo1-1] * dano)
                        valor_armadura = Database.valor_item(armadura)
                        dano_mitigado = int(math.sqrt((atributos_defensor[4]*8) + valor_armadura))
                        if party_mult_def[codigo2-1] > 0:
                            dano_mitigado = dano + (0,3 * party_mult_def[codigo2-1] * dano)
                        elif party_mult_def[codigo2-1] < 0:
                            dano = dano - (0,3 * party_mult_def[codigo2-1] * dano)
                        dano = dano - dano_mitigado
                        if party_elem_dano[codigo2-1][elemento-1] > 0:
                            if party_elem_dano[codigo2-1][elemento-1] == 1:
                                dano = dano * 2
                                await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{party[codigo2-1][1]}**!""")
                            elif party_elem_dano[codigo2-1][elemento-1] == 2:
                                dano = dano / 2
                                await canal.send(f"""**RESISTIU! {horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** em **{party[codigo2-1]}**!""")
                            elif party_elem_dano[codigo2-1][elemento-1] == 3:
                                dano = 0
                                await canal.send(f"""**NULIFICOU! **{party[codigo2-1]}** nulificou todo o dano causado!""")
                            elif party_elem_dano[codigo2-1][elemento-1] == 4:
                                await canal.send(f"""**DRENOU! **{party[codigo2-1]}** se curou em **{dano}**!""")
                            elif party_elem_dano[codigo2-1][elemento-1] == 5:
                                await canal.send(f"""**REFLETIU! **{party[codigo2-1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{horda[codigo1-1][1]}**!""")
                            else:
                                await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** em **{party[codigo2-1]}**!""")
                        elif fraquezas[elemento-1] == 1:
                            dano = dano * 2
                            await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{party[codigo2-1]}**!""")
                        elif fraquezas[elemento-1] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** em **{party[codigo2-1]}**!""")
                        elif fraquezas[elemento-1] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{party[codigo2-1]}** nulificou todo o dano causado!""")
                        elif fraquezas[elemento-1] == 4:
                            await canal.send(f"""**DRENOU! **{party[codigo2-1]}** se curou em **{dano}**!""")
                        elif fraquezas[elemento-1] == 5:
                            await canal.send(f"""**REFLETIU! **{party[codigo2-1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{horda[codigo1-1][1]}**!""")
                        else:
                            await canal.send(f"""**{horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** em **{party[codigo2-1]}**!""")
                    else:
                        await canal.send(f"""**{horda[codigo1-1][1]}** errou a habilidade **{nome_skill}** em **{party[codigo2-1]}**""")
    except:
        await ctx.send("Algo está incorreto.")

@bot.command()
async def add_atributo(ctx, canal : discord.TextChannel, personagem, tipo, quant, atributo):
    personagem_id = Database.personagem_id(personagem)
    if personagem_id != False:
        atributo_id = Database.atributo_id(atributo)
        if atributo_id != False:
            try:
                quant = int(quant)
                if quant >= 0:
                    if tipo == "n":
                        add = Database.add_atributo(personagem_id, atributo_id, quant)
                        if add:
                            await canal.send(f"""**{quant}** foi adicionado em **{atributo}** de **{personagem}**""")
                    elif tipo == "p":
                        mod = Database.mod_atributo(personagem_id, atributo_id, quant)
                        if mod:
                            await canal.send(f"""**{personagem}** agora recebe aumento de **{quant}%** de **{atributo}**""")
                    else:
                        await ctx.send(f"""Tipo incorreto (digite p(porcentagem) ou n(normal)""")
                else:
                    await ctx.send(f"""Valor incorreto.""")
            except:
                await ctx.send(f"""Valor incorreto.""")
    else:
        await ctx.send(f"""Este personagem não existe.""")

@bot.command()
async def del_atributo(ctx, canal : discord.TextChannel, personagem, quant, atributo):
    personagem_id = Database.personagem_id(personagem)
    if personagem_id != False:
        atributo_id = Database.atributo_id(atributo)
        if atributo_id != False:
            try:
                quant = int(quant)
                if quant > 0:
                    delete = Database.del_atributo(personagem_id, atributo_id, quant)
                    if delete:
                        await canal.send(f"""**{quant}** foi diminuido em **{atributo}** de **{personagem}**""")
                else:
                    await ctx.send(f"""Valor incorreto.""")
            except:
                await ctx.send(f"""Valor incorreto.""")
    else:
        await ctx.send(f"""Este personagem não existe.""")

@bot.command()
async def lider(ctx, canal : discord.TextChannel, personagem):
    if party != []:
        for i in range(len(party)):
            if party[i] == personagem:
                party.insert(0, mylist.pop(i))
                await canal.send(f"""**{personagem}** foi denominado o líder do grupo.""")
                break

@bot.command()
async def marcador(ctx,  canal : discord.TextChannel, tipo_marcador, tipo_grupo, codigo, quant):
    try:
        quant = int(quant)
        codigo = int(codigo)
        if tipo_marcador == "atk":
            if tipo_grupo == "party":
                party_mult_atk[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{party[codigo-1]}** teve seu ataque aumentado em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{party[codigo-1]}** teve seu ataque diminuido em {quant}.""")
            else:
                horda_mult_atk[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve seu ataque aumentado em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve seu ataque diminuido em {quant}.""")
        elif tipo_marcador == "def":
            if tipo_grupo == "party":
                party_mult_def[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{party[codigo-1]}** teve sua defesa aumentada em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{party[codigo-1]}** teve sua defesa diminuida em {quant}.""")
            else:
                horda_mult_atk[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve sua defesa aumentada em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve sua defesa diminuida em {quant}.""")
        elif tipo_marcador == "acc":
            if tipo_grupo == "party":
                party_mult_acc[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{party[codigo-1]}** teve sua acurácia aumentada em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{party[codigo-1]}** teve sua acurácia diminuida em {quant}.""")
            else:
                horda_mult_acc[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve sua acurácia aumentada em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve sua acurácia diminuida em {quant}.""")
        elif marcador == "evs":
            if tipo_grupo == "party":
                party_mult_evs[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{party[codigo-1]}** teve sua evasão aumentada em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{party[codigo-1]}** teve sua evasão diminuida em {quant}.""")
            else:
                horda_mult_evs[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve sua evasão aumentada em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve sua evasão diminuida em {quant}.""")
        else:
            if tipo_grupo == "party":
                party_mult_crit[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{party[codigo-1]}** teve sua taxa de acerto crítico aumentada em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{party[codigo-1]}** teve sua taxa de acerto crítico diminuida em {quant}.""")
            else:
                horda_mult_crit[codigo-1] += quant
                if quant > 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve sua taxa de acerto crítico aumentada em {quant}.""")
                elif quant < 0:
                    await canal.send(f"""**{horda[codigo-1][1]}** teve sua taxa de acerto crítico diminuida em {quant}.""")
    except:
        await ctx.send(f"""Erro""")

@bot.command()
async def interacao(ctx, tipo_grupo, codigo, elemento, tipo_interacao):
    try:
        codigo = int(codigo)
        atributo = int(atributo)
        tipo_interacao = int(tipo_interacao)
        if tipo_grupo == "horda":
            horda_elem_dano[codigo-1][elemento] == tipo_interacao
        elif tipo_grupo == "party":
            party_elem_dano[codigo-1][elemento] == tipo_interacao
        else:
            await ctx.send(f"""Tipo incorreto.""")
    except:
        await ctx.send(f"""Erro""")

def takeSecond(elem):
    return elem[1]

bot.load_extension("cogs.dado")
bot.run(data['token'])