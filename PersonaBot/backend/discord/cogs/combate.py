import discord
import random
import pickle
from discord.ext import commands

from cogs.database import *
from cogs.canal import *

class Combate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.horda = []
        self.party = []
        self.horda_mult_atk = []
        self.party_mult_atk = []
        self.horda_mult_def = []
        self.party_mult_def = []
        self.horda_mult_acc = []
        self.party_mult_acc = []
        self.horda_mult_evs = []
        self.party_mult_evs = []
        self.horda_elem_dano = []
        self.party_elem_dano = []
        self.party_mult_crit = []
        self.horda_mult_crit = []
    
    @commands.command(name='add_horda')
    async def adicionar_horda(self, ctx, tipo, *personagem):
        nome = ""
        for palavra in personagem:
            nome += palavra + " "
        nome = nome[:-1]
        if tipo == "shadow"  or tipo == "s":
            shadow_id = Database.shadow_id(nome)
            if shadow_id != False:
                self.horda.append(("s",nome))
                self.horda_mult_atk.append(0)
                self.horda_mult_def.append(0)
                self.horda_mult_acc.append(0)
                self.horda_mult_evs.append(0)
                self.horda_mult_crit.append(0)
                self. horda_elem_dano.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                await ctx.send(f"""**{nome}** foi adicionado à horda.""")
            else:
                await ctx.send("Shadow não existente.")
        elif tipo == "personagem" or tipo == "p":
            personagem_id = Database.personagem_id(nome)
            if personagem_id != False:
                self.horda.append(("p",nome))
                self.horda_mult_atk.append(0)
                self.horda_mult_def.append(0)
                self.horda_mult_acc.append(0)
                self.horda_mult_evs.append(0)
                self.horda_mult_crit.append(0)
                self.horda_elem_dano.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                await ctx.send(f"""**{nome}** foi adicionado à horda.""")
            else:
                await ctx.send("Personagem não existente.")
        else:
            await ctx.send("Tipo incorreto.")
    
    @commands.command(name='add_party')
    async def adicionar_party(self, ctx, personagem):
        personagem_id = Database.personagem_id(personagem)
        if personagem_id != False:
            self.party.append(personagem)
            self.party_mult_atk.append(0)
            self.party_mult_def.append(0)
            self.party_mult_acc.append(0)
            self.party_mult_evs.append(0)
            self.party_mult_crit.append(0)
            self.party_elem_dano.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            await ctx.send(f"""**{personagem}** foi adicionado à Party.""")
        else:
            await ctx.send("Personagem não existente.")

    @commands.command(name='del_party')
    async def remover_party(self, ctx, personagem):
        if self.party != []:
            achou = 0
            i = 0
            while i < len(self.party) and achou == 0:
                if self.party[i] == personagem:
                    del self.party[i]
                    del self.party_mult_atk[i]
                    del self.party_mult_def[i]
                    del self.party_mult_acc[i]
                    del self.party_mult_evs[i]
                    del self.party_elem_dano[i]
                    del self.party_mult_crit[i]
                    await ctx.send(f"""**{personagem}** foi removido da Party.""")
                    achou = 1
            if achou == 0:
                await ctx.send("Nome não encontrado.")
        else:
            await ctx.send("Nome não encontrado.")
    
    @commands.command(name='del_horda')
    async def remover_horda(self, ctx, *personagem):
        nome = ""
        for palavra in personagem:
            nome += palavra + " "
        nome = nome[:-1]
        if self.horda != []:
            achou = 0
            i = 0
            while i < len(self.horda) and achou == 0:
                if self.horda[i][1] == nome:
                    del self.horda[i]
                    del self.horda_mult_atk[i]
                    del self.horda_mult_def[i]
                    del self.horda_mult_acc[i]
                    del self.horda_mult_evs[i]
                    del self.horda_elem_dano[i]
                    del self.horda_mult_crit[i]
                    await ctx.send(f"""**{nome}** foi removido da horda.""")
                    achou = 1
            if achou == 0:
                await ctx.send("Nome não encontrado.")
        else:
            await ctx.send("Nome não encontrado.")

    @commands.command(name='party')
    async def mostrar_party(self, ctx):
        if self.party != []:
            embed = discord.Embed(
                title=f"""**PARTY**""",
                colour=discord.Colour.blue()
            )
            texto = ""
            i = 1
            for elem in self.party:
                texto += f"""{i}.**{elem}**\n"""
                i +=1
            texto = texto[:-1]
            embed.add_field(name="Lista dos membros da Party", value=texto, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("A party está vazia")
    
    @commands.command(name='horda')
    async def mostrar_horda(self, ctx):
        if self.horda != []:
            embed = discord.Embed(
                title=f"""**HORDA**""",
                colour=discord.Colour.blue()
            )
            texto = ""
            i = 1
            for tipo, elem in self.horda:
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

    @commands.command(name='calcular_turnos')
    async def calcular_turnos(self, ctx):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            ordem = []
            if self.horda != [] and self.party != []:
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
                    lider_id = Database.personagem_id(self.party[0])
                    usuario = Database.discord_user(lider_id)
                    dado = await Dado.rolagem_pronta(bot, canal, self.party[0], usuario, 1, 100)
                    if dado <= valor_criterio:
                        ordem1 = []
                        ordem2 = []
                        quant1 = []
                        quant2 = []
                        await canal.send(f"""O grupo tirou um dado de {dado} e conseguiu emboscar a Shadow, vocês atacarão primeiro.""")
                        for personagem in self.party:
                            personagem_id = Database.personagem_id(personagem)
                            persona_id = Database.persona_equipada(personagem_id)
                            atributos = Database.atributos(personagem_id, persona_id)
                            agilidade = atributos[5]
                            ordem1.append(personagem)
                            quant1.append(agilidade)
                        insertion_sort(quant1, ordem1)
                        for tipo, char in self.horda:
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
                        for personagem in self.party:
                            personagem_id = Database.personagem_id(personagem)
                            persona_id = Database.persona_equipada(personagem_id)
                            atributos = Database.atributos(personagem_id, persona_id)
                            agilidade = atributos[5]
                            ordem1.append(personagem)
                            quant1.append(agilidade)
                        for tipo, char in self.horda:
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
                    lider_id = Database.personagem_id(self.party[0])
                    usuario = Database.discord_user(lider_id)
                    dado = await Dado.rolagem_pronta(bot, canal, self.party[0], usuario, 1, 100)
                    if dado <= valor_criterio:
                        ordem1 = []
                        quant1 = []
                        await canal.send(f"""O grupo tirou um dado de {dado} e conseguiu evitar ser emboscado, vocês atacarão de acordo co ma sua agilidade.""")
                        for personagem in self.party:
                            personagem_id = Database.personagem_id(personagem)
                            persona_id = Database.persona_equipada(personagem_id)
                            atributos = Database.atributos(personagem_id, persona_id)
                            agilidade = atributos[5]
                            ordem1.append(personagem)
                            quant1.append(agilidade)
                        insertion_sort(quant1, ordem1)
                        for tipo, char in self.horda:
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
                        for personagem in self.party:
                            personagem_id = Database.personagem_id(personagem)
                            persona_id = Database.persona_equipada(personagem_id)
                            atributos = Database.atributos(personagem_id, persona_id)
                            agilidade = atributos[5]
                            ordem1.append(personagem)
                            quant1.append(agilidade)
                        insertion_sort(quant1, ordem1)
                        for tipo, char in self.horda:
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
        except:
            await ctx.send("Canal do grupo não está registrado.")
    
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

    @commands.command(name='ataque_fisico')
    async def ataque_fisico(self, ctx):
        try:
            embed = discord.Embed(
                title=f"""Quem vai atacar?""",
                description=f"""Reaja com a opção desejada""",
                colour=discord.Colour.blue()
            )
            embed.add_field(name=":one:", value="Party", inline=False)
            embed.add_field(name=":two:", value="Horda", inline=False)
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
                embed = discord.Embed(
                    title=f"""Qual personagem da Party irá atacar?""",
                    description=f"""Reaja com a opção desejada""",
                    colour=discord.Colour.blue()
                )
                emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
                for j in range(len(self.party)):
                    embed.add_field(name=emojis_disc[j], value=self.party[j], inline=False)
                embed_msg = await ctx.send(embed=embed)
                for i in range(len(self.party)):
                    await embed_msg.add_reaction(emoji=emojis_raw[i])
                await embed_msg.add_reaction(emoji="❌")
                ok1 = 0
                while ok1 == 0:
                    reaction, user = await bot.wait_for('reaction_add', timeout=None)
                    if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                        ok1 = 1
                    if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                        ok1 = 2
                    if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                        ok1 = 3
                    if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                        ok1 = 4
                    if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                        ok1 = 5
                    if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                        ok1 = 6
                await embed_msg.delete()
                nome_party = self.party[ok1-1]
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[ok1-1]))
                personagem_id = Database.personagem_id(self.party[ok1-1])
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
                embed = discord.Embed(
                    title=f"""Quem da horda será atacado?""",
                    description=f"""Reaja com a opção desejada""",
                    colour=discord.Colour.blue()
                )
                emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
                for j in range(len(self.horda)):
                    embed.add_field(name=emojis_disc[j], value=self.horda[j][1], inline=False)
                embed_msg = await ctx.send(embed=embed)
                for i in range(len(self.horda)):
                    await embed_msg.add_reaction(emoji=emojis_raw[i])
                await embed_msg.add_reaction(emoji="❌")
                ok2 = 0
                while ok2 == 0:
                    reaction, user = await bot.wait_for('reaction_add', timeout=None)
                    if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                        ok2 = 1
                    if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                        ok2 = 2
                    if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                        ok2 = 3
                    if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                        ok2 = 4
                    if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                        ok2 = 5
                    if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                        ok2 = 6
                await embed_msg.delete()
                nome_horda = self.horda[ok2-1][1]
                if self.horda[ok2-1][0] == "s":
                    shadow_id = Database.shadow_id(self.horda[ok2-1][1])
                    fraquezas = Database.fraquezas(shadow_id)
                    atributos_defensor = Database.atributos_iniciais(shadow_id)
                    for i in range(len(atributos_defensor)):
                        atributos_defensor[i] = atributos_defensor[i][1]
                    atributos_porcent = Database.atributos_porcent(shadow_id)
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
                    valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.party_mult_acc[ok1-1]) - (10*self.horda_mult_evs[ok2-1])
                    await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                    dado = await Dado.rolagem_pronta(bot, canal, self.party[ok1-1], usuario, 1, 100)
                    critico = 10 + (self.party_mult_crit[ok1-1] * 10)
                    if dado <= valor_criterio:
                        valor_arma = Database.valor_item(meelee)
                        dano = int(20 + (math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2])))
                        if self.party_mult_atk[ok1-1] > 0:
                            dano = dano + (0,3 * self.party_mult_atk[ok1-1] * dano)
                        elif self.party_mult_atk[ok1-1] < 0:
                            dano = dano - (0,3 * self.party_mult_atk[ok1-1] * dano)
                        dano_mitigado = int(dano / math.sqrt(atributos_defensor[4]*8))
                        if self.horda_mult_def[ok2-1] > 0:
                            dano_mitigado = dano + (0,3 * self.horda_mult_def[ok2-1] * dano)
                        elif self.horda_mult_def[ok2-1] < 0:
                            dano = dano - (0,3 * self.horda_mult_def[ok2-1] * dano)
                        dano = dano - dano_mitigado
                        if self.horda_elem_dano[ok2-1][0] > 0:
                            if self.horda_elem_dano[ok2-1][0] == 1:
                                dano = dano * 2
                                await canal.send(f"""**{nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                            elif self.horda_elem_dano[ok2-1][0] == 2:
                                dano = dano / 2
                                await canal.send(f"""**RESISTIU! {nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                            elif self.horda_elem_dano[ok2-1][0] == 3:
                                dano = 0
                                await canal.send(f"""**NULIFICOU! **{nome_horda}** nulificou todo o dano causado!""")
                            elif self.horda_elem_dano[ok2-1][0] == 4:
                                await canal.send(f"""**DRENOU! **{nome_horda}** se curou em **{dano}**!""")
                            elif self.horda_elem_dano[ok2-1][0] == 5:
                                await canal.send(f"""**REFLETIU! **{nome_horda}** refletiu **{dano}** de dano em **{nome_party}**!""")
                            else:
                                await canal.send(f"""**{nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                        elif fraquezas[0] == 1:
                            dano = dano * 2
                            await canal.send(f"""**{nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                        elif fraquezas[0] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                        elif fraquezas[0] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{nome_horda}** nulificou todo o dano causado!""")
                        elif fraquezas[0] == 4:
                            await canal.send(f"""**DRENOU! **{nome_horda}** se curou em **{dano}**!""")
                        elif fraquezas[0] == 5:
                            await canal.send(f"""**REFLETIU! **{nome_horda}** refletiu **{dano}** de dano em **{nome_party}**!""")
                        else:
                            if dado <= critico:
                                dano = dano * 2
                                await canal.send(f"""**CRÍTICO! {nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                            else:
                                await canal.send(f"""**{nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                    else:
                        await canal.send(f"""**{nome_party}** errou o ataque físico  em **{nome_horda}**""")
                else:
                    defensor_id = Database.personagem_id(self.horda[ok2-1][1])
                    d_persona_id = Database.persona_equipada(defensor_id)
                    equips_defensor = Database.itens_equipados(defensor_id)
                    armadura_defensor = equips_defensor[2]
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
                    valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.party_mult_acc[ok1-1]) - (10*self.horda_mult_evs[ok2-1])
                    await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                    dado = await Dado.rolagem_pronta(bot, canal, self.party[ok1-1], usuario, 1, 100)
                    critico = 10 + (self.party_mult_crit[ok1-1] * 10)
                    if dado <= valor_criterio:
                        valor_arma = Database.valor_item(meelee)
                        dano = int(20 + math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2]))
                        if self.party_mult_atk[ok1-1] > 0:
                            dano = dano + (0,3 * self.party_mult_atk[ok1-1] * dano)
                        elif self.party_mult_atk[ok1-1] < 0:
                            dano = dano - (0,3 * self.party_mult_atk[ok1-1] * dano)
                        if armadura_defensor == None:
                            valor_armadura = 0
                        else:
                            valor_armadura = Database.valor_item(armadura_defensor)
                        dano_mitigado = int(dano / math.sqrt((atributos_defensor[4]*8)+valor_armadura))
                        if self.horda_mult_def[ok2-1] > 0:
                            dano_mitigado = dano + (0,3 * self.horda_mult_def[ok2-1] * dano)
                        elif self.horda_mult_def[ok2-1] < 0:
                            dano = dano - (0,3 * self.horda_mult_def[ok2-1] * dano)
                        dano = dano - dano_mitigado
                        if self.horda_elem_dano[ok2-1][0] > 0:
                            if self.horda_elem_dano[ok2-1][0] == 1:
                                dano = dano * 2
                                await canal.send(f"""**{nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                            elif self.horda_elem_dano[ok2-1][0] == 2:
                                dano = dano / 2
                                await canal.send(f"""**RESISTIU! {nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                            elif self.horda_elem_dano[ok2-1][0] == 3:
                                dano = 0
                                await canal.send(f"""**NULIFICOU! **{nome_horda}** nulificou todo o dano causado!""")
                            elif self.horda_elem_dano[ok2-1][0] == 4:
                                await canal.send(f"""**DRENOU! **{nome_horda}** se curou em **{dano}**!""")
                            elif self.horda_elem_dano[ok2-1][0] == 5:
                                await canal.send(f"""**REFLETIU! **{nome_horda}** refletiu **{dano}** de dano em **{nome_party}**!""")
                            else:
                                await canal.send(f"""**{nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                        elif fraquezas[0] == 1:
                            dano = dano * 2
                            await canal.send(f"""**{nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                        elif fraquezas[0] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                        elif fraquezas[0] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{nome_horda}** nulificou todo o dano causado!""")
                        elif fraquezas[0] == 4:
                            await canal.send(f"""**DRENOU! **{nome_horda}** se curou em **{dano}**!""")
                        elif fraquezas[0] == 5:
                            await canal.send(f"""**REFLETIU! **{nome_horda}** refletiu **{dano}** de dano em **{nome_party}**!""")
                        else:
                            if dado <= critico:
                                dano = dano * 2
                                await canal.send(f"""**CRÍTICO! {nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                            else:
                                await canal.send(f"""**{nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                    else:
                        await ctx.send(f"""**{nome_party}** errou o ataque físico  em **{nome_horda}**""")
            elif ok == 2:
                canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
                embed = discord.Embed(
                    title=f"""Quem da horda atacará?""",
                    description=f"""Reaja com a opção desejada""",
                    colour=discord.Colour.blue()
                )
                emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
                for j in range(len(self.horda)):
                    embed.add_field(name=emojis_disc[j], value=self.horda[j][1], inline=False)
                embed_msg = await ctx.send(embed=embed)
                for i in range(len(self.horda)):
                    await embed_msg.add_reaction(emoji=emojis_raw[i])
                await embed_msg.add_reaction(emoji="❌")
                ok1 = 0
                while ok1 == 0:
                    reaction, user = await bot.wait_for('reaction_add', timeout=None)
                    if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                        ok1 = 1
                    if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                        ok1 = 2
                    if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                        ok1 = 3
                    if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                        ok1 = 4
                    if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                        ok1 = 5
                    if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                        ok1 = 6
                await embed_msg.delete()
                nome_horda = self.horda[ok1-1][1]
                embed = discord.Embed(
                    title=f"""Qual personagem da Party será atacado?""",
                    description=f"""Reaja com a opção desejada""",
                    colour=discord.Colour.blue()
                )
                emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
                for j in range(len(self.party)):
                    embed.add_field(name=emojis_disc[j], value=self.party[j], inline=False)
                embed_msg = await ctx.send(embed=embed)
                for i in range(len(self.party)):
                    await embed_msg.add_reaction(emoji=emojis_raw[i])
                await embed_msg.add_reaction(emoji="❌")
                ok2 = 0
                while ok2 == 0:
                    reaction, user = await bot.wait_for('reaction_add', timeout=None)
                    if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                        ok2 = 1
                    if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                        ok2 = 2
                    if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                        ok2 = 3
                    if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                        ok2 = 4
                    if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                        ok2 = 5
                    if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                        ok2 = 6
                await embed_msg.delete()
                nome_party = self.party[ok2-1]
                personagem_id = Database.personagem_id(self.party[ok2-1])
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
                if self.horda[ok1-1][0] == "s":
                    shadow_id = Database.shadow_id(self.horda[ok1-1][1])
                    atributos_atacante = Database.atributos_iniciais(shadow_id)
                    for i in range(len(atributos_atacante)):
                        atributos_atacante[i] = atributos_atacante[i][1]
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
                    valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.horda_mult_acc[ok1-1])- (10*self.party_mult_evs[ok2-1])
                    await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                    dado = await Dado.rolagem_pronta(bot, canal, "Mestre", "Axuáti#9639", 1, 100)
                    critico = 10 + (self.horda_mult_crit[ok1-1] * 10)
                    if dado <= valor_criterio:
                        dano = int(20 * math.sqrt(atributos_atacante[2]))
                        if self.horda_mult_atk[ok1-1] > 0:
                            dano = dano + (0,3 * self.horda_mult_atk[ok1-1] * dano)
                        elif self.horda_mult_atk[ok1-1] < 0:
                            dano = dano - (0,3 * self.horda_mult_atk[ok1-1] * dano)
                        if armadura == None:
                            valor_armadura = 0
                        else:
                            valor_armadura = Database.valor_item(armadura)
                        if armadura == None:
                            valor_armadura = 0
                        else:
                            valor_armadura = Database.valor_item(armadur)
                        dano_mitigado = int(dano / math.sqrt((atributos_defensor[4]*8) + valor_armadura))
                        if self.party_mult_def[ok2-1] > 0:
                            dano_mitigado = dano + (0,3 *self.party_mult_def[ok2-1] * dano)
                        elif self.party_mult_def[ok2-1] < 0:
                            dano = dano - (0,3 * self.party_mult_def[ok2-1] * dano)
                        dano = dano - dano_mitigado
                        if self.party_elem_dano[ok2-1][0] > 0:
                            if self.party_elem_dano[ok2-1][0] == 1:
                                dano = dano * 2
                                await canal.send(f"""**{nome_horda}** causou **{dano}** de dano e derrubou **{nome_party}**!""")
                            elif self.party_elem_dano[ok2-1][0] == 2:
                                dano = dano / 2
                                await canal.send(f"""**RESISTIU! {nome_horda}** causou **{dano}** de dano em **{nome_party}**!""")
                            elif self.party_elem_dano[ok2-1][0] == 3:
                                dano = 0
                                await canal.send(f"""**NULIFICOU! **{nome_party}** nulificou todo o dano causado!""")
                            elif self.party_elem_dano[ok2-1][0] == 4:
                                await canal.send(f"""**DRENOU! **{nome_party}** se curou em **{dano}**!""")
                            elif self.party_elem_dano[ok2-1][0] == 5:
                                await canal.send(f"""**REFLETIU! **{nome_party}** refletiu **{dano}** de dano em **{nome_horda}**!""")
                            else:
                                await canal.send(f"""**{nome_horda}** causou **{dano}** de dano em **{nome_party}**!""")
                        elif fraquezas[0] == 1:
                            dano = dano * 2
                            await canal.send(f"""**{nome_horda}** causou **{dano}** de dano e derrubou **{nome_party}**!""")
                        elif fraquezas[0] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {nome_horda}** causou **{dano}** de dano em **{nome_party}**!""")
                        elif fraquezas[0] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{nome_party}** nulificou todo o dano causado!""")
                        elif fraquezas[0] == 4:
                            await canal.send(f"""**DRENOU! **{nome_party}** se curou em **{dano}**!""")
                        elif fraquezas[0] == 5:
                            await canal.send(f"""**REFLETIU! **{nome_party}** refletiu **{dano}** de dano em **{nome_horda}**!""")
                        else:
                            if dado <= critico:
                                dano = dano * 2
                                await canal.send(f"""**CRÍTICO! {nome_horda}** causou **{dano}** de dano e derrubou **{nome_party}**!""")
                            else:
                                await canal.send(f"""**{nome_horda}** causou **{dano}** de dano em **{nome_party}**!""")
                    else:
                        await canal.send(f"""**{nome_horda}** errou o ataque físico  em **{nome_party}**""")
                else:
                    atacante_id = Database.personagem_id(self.horda[ok1-1])
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
                    valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.horda_mult_acc[ok1-1])- (10*self.party_mult_evs[ok2-1])
                    await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                    dado = await Dado.rolagem_pronta(bot, canal, "Mestre", "Axuáti#9639", 1, 100)
                    critico = 10 + (self.horda_mult_crit[ok1-1] * 10)
                    if dado <= valor_criterio:
                        valor_arma = Database.valor_item(meelee_atacante)
                        dano = int(20 + math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2]))
                        if self.horda_mult_atk[ok1-1] > 0:
                            dano = dano + (0,3 * self.horda_mult_atk[ok1-1] * dano)
                        elif self.horda_mult_atk[ok1-1] < 0:
                            dano = dano - (0,3 * self.horda_mult_atk[ok1-1] * dano)
                        if armadura == None:
                            valor_armadura = 0
                        else:
                            valor_armadura = Database.valor_item(armadura)
                        dano_mitigado = int(math.sqrt((atributos_defensor[4]*8)+valor_armadura))
                        if self.party_mult_def[ok2-1] > 0:
                            dano_mitigado = dano + (0,3 * self.party_mult_def[ok2-1] * dano)
                        elif self.party_mult_def[ok2-1] < 0:
                            dano = dano - (0,3 * self.party_mult_def[ok2-1] * dano)
                        dano = dano - dano_mitigado
                        if self.party_elem_dano[ok2-1][0] > 0:
                            if self.party_elem_dano[ok2-1][0] == 1:
                                dano = dano * 2
                                await canal.send(f"""**FRACO! {nome_horda}** causou **{dano}** de dano e derrubou **{nome_party}**!""")
                            elif self.party_elem_dano[ok2-1][0] == 2:
                                dano = dano / 2
                                await canal.send(f"""**RESISTIU! {nome_horda}** causou **{dano}** de dano em **{nome_party}**!""")
                            elif self.party_elem_dano[ok2-1][0] == 3:
                                dano = 0
                                await canal.send(f"""**NULIFICOU! **{nome_party}** nulificou todo o dano causado!""")
                            elif self.party_elem_dano[ok2-1][0] == 4:
                                await canal.send(f"""**DRENOU! **{nome_party}** se curou em **{dano}**!""")
                            elif self.party_elem_dano[ok2-1][0] == 5:
                                await canal.send(f"""**REFLETIU! **{nome_party}** refletiu **{dano}** de dano em **{nome_horda}**!""")
                            else:
                                await canal.send(f"""**{nome_horda}** causou **{dano}** de dano em **{nome_party}**!""")
                        elif fraquezas[0] == 1:
                            dano = dano * 2
                            await canal.send(f"""**FRACO! {nome_horda}** causou **{dano}** de dano e derrubou **{nome_party}**!""")
                        elif fraquezas[0] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {nome_horda}** causou **{dano}** de dano em **{nome_party}**!""")
                        elif fraquezas[0] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{nome_party}** nulificou todo o dano causado!""")
                        elif fraquezas[0] == 4:
                            await canal.send(f"""**DRENOU! **{nome_party}** se curou em **{dano}**!""")
                        elif fraquezas[0] == 5:
                            await canal.send(f"""**REFLETIU! **{nome_party}** refletiu **{dano}** de dano em **{nome_horda}**!""")
                        else:
                            if dado <= critico:
                                dano = dano * 2
                                await canal.send(f"""**CRÍTICO! {nome_horda}** causou **{dano}** de dano e derrubou **{nome_party}**!""")
                            else:
                                await canal.send(f"""**{nome_horda}** causou **{dano}** de dano em **{nome_party}**!""")
                    else:
                        await canal.send(f"""**{nome_horda}** errou o ataque físico  em **{nome_party}**""")
            else:
                await ctx.send("Ataque físico cancelado.")
        except:
            await ctx.send("Ataque cancelado ou Algo está incorreto.")

    @commands.command(name='tiro')
    async def tiro(self, ctx):
        try:
            embed = discord.Embed(
                title=f"""Qual personagem da Party irá atacar?""",
                description=f"""Reaja com a opção desejada""",
                colour=discord.Colour.blue()
            )
            emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
            for j in range(len(self.party)):
                embed.add_field(name=emojis_disc[j], value=self.party[j], inline=False)
            embed_msg = await ctx.send(embed=embed)
            for i in range(len(self.party)):
                await embed_msg.add_reaction(emoji=emojis_raw[i])
            await embed_msg.add_reaction(emoji="❌")
            ok1 = 0
            while ok1 == 0:
                reaction, user = await bot.wait_for('reaction_add', timeout=None)
                if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                    ok1 = 1
                if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                    ok1 = 2
                if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                    ok1 = 3
                if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                    ok1 = 4
                if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                    ok1 = 5
                if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                    ok1 = 6
            await embed_msg.delete()
            nome_party = self.party[ok1-1]
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[ok1-1]))
            personagem_id = Database.personagem_id(self.party[ok1-1])
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
            embed = discord.Embed(
                title=f"""Quem da horda será atacado?""",
                description=f"""Reaja com a opção desejada""",
                colour=discord.Colour.blue()
            )
            emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
            for j in range(len(self.horda)):
                embed.add_field(name=emojis_disc[j], value=self.horda[j][1], inline=False)
            embed_msg = await ctx.send(embed=embed)
            for i in range(len(self.horda)):
                await embed_msg.add_reaction(emoji=emojis_raw[i])
            await embed_msg.add_reaction(emoji="❌")
            ok2 = 0
            while ok2 == 0:
                reaction, user = await bot.wait_for('reaction_add', timeout=None)
                if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                    ok2 = 1
                if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                    ok2 = 2
                if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                    ok2 = 3
                if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                    ok2 = 4
                if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                    ok2 = 5
                if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                    ok2 = 6
            await embed_msg.delete()
            nome_horda = self.horda[ok2-1][1]
            if self.horda[ok2-1][0] == "s":
                shadow_id = Database.shadow_id(self.horda[ok2-1][1])
                fraquezas = Database.fraquezas(shadow_id)
                atributos_defensor = Database.atributos_iniciais(shadow_id)
                for i in range(len(atributos_defensor)):
                    atributos_defensor[i] = atributos_defensor[i][1]
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
                valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.party_mult_acc[ok1-1]) - (10*horda_mult_evs[ok2-1])
                await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                critico = 10 + (self.party_mult_crit[ok1-1] * 10)
                dado = await Dado.rolagem_pronta(bot, canal, self.party[ok1-1], usuario, 1, 100)
                if dado <= valor_criterio:
                    valor_arma = Database.valor_item(ranged)
                    dano = int(math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2]))
                    if self.party_mult_atk[ok1-1] > 0:
                        dano = dano + (0,3 * self.party_mult_atk[ok1-1] * dano)
                    elif self.party_mult_atk[ok1-1] < 0:
                        dano = dano - (0,3 * self.party_mult_atk[ok1-1] * dano)
                    dano_mitigado = int(math.sqrt(atributos_defensor[4]*8))
                    if self.horda_mult_def[ok2-1] > 0:
                        dano_mitigado = dano + (0,3 * self.horda_mult_def[ok2-1] * dano)
                    elif self.horda_mult_def[ok2-1] < 0:
                        dano = dano - (0,3 * self.horda_mult_def[ok2-1] * dano)
                    dano = dano - dano_mitigado
                    if self.horda_elem_dano[ok2-1][0] > 0:
                        if self.horda_elem_dano[ok2-1][1] == 1:
                            dano = dano * 2
                            await canal.send(f"""**FRACO! {nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                        elif self.horda_elem_dano[ok2-1][1] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                        elif self.horda_elem_dano[ok2-1][1] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{nome_horda}** nulificou todo o dano causado!""")
                        elif self.horda_elem_dano[ok2-1][1] == 4:
                            await canal.send(f"""**DRENOU! **{nome_horda}** se curou em **{dano}**!""")
                        elif self.horda_elem_dano[ok2-1][1] == 5:
                            await canal.send(f"""**REFLETIU! **{nome_horda}** refletiu **{dano}** de dano em **{nome_party}**!""")
                        else:
                            await canal.send(f"""**{nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                    elif fraquezas[0] == 1:
                        dano = dano * 2
                        await canal.send(f"""**FRACO! {nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                    elif fraquezas[0] == 2:
                        dano = dano / 2
                        await canal.send(f"""**RESISTIU! {nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                    elif fraquezas[0] == 3:
                        dano = 0
                        await canal.send(f"""**NULIFICOU! **{nome_horda}** nulificou todo o dano causado!""")
                    elif fraquezas[0] == 4:
                        await canal.send(f"""**DRENOU! **{nome_horda}** se curou em **{dano}**!""")
                    elif fraquezas[0] == 5:
                        await canal.send(f"""**REFLETIU! **{nome_horda}** refletiu **{dano}** de dano em **{nome_party}**!""")
                    else:
                        if dado <= critico:
                            dano = dano * 2
                            await canal.send(f"""**CRÍTICO! {nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                        else:
                            await canal.send(f"""**{nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                else:
                    await canal.send(f"""**{nome_party}** errou o tiro em **{nome_horda}**""")
            else:
                defensor_id = Database.personagem_id(self.horda[ok2-1])
                d_persona_id = Database.persona_equipada(defensor_id)
                equips_defensor = Database.itens_equipados(defensor_id)
                armadura_defensor = equips_defensor[2]
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
                valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.party_mult_acc[ok1-1]) - (10*self.horda_mult_evs[ok2-1])
                await canal.send(f"""Você precisa tirar um valor menor que **{valor_criterio}** no dado""")
                dado = await Dado.rolagem_pronta(bot, canal, self.party[ok1-1], usuario, 1, 100)
                critico = 10 + (self.party_mult_crit[ok1-1] * 10)
                if dado <= valor_criterio:
                    valor_arma = Database.valor_item(ranged)
                    dano = int(math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2]))
                    if self.party_mult_atk[ok1-1] > 0:
                        dano = dano + (0,3 * self.party_mult_atk[ok1-1] * dano)
                    elif self.party_mult_atk[ok1-1] < 0:
                        dano = dano - (0,3 * self.party_mult_atk[ok1-1] * dano)
                    if armadura_defensor == None:
                        valor_armadura = 0
                    else:
                        valor_armadura = Database.valor_item(armadura_defensor)
                    dano_mitigado = int(dano / math.sqrt((atributos_defensor[4]*8)+valor_armadura))
                    if self.horda_mult_def[ok2-1] > 0:
                        dano_mitigado = dano + (0,3 * self.horda_mult_def[ok2-1] * dano)
                    elif self.horda_mult_def[ok2-1] < 0:
                        dano = dano - (0,3 * self.horda_mult_def[ok2-1] * dano)
                    dano = dano - dano_mitigado
                    if self.horda_elem_dano[ok2-1][1] > 0:
                        if self.horda_elem_dano[ok2-1][1] == 1:
                            dano = dano * 2
                            await canal.send(f"""**FRACO! {nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                        elif self.horda_elem_dano[ok2-1][1] == 2:
                            dano = dano / 2
                            await canal.send(f"""**RESISTIU! {nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                        elif self.horda_elem_dano[ok2-1][1] == 3:
                            dano = 0
                            await canal.send(f"""**NULIFICOU! **{nome_horda}** nulificou todo o dano causado!""")
                        elif self.horda_elem_dano[ok2-1][1] == 4:
                            await canal.send(f"""**DRENOU! **{nome_horda}** se curou em **{dano}**!""")
                        elif self.horda_elem_dano[ok2-1][1] == 5:
                            await canal.send(f"""**REFLETIU! **{nome_horda}** refletiu **{dano}** de dano em **{nome_party}**!""")
                        else:
                            await canal.send(f"""**{nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                    elif fraquezas[1] == 1:
                        dano = dano * 2
                        await canal.send(f"""**FRACO! {nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                    elif fraquezas[1] == 2:
                        dano = dano / 2
                        await canal.send(f"""**RESISTIU! {nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                    elif fraquezas[1] == 3:
                        dano = 0
                        await canal.send(f"""**NULIFICOU! **{nome_horda}** nulificou todo o dano causado!""")
                    elif fraquezas[1] == 4:
                        await canal.send(f"""**DRENOU! **{nome_horda}** se curou em **{dano}**!""")
                    elif fraquezas[1] == 5:
                        await canal.send(f"""**REFLETIU! **{nome_horda}** refletiu **{dano}** de dano em **{nome_party}**!""")
                    else:
                        if dado <= critico:
                            dano = dano * 2
                            await canal.send(f"""**CRÍTICO! {nome_party}** causou **{dano}** de dano e derrubou **{nome_horda}**!""")
                        else:
                            await canal.send(f"""**{nome_party}** causou **{dano}** de dano em **{nome_horda}**!""")
                else:
                    await canal.send(f"""**{nome_party}** errou o tiro em **{nome_horda}**""")
        except:
            await ctx.send("Algo está incorreto.")

    @commands.command(name='habilidade')
    async def habilidade(self, ctx, bonus=0.0, *habilidade):
        try:
            nome = ""
            for palavra in habilidade:
                nome += palavra + " "
            nome = nome[:-1]
            skill_id = Database.skill_id(nome)
            if skill_id != False:
                embed = discord.Embed(
                    title=f"""Quem vai atacar?""",
                    description=f"""Reaja com a opção desejada""",
                    colour=discord.Colour.blue()
                )
                embed.add_field(name=":one:", value="Party", inline=False)
                embed.add_field(name=":two:", value="Horda", inline=False)
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
                nome_skill = Database.nome_skill(skill_id)
                vezes = Database.skill_vezes(skill_id)
                if ok == 1:
                    embed = discord.Embed(
                        title=f"""Qual personagem da Party irá atacar?""",
                        description=f"""Reaja com a opção desejada""",
                        colour=discord.Colour.blue()
                    )
                    emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                    emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
                    for j in range(len(self.party)):
                        embed.add_field(name=emojis_disc[j], value=self.party[j], inline=False)
                    embed_msg = await ctx.send(embed=embed)
                    for i in range(len(self.party)):
                        await embed_msg.add_reaction(emoji=emojis_raw[i])
                    await embed_msg.add_reaction(emoji="❌")
                    ok1 = 0
                    while ok1 == 0:
                        reaction, user = await bot.wait_for('reaction_add', timeout=None)
                        if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                            ok1 = 1
                        if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                            ok1 = 2
                        if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                            ok1 = 3
                        if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                            ok1 = 4
                        if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                            ok1 = 5
                        if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                            ok1 = 6
                    await embed_msg.delete()
                    canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[ok1-1]))
                    codigo1 = ok1
                    personagem_id = Database.personagem_id(self.party[codigo1-1])
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
                        embed = discord.Embed(
                            title=f"""Quem/Quais da horda será atacado?""",
                            description=f"""Reaja com a opções desejadas e confirme""",
                            colour=discord.Colour.blue()
                        )
                        emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                        emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
                        for j in range(len(self.horda)):
                            embed.add_field(name=emojis_disc[j], value=self.horda[j][1], inline=False)
                        embed_msg = await ctx.send(embed=embed)
                        for i in range(len(self.horda)):
                            await embed_msg.add_reaction(emoji=emojis_raw[i])
                        await embed_msg.add_reaction(emoji="✅")
                        await embed_msg.add_reaction(emoji="❌")
                        ok2 = 0
                        defensores = []
                        while ok2 == 0:
                            reaction, user = await bot.wait_for('reaction_add', timeout=None)
                            if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                                defensores.append(1)
                            if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                                defensores.append(2)
                            if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                                defensores.append(3)
                            if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                                defensores.append(4)
                            if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                                defensores.append(5)
                            if str(reaction.emoji) == "✅" and str(user) != "Persona Bot#0708":
                                ok2 = 6
                            if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                                ok2 = 7
                        await embed_msg.delete()
                        if ok2 == 6 and defensores != []:
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
                            valores = []
                            for defensor in defensores:
                                if self.horda[defensor-1][0] == "s":
                                    shadow_id = Database.shadow_id(self.horda[defensor-1][1])
                                    fraquezas = Database.fraquezas(shadow_id)
                                    atributos_defensor = Database.atributos_iniciais(shadow_id)
                                    for i in range(len(atributos_defensor)):
                                        atributos_defensor[i] = atributos_defensor[i][1]
                                else:
                                    defensor_id = Database.personagem_id(self.party[defensor-1])
                                    d_persona_id = Database.persona_equipada(defensor_id)
                                    equips_defensor = Database.itens_equipados(defensor_id)
                                    armadura_defensor = equips_defensor[2]
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
                                valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.party_mult_acc[ok1-1]) - (10*self.horda_mult_evs[defensor-1])
                                valores.append(valor_criterio)
                            texto = ""
                            for valor in valores:
                                texto += str(valor_criterio) + ", "
                            texto = texto[:-2]
                            await canal.send(f"""Você precisa tirar valor(es) menor(es) que **{texto}** no dado""")
                            dados = []
                            for i in range(vezes):   
                                dado = await Dado.rolagem_pronta(bot, canal, self.party[codigo1-1], usuario, 1, 100)
                                dados.append(dado)
                            for defensor in defensores:
                                codigo2 = defensor
                                if self.horda[codigo2-1][0] == "s":
                                    shadow_id = Database.shadow_id(self.horda[codigo2-1][1])
                                    fraquezas = Database.fraquezas(shadow_id)
                                    atributos_defensor = Database.atributos_iniciais(shadow_id)
                                    for i in range(len(atributos_defensor)):
                                        atributos_defensor[i] = atributos_defensor[i][1]
                                    valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.party_mult_acc[codigo1-1]) - (10*self.horda_mult_evs[codigo2-1])
                                    for i in range(len(dados)):   
                                        dado = dados[i]
                                        if dado <= valor_criterio:
                                            if elemento < 3:
                                                dano = int((intensidade * 25) * math.sqrt(atributos_atacante[2]))
                                            else:
                                                dano = int((intensidade * 25) + ((intensidade * 25) * (atributos_atacante[3]/30)))
                                            if self.party_mult_atk[codigo1-1] > 0:
                                                dano = dano + (0,3 * self.party_mult_atk[codigo1-1] * dano)
                                            elif self.party_mult_atk[codigo1-1] < 0:
                                                dano = dano - (0,3 * self.party_mult_atk[codigo1-1] * dano)
                                            dano_mitigado = int(math.sqrt(atributos_defensor[4]*8))
                                            if self.horda_mult_def[codigo2-1] > 0:
                                                dano_mitigado = dano + (0,3 * self.horda_mult_def[codigo2-1] * dano)
                                            elif self.horda_mult_def[codigo2-1] < 0:
                                                dano = dano - (0,3 * self.horda_mult_def[codigo2-1] * dano)
                                            dano = int((1+bonus) * dano)
                                            dano = dano - dano_mitigado
                                            if self.horda_elem_dano[codigo2-1][elemento-1] > 0:
                                                if self.horda_elem_dano[codigo2-1][elemento-1] == 1:
                                                    dano = dano * 2
                                                    await canal.send(f"""**FRACO! {self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{self.horda[codigo2-1][1]}**!""")
                                                elif self.horda_elem_dano[codigo2-1][elemento-1] == 2:
                                                    dano = dano / 2
                                                    await canal.send(f"""**RESISTIU! {self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo2-1][1]}**!""")
                                                elif self.horda_elem_dano[codigo2-1][elemento-1] == 3:
                                                    dano = 0
                                                    await canal.send(f"""**NULIFICOU! **{self.horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                                                elif self.horda_elem_dano[codigo2-1][elemento-1] == 4:
                                                    await canal.send(f"""**DRENOU! **{self.horda[codigo2-1][1]}** se curou em **{dano}**!""")
                                                elif self.horda_elem_dano[codigo2-1][elemento-1] == 5:
                                                    await canal.send(f"""**REFLETIU! **{self.horda[codigo2-1][1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{self.party[codigo1-1]}**!""")
                                                else:
                                                    await canal.send(f"""**{self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo2-1][1]}**!""")
                                            elif fraquezas[elemento-1] == 1:
                                                dano = dano * 2
                                                await canal.send(f"""**FRACO! {self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{self.horda[codigo2-1][1]}**!""")
                                            elif fraquezas[elemento-1] == 2:
                                                dano = dano / 2
                                                await canal.send(f"""**RESISTIU! {self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo2-1][1]}**!""")
                                            elif fraquezas[elemento-1] == 3:
                                                dano = 0
                                                await canal.send(f"""**NULIFICOU! **{self.horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                                            elif fraquezas[elemento-1] == 4:
                                                await canal.send(f"""**DRENOU! **{self.horda[codigo2-1][1]}** se curou em **{dano}**!""")
                                            elif fraquezas[elemento-1] == 5:
                                                await canal.send(f"""**REFLETIU! **{self.horda[codigo2-1][1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{self.party[codigo1-1]}**!""")
                                            else:
                                                await canal.send(f"""**{self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo2-1][1]}**!""")
                                        else:
                                            await canal.send(f"""**{self.party[codigo1-1]}** errou a habilidade **{nome_skill}** em **{self.horda[codigo2-1][1]}**""")
                                else:
                                    defensor_id = Database.personagem_id(self.party[codigo2-1])
                                    d_persona_id = Database.persona_equipada(defensor_id)
                                    equips_defensor = Database.itens_equipados(defensor_id)
                                    armadura_defensor = equips_defensor[2]
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
                                    valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.party_mult_acc[codigo1-1]) - (10*self.horda_mult_evs[codigo2-1])
                                    for i in range(vezes):  
                                        dado = await Dado.rolagem_pronta(bot, canal, self.party[codigo1-1], usuario, 1, 100)
                                        if dado <= valor_criterio:
                                            if elemento < 3:
                                                dano = int((intensidade * 25) * math.sqrt(atributos_atacante[2]))
                                            else:
                                                dano = int((intensidade * 25) + ((intensidade * 25) * (atributos_atacante[3]/30)))
                                            if self.party_mult_atk[codigo1-1] > 0:
                                                dano = dano + (0,3 * self.party_mult_atk[codigo1-1] * dano)
                                            elif self.party_mult_atk[codigo1-1] < 0:
                                                dano = dano - (0,3 * self.party_mult_atk[codigo1-1] * dano)
                                            valor_armadura = Database.valor_item(armadura_defensor)
                                            dano = int((1+bonus) * dano)
                                            dano_mitigado = int(math.sqrt((atributos_defensor[4]*8)+valor_armadura))
                                            if self.horda_mult_def[codigo2-1] > 0:
                                                dano_mitigado = dano + (0,3 * self.horda_mult_def[codigo2-1] * dano)
                                            elif self.horda_mult_def[codigo2-1] < 0:
                                                dano = dano - (0,3 * self.horda_mult_def[codigo2-1] * dano)
                                            dano = dano - dano_mitigado
                                            if self.horda_elem_dano[codigo2-1][elemento-1] > 0:
                                                if self.horda_elem_dano[codigo2-1][elemento-1] == 1:
                                                    dano = dano * 2
                                                    await canal.send(f"""**FRACO! {self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{self.horda[codigo2-1][1]}**!""")
                                                elif self.horda_elem_dano[codigo2-1][elemento-1] == 2:
                                                    dano = dano / 2
                                                    await canal.send(f"""**RESISTIU! {self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo2-1][1]}**!""")
                                                elif self.horda_elem_dano[codigo2-1][elemento-1] == 3:
                                                    dano = 0
                                                    await canal.send(f"""**NULIFICOU! **{self.horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                                                elif self.horda_elem_dano[codigo2-1][elemento-1] == 4:
                                                    await canal.send(f"""**DRENOU! **{self.horda[codigo2-1][1]}** se curou em **{dano}**!""")
                                                elif self.horda_elem_dano[codigo2-1][elemento-1] == 5:
                                                    await canal.send(f"""**REFLETIU! **{self.horda[codigo2-1][1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{self.party[codigo1-1]}**!""")
                                                else:
                                                    await canal.send(f"""**{self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo2-1][1]}**!""")
                                            elif fraquezas[elemento-1] == 1:
                                                dano = dano * 2
                                                await canal.send(f"""**FRACO! {self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{self.horda[codigo2-1][1]}**!""")
                                            elif fraquezas[elemento-1] == 2:
                                                dano = dano / 2
                                                await canal.send(f"""**RESISTIU! {self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo2-1][1]}**!""")
                                            elif fraquezas[elemento-1] == 3:
                                                dano = 0
                                                await canal.send(f"""**NULIFICOU! **{self.horda[codigo2-1][1]}** nulificou todo o dano causado!""")
                                            elif fraquezas[elemento-1] == 4:
                                                await canal.send(f"""**DRENOU! **{self.horda[codigo2-1][1]}** se curou em **{dano}**!""")
                                            elif fraquezas[elemento-1] == 5:
                                                await canal.send(f"""**REFLETIU! **{self.horda[codigo2-1][1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{self.party[codigo1-1]}**!""")
                                            else:
                                                await canal.send(f"""**{self.party[codigo1-1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo2-1][1]}**!""")
                                        else:
                                            await canal.send(f"""**{self.party[codigo1-1]}** errou a habilidade **{nome_skill}** em **{self.horda[codigo2-1][1]}**""")
                        else:
                            await ctx.send("Habilidade cancelada.")
                elif ok == 2:
                    embed = discord.Embed(
                        title=f"""Qual personagem da Horda irá atacar?""",
                        description=f"""Reaja com a opção desejada""",
                        colour=discord.Colour.blue()
                    )
                    emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                    emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
                    for j in range(len(self.horda)):
                        embed.add_field(name=emojis_disc[j], value=horda[j][1], inline=False)
                    embed_msg = await ctx.send(embed=embed)
                    for i in range(len(self.horda)):
                        await embed_msg.add_reaction(emoji=emojis_raw[i])
                    await embed_msg.add_reaction(emoji="❌")
                    ok1 = 0
                    while ok1 == 0:
                        reaction, user = await bot.wait_for('reaction_add', timeout=None)
                        if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                            ok1 = 1
                        if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                            ok1 = 2
                        if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                            ok1 = 3
                        if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                            ok1 = 4
                        if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                            ok1 = 5
                        if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                            ok1 = 6
                    await embed_msg.delete()
                    codigo1 = ok1
                    canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
                    if self.horda[codigo1-1][0] == "s":
                        shadow_id = Database.shadow_id(self.horda[codigo1-1][1])
                        atributos_atacante = Database.atributos_iniciais(shadow_id)
                        nivel = Database.nivel_persona(shadow_id)
                        skills = Database.skills_shadow(shadow_id, nivel)
                        for i in range(len(atributos_atacante)):
                            atributos_atacante[i] = atributos_atacante[i][1]
                    else:
                        personagem_id = Database.personagem_id(self.horda[codigo1-1][1])
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
                        embed = discord.Embed(
                            title=f"""Quem/Quais da Party será atacado?""",
                            description=f"""Reaja com a opções desejadas e confirme""",
                            colour=discord.Colour.blue()
                        )
                        emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                        emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
                        for j in range(len(self.party)):
                            embed.add_field(name=emojis_disc[j], value=self.party[j], inline=False)
                        embed_msg = await ctx.send(embed=embed)
                        for i in range(len(self.party)):
                            await embed_msg.add_reaction(emoji=emojis_raw[i])
                        await embed_msg.add_reaction(emoji="✅")
                        await embed_msg.add_reaction(emoji="❌")
                        ok2 = 0
                        defensores = []
                        while ok2 == 0:
                            reaction, user = await bot.wait_for('reaction_add', timeout=None)
                            if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                                defensores.append(1)
                            if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                                defensores.append(2)
                            if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                                defensores.append(3)
                            if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                                defensores.append(4)
                            if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                                defensores.append(5)
                            if str(reaction.emoji) == "✅" and str(user) != "Persona Bot#0708":
                                ok2 = 6
                            if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                                ok2 = 7
                        await embed_msg.delete()
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
                        valores = []
                        for defensor in defensores:
                            defensor_id = Database.personagem_id(self.party[defensor-1])
                            d_persona_id = Database.persona_equipada(defensor)
                            equips_defensor = Database.itens_equipados(defensor_id)
                            armadura_defensor = equips_defensor[2]
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
                            valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.horda_mult_acc[ok1-1]) - (10*self.party_mult_evs[defensor-1])
                            valores.append(valor_criterio)
                        texto = ""
                        for valor in valores:
                            texto += str(valor_criterio) + ", "
                        texto = texto[:-2]
                        await canal.send(f"""Você precisa tirar valor(es) menor(es) que **{texto}** no dado""")
                        dados = []
                        for i in range(vezes):   
                            dado = await Dado.rolagem_pronta(bot, canal, self.horda[codigo1-1][1], "Axuáti#9639", 1, 100)
                            dados.append(dado)
                        for defensor in defensores:
                            codigo2 = defensor
                            personagem_id = Database.personagem_id(self.party[codigo2-1])
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
                            valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.horda_mult_acc[codigo1-1])- (10*self.party_mult_evs[codigo1-1])
                            for i in range(len(dados)):     
                                dado = dados[i]
                                if dado <= valor_criterio:
                                    if elemento < 3:
                                        dano = int((intensidade * 25) * math.sqrt(atributos_atacante[2]))
                                    else:
                                        dano = int((intensidade * 25) + ((intensidade * 25) * (atributos_atacante[3]/30)))
                                    if self.horda_mult_atk[codigo1-1] > 0:
                                        dano = dano + (0,3 * self.horda_mult_atk[codigo1-1] * dano)
                                    elif self.horda_mult_atk[codigo1-1] < 0:
                                        dano = dano - (0,3 * self.horda_mult_atk[codigo1-1] * dano)
                                    valor_armadura = Database.valor_item(armadura)
                                    dano_mitigado = int(math.sqrt((atributos_defensor[4]*8) + valor_armadura))
                                    if self.party_mult_def[codigo2-1] > 0:
                                        dano_mitigado = dano + (0,3 * self.party_mult_def[codigo2-1] * dano)
                                    elif self.party_mult_def[codigo2-1] < 0:
                                        dano = dano - (0,3 * self.party_mult_def[codigo2-1] * dano)
                                    dano = int((1+bonus) * dano)
                                    dano = dano - dano_mitigado
                                    if self.party_elem_dano[codigo2-1][elemento-1] > 0:
                                        if self.party_elem_dano[codigo2-1][elemento-1] == 1:
                                            dano = dano * 2
                                            await canal.send(f"""**FRACO! {self.horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{self.party[codigo2-1][1]}**!""")
                                        elif self.party_elem_dano[codigo2-1][elemento-1] == 2:
                                            dano = dano / 2
                                            await canal.send(f"""**RESISTIU! {self.horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.party[codigo2-1]}**!""")
                                        elif self.party_elem_dano[codigo2-1][elemento-1] == 3:
                                            dano = 0
                                            await canal.send(f"""**NULIFICOU! **{self.party[codigo2-1]}** nulificou todo o dano causado!""")
                                        elif self.party_elem_dano[codigo2-1][elemento-1] == 4:
                                            await canal.send(f"""**DRENOU! **{self.party[codigo2-1]}** se curou em **{dano}**!""")
                                        elif self.party_elem_dano[codigo2-1][elemento-1] == 5:
                                            await canal.send(f"""**REFLETIU! **{self.party[codigo2-1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo1-1][1]}**!""")
                                        else:
                                            await canal.send(f"""**{self.horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.party[codigo2-1]}**!""")
                                    elif fraquezas[elemento-1] == 1:
                                        dano = dano * 2
                                        await canal.send(f"""**FRACO! {self.horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** e derrubou **{self.party[codigo2-1]}**!""")
                                    elif fraquezas[elemento-1] == 2:
                                        dano = dano / 2
                                        await canal.send(f"""**RESISTIU! {self.horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.party[codigo2-1]}**!""")
                                    elif fraquezas[elemento-1] == 3:
                                        dano = 0
                                        await canal.send(f"""**NULIFICOU! **{self.party[codigo2-1]}** nulificou todo o dano causado!""")
                                    elif fraquezas[elemento-1] == 4:
                                        await canal.send(f"""**DRENOU! **{self.party[codigo2-1]}** se curou em **{dano}**!""")
                                    elif fraquezas[elemento-1] == 5:
                                        await canal.send(f"""**REFLETIU! **{self.party[codigo2-1]}** refletiu **{dano}** de dano de **{nome_elemento}** em **{self.horda[codigo1-1][1]}**!""")
                                    else:
                                        await canal.send(f"""**{self.horda[codigo1-1][1]}** causou **{dano}** de dano de **{nome_elemento}** em **{self.party[codigo2-1]}**!""")
                                else:
                                    await canal.send(f"""**{self.horda[codigo1-1][1]}** errou a habilidade **{nome_skill}** em **{self.party[codigo2-1]}**""")
                else:
                    await ctx.send("Habilidade cancelada.")
        except:
            await ctx.send("Algo está incorreto.")

    @commands.command(name='lider')
    async def lider(self, ctx, personagem):
        canal = self.bot.get_channel(Canal.carregar_canal_grupo())
        if self.party != []:
            for i in range(len(self.party)):
                if self.party[i] == personagem:
                    self.party.insert(0, mylist.pop(i))
                    await canal.send(f"""**{personagem}** foi denominado o líder do grupo.""")
                    break
    
    @commands.command(name='marcador')
    async def marcador(self, ctx, tipo_marcador, tipo_grupo, codigo, quant):
        try:
            quant = int(quant)
            codigo = int(codigo)
            if tipo_grupo == "party":
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[codigo-1]))
            elif tipo_grupo == "horda":
                canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
            if tipo_marcador == "atk":
                if tipo_grupo == "party":
                    self.party_mult_atk[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve seu ataque aumentado em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve seu ataque diminuido em {quant}.""")
                else:
                    self.horda_mult_atk[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve seu ataque aumentado em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve seu ataque diminuido em {quant}.""")
            elif tipo_marcador == "def":
                if tipo_grupo == "party":
                    self.party_mult_def[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve sua defesa aumentada em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve sua defesa diminuida em {quant}.""")
                else:
                    self.horda_mult_atk[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve sua defesa aumentada em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve sua defesa diminuida em {quant}.""")
            elif tipo_marcador == "acc":
                if tipo_grupo == "party":
                    self.party_mult_acc[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve sua acurácia aumentada em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve sua acurácia diminuida em {quant}.""")
                else:
                    self.horda_mult_acc[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve sua acurácia aumentada em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve sua acurácia diminuida em {quant}.""")
            elif marcador == "evs":
                if tipo_grupo == "party":
                    self.party_mult_evs[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve sua evasão aumentada em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve sua evasão diminuida em {quant}.""")
                else:
                    self.horda_mult_evs[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve sua evasão aumentada em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve sua evasão diminuida em {quant}.""")
            else:
                if tipo_grupo == "party":
                    self.party_mult_crit[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve sua taxa de acerto crítico aumentada em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.party[codigo-1]}** teve sua taxa de acerto crítico diminuida em {quant}.""")
                else:
                    self.horda_mult_crit[codigo-1] += quant
                    if quant > 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve sua taxa de acerto crítico aumentada em {quant}.""")
                    elif quant < 0:
                        await canal.send(f"""**{self.horda[codigo-1][1]}** teve sua taxa de acerto crítico diminuida em {quant}.""")
        except:
            await ctx.send(f"""Erro""")

    @commands.command(name='cura')
    async def cura(self, ctx, bonus=0.0):
        embed = discord.Embed(
            title=f"""Quem vai conjurar?""",
            description=f"""Reaja com a opção desejada""",
            colour=discord.Colour.blue()
        )
        embed.add_field(name=":one:", value="Party", inline=False)
        embed.add_field(name=":two:", value="Horda", inline=False)
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
        conjurador = 0
        if ok == 1:
            embed = discord.Embed(
                title=f"""Qual personagem da Party irá conjurar?""",
                description=f"""Reaja com a opção desejada""",
                colour=discord.Colour.blue()
            )
            emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
            for j in range(len(self.party)):
                embed.add_field(name=emojis_disc[j], value=self.party[j], inline=False)
            embed_msg = await ctx.send(embed=embed)
            for i in range(len(self.party)):
                await embed_msg.add_reaction(emoji=emojis_raw[i])
            await embed_msg.add_reaction(emoji="❌")
            while conjurador == 0:
                reaction, user = await bot.wait_for('reaction_add', timeout=None)
                if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                    conjurador = 1
                if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                    conjurador = 2
                if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                    conjurador = 3
                if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                    conjurador = 4
                if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                    conjurador = 5
                if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                    conjurador = 6
            await embed_msg.delete()
            if conjurador < 6:
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[conjurador-1]))
                personagem_id = Database.personagem_id(self.party[conjurador-1])
                persona_id = Database.persona_equipada(personagem_id)
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
        elif ok == 2:
            embed = discord.Embed(
                title=f"""Qual personagem da Horda irá conjurar?""",
                description=f"""Reaja com a opção desejada""",
                colour=discord.Colour.blue()
            )
            emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            emojis_disc = [":one:", ":two:", ":three:", ":four:", ":five:"]
            for j in range(len(self.horda)):
                embed.add_field(name=emojis_disc[j], value=self.horda[j][1], inline=False)
            embed_msg = await ctx.send(embed=embed)
            for i in range(len(self.horda)):
                await embed_msg.add_reaction(emoji=emojis_raw[i])
            await embed_msg.add_reaction(emoji="❌")
            while conjurador == 0:
                reaction, user = await bot.wait_for('reaction_add', timeout=None)
                if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                    conjurador = 1
                if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                    conjurador = 2
                if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                    conjurador = 3
                if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                    conjurador = 4
                if str(reaction.emoji) == emojis_raw[4] and str(user) != "Persona Bot#0708":
                    conjurador = 5
                if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                    conjurador = 6
            await embed_msg.delete()
            canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
            if conjurador < 6:
                if self.horda[conjurador-1][0] == "s":
                    shadow_id = Database.shadow_id(self.horda[conjurador-1][1])
                    atributos_atacante = Database.atributos_iniciais(shadow_id)
                    nivel = Database.nivel_persona(shadow_id)
                    skills = Database.skills_shadow(shadow_id, nivel)
                    for i in range(len(atributos_atacante)):
                        atributos_atacante[i] = atributos_atacante[i][1]
                else:
                    personagem_id = Database.personagem_id(self.horda[conjurador-1][1])
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
        else:
            await ctx.send("Cura cancelada.")
        if conjurador > 0 and conjurador < 6:
            embed = discord.Embed(
                title=f"""Qual a magia de cura?""",
                description=f"""Reaja com a opção desejada""",
                colour=discord.Colour.blue()
            )
            emojis_raw = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
            embed.add_field(name=":one:", value="Dia", inline=False)
            embed.add_field(name=":two:", value="Media", inline=False)
            embed.add_field(name=":three:", value="Diarama", inline=False)
            embed.add_field(name=":four:", value="Mediarama", inline=False)
            embed_msg = await ctx.send(embed=embed)
            for i in range(4):
                await embed_msg.add_reaction(emoji=emojis_raw[i])
            await embed_msg.add_reaction(emoji="❌")
            skill = 0
            while skill == 0:
                reaction, user = await bot.wait_for('reaction_add', timeout=None)
                if str(reaction.emoji) == emojis_raw[0] and str(user) != "Persona Bot#0708":
                    skill = 1
                if str(reaction.emoji) == emojis_raw[1] and str(user) != "Persona Bot#0708":
                    skill = 2
                if str(reaction.emoji) == emojis_raw[2] and str(user) != "Persona Bot#0708":
                    skill = 3
                if str(reaction.emoji) == emojis_raw[3] and str(user) != "Persona Bot#0708":
                    skill = 4
                if str(reaction.emoji) == "❌" and str(user) != "Persona Bot#0708":
                    skill = 5
            await embed_msg.delete()
            if bonus != 0:
                try:
                    bonus = float(bonus)
                except:
                    bonus = 0
            if skill > 0:
                if ok == 1:
                    if skill == 1:
                        cura = int((1+bonus) * (50 + (50 * (atributos_atacante[3]/30))))
                        await canal.send(f"""**{self.party[conjurador-1]}** curou seu alvo em **{cura}**""")
                    elif skill == 2:
                        cura = int((1+bonus) * (50 + (50 * (atributos_atacante[3]/30))))
                        await canal.send(f"""**{self.party[conjurador-1]}** curou em área os alvos em **{cura}**""")
                    elif skill == 3:
                        cura = int((1+bonus) * (75 + (75 * (atributos_atacante[3]/30))))
                        await canal.send(f"""**{self.party[conjurador-1]}** curou seu alvo em **{cura}***""")
                    else:
                        cura = int((1+bonus) * (75 + (75 * (atributos_atacante[3]/30))))
                        await canal.send(f"""**{self.party[conjurador-1]}** curou em área os alvos em **{cura}**""")
                else:
                    if skill == 1:
                        cura = int((1+bonus) * (50 + (50 * (atributos_atacante[3]/30))))
                        await canal.send(f"""**{self.horda[conjurador-1][1]}** curou seu alvo em **{cura}**""")
                    elif skill == 2:
                        cura = int((1+bonus) * (50 + (50 * (atributos_atacante[3]/30))))
                        await canal.send(f"""**{self.horda[conjurador-1][1]}** curou em área os alvos em **{cura}**""")
                    elif skill == 3:
                        cura = int((1+bonus) * (75 + (75 * (atributos_atacante[3]/30))))
                        await canal.send(f"""**{self.horda[conjurador-1][1]}** curou seu alvo em **{cura}***""")
                    else:
                        cura = int((1+bonus) * (75 + (75 * (atributos_atacante[3]/30))))
                        await canal.send(f"""**{self.horda[conjurador-1][1]}** curou em área os alvos em **{cura}**""")
            else:
                await ctx.send("Cura cancelada.")

    @commands.command(name='interacao')
    async def interacao(self, ctx, tipo_grupo, codigo, elemento, tipo_interacao):
        try:
            codigo = int(codigo)
            atributo = int(atributo)
            tipo_interacao = int(tipo_interacao)
            if tipo_grupo == "horda":
                self.horda_elem_dano[codigo-1][elemento] == tipo_interacao
            elif tipo_grupo == "party":
                self.party_elem_dano[codigo-1][elemento] == tipo_interacao
            else:
                await ctx.send(f"""Tipo incorreto.""")
        except:
            await ctx.send(f"""Erro""")

def setup(bot):
    bot.add_cog(Combate(bot))