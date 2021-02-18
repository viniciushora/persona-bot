import discord
import random
import pickle
from discord.ext import commands

from cogs.database import *
from cogs.canal import *

class Persona(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='upar')
    async def subir_nivel(self, ctx, personagem):
        try:
            personagem_id = Database.personagem_id(personagem)
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
            eh_fool = Database.eh_fool(personagem_id)
            emote = ["<:phys:790320130810839101>", "<:gun:790320131028287488>", "<:fire:790320130483421245>", "<:ice:790320130738356224>", "<:elec:790320130151809047>", "<:wind:790320130521169922>", "<:psy:790320130772566046>", "<:nuclear:790320130584084532>", "<:bless:790320130746744892>", "<:curse:790320130387214336>", "<:almighty:790320130297954374>", "<:ailment:790320130286551060>", "<:healing:790320130508718100>", "<:support:790320130323775518>", "<:passive:790320130780561408>", "<:navigator:798197909761556521>"]
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
                flex.sort(key=self.takeSecond, reverse=True)
                nao_repetidos = list(dict.fromkeys(flex))
                pontos = 3
                valores_criterio = []
                if len(nao_repetidos) == 5:
                    valores_criterio = [90, 72, 54, 36, 18]
                elif len(nao_repetidos) == 4:
                    valores_criterio = [90, 68, 44, 22]
                elif len(nao_repetidos) == 3:
                    valores_criterio = [90, 60, 30]
                elif len(nao_repetidos) == 2:
                    valores_criterio = [90, 45]
                else:
                    valores_criterio = [90]
                while pontos > 0:
                    for atributo_id, quant_inicial in flex:
                        pos = -1
                        for i in range(len(nao_repetidos)):
                            if quant_inicial == nao_repetidos[i]:
                                pos = i
                                break
                        valor_criterio = valores_criterio[pos]
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
                                    elemento = Database.elemento(skill)
                                    await canal.send(f"""**{personagem}** aprendeu a habilidade **{nome_skill}** {emote[elemento-1]}""")
                    elif len(skills_id) + len(nivel_skills) > 8 and len(skills) < 8:
                        tam = len(skills_id)
                        while tam < 8:
                            if nivel_skills[i] not in skills_id:
                                aprendeu = Database.add_skill(nivel_skills[0], personagem_persona_id)
                                if aprendeu == True:
                                    nome_skill = Database.nome_skill(nivel_skills[0])
                                    elemento = Database.elemento(nivel_skills[0])
                                    await canal.send(f"""**{personagem}** aprendeu a habilidade **{nome_skill}** {emote[elemento-1]}""")
                                    del nivel_skills[i]
                                    tam += 1
                        if nivel_skills != []:
                            nova_skills = Database.skills(personagem_id, persona_id)
                            skills_id = []
                            for skill in nova_skills:
                                skills_id.append(Database.skill_id(skill))
                            for skill in nivel_skills:
                                nome_skill = Database.nome_skill(skill)
                                elemento = Database.elemento(skill)
                                embed = discord.Embed(
                                    title=f"""**{personagem}** aprendeu uma nova habilidade!""",
                                    description=f"""Você já conhece habilidades demais, deseja trocar alguma por **{nome_skill}** {emote[elemento-1]}?""",
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
                                    reaction, user = await self.bot.wait_for('reaction_add', timeout=None)
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
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=None)
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
        except:
            await ctx.send("Canal do jogador não registrado.")
    
    @commands.command(name='desupar')
    async def diminuir_nivel(self, ctx, personagem):
        try:
            personagem_id = Database.personagem_id(personagem)
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
        except:
            await ctx.send("Canal do jogador não registrado.")

    @commands.command(name='upar_persona')
    async def subir_nivel_persona(self, ctx, personagem):
        try:
            personagem_id = Database.personagem_id(personagem)
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
                flex.sort(key=self.takeSecond, reverse=True)
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
                                    reaction, user = await self.bot.wait_for('reaction_add', timeout=None)
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
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=None)
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
        except:
            await ctx.send("Canal do jogador não registrado.")
    
    @commands.command(name='desupar_persona')
    async def diminuir_nivel_persona(self, ctx, personagem):
        try:
            personagem_id = Database.personagem_id(personagem)
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
        except:
            await ctx.send("Canal do jogador não registrado.")

    @commands.command(name='equipar_persona')
    async def equipar_persona(self, ctx, personagem):
        try:
            personagem_id = Database.personagem_id(personagem)
            eh_fool = Database.eh_fool(personagem_id)
            if personagem_id != False:
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=None)
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
        except:
            await ctx.send("Canal do jogador não registrado.")

    @commands.command(name='tomar_persona')
    async def tomar_persona(self, ctx , personagem, *persona):
        try:
            personagem_id = Database.personagem_id(personagem)
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
        except:
            await ctx.send("Canal do jogador não registrado.")

    @commands.command(name='soltar_persona')
    async def soltar_persona(self, ctx, personagem, *persona):
        try:
            personagem_id = Database.personagem_id(personagem)
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
        except:
            await ctx.send("Canal do jogador não registrado.")

    @commands.command(name='habilidades_conhecidas')
    async def skills_conhecidas(self, ctx, personagem):
        try:
            personagem_id = Database.personagem_id(personagem)
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
            persona_id = Database.persona_equipada(personagem_id)
            nome = Database.nome_persona(persona_id)
            nivel = Database.nivel(personagem_id, persona_id)
            skills = Database.skills_conhecidas(nivel, persona_id)
            texto = ""
            emote = ["<:phys:790320130810839101>", "<:gun:790320131028287488>", "<:fire:790320130483421245>", "<:ice:790320130738356224>", "<:elec:790320130151809047>", "<:wind:790320130521169922>", "<:psy:790320130772566046>", "<:nuclear:790320130584084532>", "<:bless:790320130746744892>", "<:curse:790320130387214336>", "<:almighty:790320130297954374>", "<:ailment:790320130286551060>", "<:healing:790320130508718100>", "<:support:790320130323775518>", "<:passive:790320130780561408>", "<:navigator:798197909761556521>"]
            for skill in skills:
                nome_skill = Database.nome_skill(skill)
                skill_id = Database.skill_id(nome_skill)
                elemento = Database.elemento(skill_id)
                texto += f"""{nome_skill} {emote[elemento-1]}\n"""
            texto = texto[:-1]
            embed = discord.Embed(
                title=f"""Habilidades conhecidas de **{nome}**""",
                description=texto,
                colour=discord.Colour.blue()
            )
            await canal.send(embed=embed)
        except:
            await ctx.send("Canal do jogador não registrado.")
    
    @commands.command(name='aprender_skill')
    async def aprender_skill(self, ctx, personagem, *skill):
        global canais_jogadores
        try:
            nome = ""
            for palavra in skill:
                nome += palavra + " "
            nome = nome[:-1]
            personagem_id = Database.personagem_id(personagem)
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=None)
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
        except:
            await ctx.send("Canal do jogador não registrado.")

    @commands.command(name='esquecer_skill')
    async def esquecer_skill(self, ctx, personagem):
        try:
            personagem_id = Database.personagem_id(personagem)
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
                reaction, user = await self.bot.wait_for('reaction_add', timeout=None)
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
        except:
            await ctx.send("Canal do jogador não registrado.")
    
    @commands.command(name='add_atributo')
    async def add_atributo(self, ctx, personagem, tipo, quant, atributo):
        canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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

    @commands.command(name='del_atributo')
    async def del_atributo(self, ctx, personagem, quant, atributo):
        canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
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
    
    def takeSecond(self, elem):
        return elem[1]

def setup(bot):
    bot.add_cog(Persona(bot))