import discord
import random
import pickle
from discord.ext import commands

from cogs.database import *
from cogs.canal import *

class Ficha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @classmethod
    def iniciar_info(self):
        info = {}
        shadows = Database.lista_shadows_id()
        if shadows:
            for shadow in shadows:
                info[shadow] = [0,0,0,0,0,0,0,0,0,0,0]
            with open('info.pickle', 'wb') as handle:
                pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()
            print("Informações de Shadows iniciadas.")

    @commands.command(name='atualizar_info')
    async def atualizar_info(self, ctx):
        with open('info.pickle', 'rb') as handle:
            info = pickle.load(handle)
        shadows = Database.lista_shadows_id()
        if shadows:
            for shadow in shadows:
                if shadow not in info:
                    info[shadow] = [0,0,0,0,0,0,0,0,0,0,0]
                    await ctx.send("**Shadow nova adicionada**")
            with open('info.pickle', 'wb') as handle:
                pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()
            await ctx.send("**Informação atualizada**")

    @commands.command(name='mostrar_ficha')
    async def mostrar_ficha(self, ctx,  canal : discord.TextChannel, *persona):
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
    
    @commands.command(name='info_shadow')
    async def info_shadow(self, ctx, *shadow):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_suporte())
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
        except:
            await ctx.send("Canal do suporte ainda não registrado.")

    @commands.command(name='revelar_afinidade')
    async def revelar_afinidade(self, ctx, *shadow):
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
    
    @commands.command(name='esconder_afinidade')
    async def esconder_afinidade(self, ctx, *shadow):
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
    
    @commands.command(name='ficha')
    async def ficha(self, ctx, personagem):
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
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
                emote = ["<:phys:790320130810839101>", "<:gun:790320131028287488>", "<:fire:790320130483421245>", "<:ice:790320130738356224>", "<:elec:790320130151809047>", "<:wind:790320130521169922>", "<:psy:790320130772566046>", "<:nuclear:790320130584084532>", "<:bless:790320130746744892>", "<:curse:790320130387214336>", "<:almighty:790320130297954374>", "<:ailment:790320130286551060>", "<:healing:790320130508718100>", "<:support:790320130323775518>", "<:passive:790320130780561408>", "<:navigator:798197909761556521>"]
                for skill in skills:
                    skill_id = Database.skill_id(skill)
                    elemento = Database.elemento(skill_id)
                    texto += f"""{skill} {emote[elemento-1]}\n"""
                texto = texto[:-1]
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
                await canal.send(embed=personagem_ficha)
                await canal.send(embed=embed)
                await canal.send(embed=embed2)
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
                emote = ["<:phys:790320130810839101>", "<:gun:790320131028287488>", "<:fire:790320130483421245>", "<:ice:790320130738356224>", "<:elec:790320130151809047>", "<:wind:790320130521169922>", "<:psy:790320130772566046>", "<:nuclear:790320130584084532>", "<:bless:790320130746744892>", "<:curse:790320130387214336>", "<:almighty:790320130297954374>", "<:ailment:790320130286551060>", "<:healing:790320130508718100>", "<:support:790320130323775518>", "<:passive:790320130780561408>", "<:navigator:798197909761556521>"]
                for skill in skills:
                    skill_id = Database.skill_id(skill)
                    elemento = Database.elemento(skill_id)
                    texto += f"""{skill} {emote[elemento-1]}\n"""
                texto = texto[:-1]
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
                await canal.send(embed=personagem_ficha)
                await canal.send(embed=embed)
                await canal.send(embed=embed2)
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
                await canal.send(embed=personas)
        else:
            await ctx.send("Personagem não encontrado.")

def setup(bot):
    bot.add_cog(Ficha(bot))