import discord
import math
from discord.ext import commands

from cogs.database import Database
from cogs.dado import Dado
from cogs.canal import Canal
from cogs.embed import Embed, EmbedComCampos, EmbedComReacao
from cogs.utilitarios import Ordenacao, Somatorio, Reparador, Gerador

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
                await ctx.send(f'**{nome}** foi adicionado à horda.')
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
                await ctx.send(f'**{nome}** foi adicionado à horda.')
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
            await ctx.send(f'**{personagem}** foi adicionado à Party.')
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
                    await ctx.send(f'**{personagem}** foi removido da Party.')
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
                    await ctx.send(f'**{nome}** foi removido da horda.')
                    achou = 1
            if achou == 0:
                await ctx.send("Nome não encontrado.")
        else:
            await ctx.send("Nome não encontrado.")

    @commands.command(name='party')
    async def mostrar_party(self, ctx):
        if self.party != []:
            titulo = "**PARTY**"
            cor = "azul"
            texto = ""
            i = 1
            for elem in self.party:
                texto += f'{i}.**{elem}**' + "\n"
                i +=1
            texto = texto[:-1]
            campos = [("Lista dos membros da Party", texto)]
            embed = EmbedComCampos(self.bot, ctx, titulo, False, cor, False, campos, False)
            await embed.enviar_embed()
        else:
            await ctx.send("A party está vazia")
    
    @commands.command(name='horda')
    async def mostrar_horda(self, ctx):
        if self.horda != []:
            opcoes = {"s": "Shadow", "p": "Personagem"}
            cor = "azul"
            texto = ""
            i = 1
            for tipo, elem in self.horda:
                nome = opcoes[tipo]
                texto += f'{i}.**{elem}** ({nome})' + "\n"
                i += 1
            texto = texto[:-1]
            titulo = "**HORDA**"
            campos = [("Lista dos elementos da Horda", texto)]
            embed = EmbedComCampos(self.bot, ctx, titulo, False, cor, False, campos, False)
            await embed.enviar_embed()
        else:
            await ctx.send("A horda está vazia")

    @commands.command(name='calcular_turnos')
    async def calcular_turnos(self, ctx):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            ordem = []
            if self.horda != [] and self.party != []:
                titulo = "Qual a forma de interação pós combate?"
                descricao ="Reaja com a opção desejada"
                cor = "azul"
                campos = [(":one:", "Emboscada"), (":two:","Disputa")]
                reacoes = ["1️⃣", "2️⃣"]
                embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                ok = await embed.enviar_embed_reacoes()
                titulo = "**Ordem de turnos**"
                if ok == 1:
                    next = 0
                    while next == 0:
                        await ctx.send("**EMBOSCADA**: Qual o valor critério? (0 a 100)")
                        msg = await self.bot.wait_for('message')
                        mensagem = msg.content
                        try:
                            valor_criterio = int(mensagem)
                            if valor_criterio > 0 and valor_criterio <= 100:
                                next = 1
                        except:
                            await ctx.send("Digite um número entre 0 e 100.")
                    lider_id = Database.personagem_id(self.party[0])
                    usuario = Database.discord_user(lider_id)
                    dado = await Dado.rolagem_pronta(self.bot, canal, self.party[0], usuario, 1, 100)
                    if dado <= valor_criterio:
                        await canal.send(f'O grupo tirou um dado de {dado} e conseguiu emboscar a Shadow, vocês atacarão primeiro.')
                        ordem = Ordenacao.ordenacao_emboscada(self.party, self.horda)
                    else:
                        await canal.send(f'O grupo tirou um dado de {dado} e falhou em emboscar a shadow, vocês atacarão de acordo com a sua agilidade.')
                        ordem = Ordenacao.ordenacao_disputa(self.party, self.horda)
                elif ok == 2:
                    next = 0
                    while next == 0:
                        await ctx.send("**DISPUTA**: Qual o valor critério? (0 a 100)")
                        msg = await self.bot.wait_for('message')
                        mensagem = msg.content
                        try:
                            valor_criterio = int(mensagem)
                            if valor_criterio > 0 and valor_criterio <= 100:
                                next = 1
                        except:
                            await ctx.send("Digite um número entre 0 e 100.")
                    lider_id = Database.personagem_id(self.party[0])
                    usuario = Database.discord_user(lider_id)
                    dado = await Dado.rolagem_pronta(self.bot, canal, self.party[0], usuario, 1, 100)
                    if dado <= valor_criterio:
                        await canal.send(f'O grupo tirou um dado de {dado} e conseguiu evitar ser emboscado, vocês atacarão de acordo com a sua agilidade.')
                        ordem = Ordenacao.ordenacao_disputa(self.party, self.horda)
                    else:
                        await canal.send(f'O grupo tirou um dado de {dado} e falhou em evitar ser emboscado, vocês atacarão por último.')
                        ordem = Ordenacao.ordenacao_emboscado(self.party, self.horda)
                if ordem != []:
                    texto = ""
                    i = 1
                    for elem in ordem:
                        texto += f'{i}. {elem}' + "\n"
                        i += 1
                    texto[:-1]
                    campos = [("ORDEM:", texto)]
                    embed = EmbedComCampos(self.bot, canal, titulo, False, cor, False, campos, False)
                    await embed.enviar_embed()
                else:
                    await ctx.send("Cálculo cancelado.")
            else:
                await ctx.send("Sem requisitos mínimos para iniciar um combate.")
        except:
            await ctx.send("Canal do grupo não está registrado.")

    @commands.command(name='ataque_fisico')
    async def ataque_fisico(self, ctx):
        try:
            atributos_atacante = []
            atributos_defensor = []
            ok1 = -1
            ok2 = -1
            nome1 = ""
            nome2 = ""
            usuario = ""
            meelee_atacante = None
            armadura_defensor = None
            valor = 0
            dano_mod = 0
            ataque = 0
            defesa = 0
            critico_mod = 0
            emojis_campo = [":one:", ":two:", ":three:", ":four:", ":five:"]
            fraquezas = []
            titulo = "Quem vai atacar?"
            descricao = "Reaja com a opção desejada"
            cor = "azul"
            campos = [(":one:", "Party"), (":two:", "Horda")]
            reacoes = ["1️⃣", "2️⃣", "❌"]
            embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
            ok = await embed.enviar_embed_reacoes()
            if ok == 1:
                titulo = "Qual personagem da Party irá atacar?"
                descricao = "Reaja com a opção desejada"
                campos = Gerador.gerador_campos(emojis_campo, self.party)
                reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                reacoes = reacoes[:len(self.party)]
                reacoes.append("❌")
                embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                ok1 = await embed.enviar_embed_reacoes()
                nome_party = self.party[ok1-1]
                nome1 = nome_party
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(nome_party))
                personagem_id = Database.personagem_id(nome_party)
                persona_id = Database.persona_equipada(personagem_id)
                usuario = Database.discord_user(personagem_id)
                equips = Database.itens_equipados(personagem_id)
                meelee_atacante = equips[0]
                atributos = Database.atributos(personagem_id, persona_id)
                atributos_base = Reparador.valores_atributos(atributos)
                atributos_atacante = Somatorio.atributos_totais_personagem(personagem_id, atributos_base)
                titulo = "Quem da horda será atacado?"
                horda_nomes = Reparador.repara_lista(self.horda, 1)
                campos = Gerador.gerador_campos(emojis_campo, horda_nomes)
                reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                reacoes = reacoes[:len(self.horda)]
                reacoes.append("❌")
                embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                ok2 = await embed.enviar_embed_reacoes()
                nome_horda = horda_nomes[ok2-1]
                nome2 = nome_horda
                if self.horda[ok2-1][0] == "s":
                    shadow_id = Database.shadow_id(nome_horda)
                    fraquezas = Database.fraquezas(shadow_id)
                    atributos = Database.atributos_iniciais(shadow_id)
                    atributos_defensor = Reparador.valores_atributos(atributos)
                else:
                    defensor_id = Database.personagem_id(nome_horda)
                    d_persona_id = Database.persona_equipada(defensor_id)
                    equips_defensor = Database.itens_equipados(defensor_id)
                    armadura_defensor = equips_defensor[2]
                    fraquezas = Database.fraquezas(d_persona_id)
                    atributos = Database.atributos(defensor_id, d_persona_id)
                    atributos_base = Reparador.valores_atributos(atributos)
                    atributos_defensor = Somatorio.atributos_totais_personagem(defensor_id, atributos_base)
                valor = (self.party_mult_acc[ok1-1], self.horda_mult_evs[ok2-1])
                critico_mod =  self.party_mult_crit[ok1-1]
                ataque = self.party_mult_atk[ok1-1]
                defesa = self.horda_mult_def[ok2-1]
                dano_mod = self.horda_elem_dano[ok2-1][0]
            elif ok == 2:
                canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
                titulo = "Qual personagem da Horda irá atacar?"
                descricao = "Reaja com a opção desejada"
                horda_nomes = Reparador.repara_lista(self.horda, 1)
                campos = Gerador.gerador_campos(emojis_campo, horda_nomes)
                reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                reacoes = reacoes[:len(self.horda)]
                reacoes.append("❌")
                embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                ok1 = await embed.enviar_embed_reacoes()
                nome_horda = self.horda[ok1-1][1]
                nome1 = nome_horda
                titulo = "Qual personagem da Party será atacado?"
                descricao = "Reaja com a opção desejada"
                emojis_campo = [":one:", ":two:", ":three:", ":four:", ":five:"]
                campos = Gerador.gerador_campos(emojis_campo, self.party)
                reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                reacoes = reacoes[:len(self.party)]
                reacoes.append("❌")
                embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                ok2 = await embed.enviar_embed_reacoes()
                nome_party = self.party[ok2-1]
                nome2 = nome_party
                personagem_id = Database.personagem_id(nome_party)
                persona_id = Database.persona_equipada(personagem_id)
                usuario = Database.discord_user(personagem_id)
                equips = Database.itens_equipados(personagem_id)
                fraquezas = Database.fraquezas(persona_id)
                armadura_defensor = equips[2]
                atributos = Database.atributos(personagem_id, persona_id)
                atributos_base = Reparador.valores_atributos(atributos)
                atributos_defensor = Somatorio.atributos_totais_personagem(personagem_id, atributos_base)
                meelee_atacante = None
                if self.horda[ok1-1][0] == "s":
                    shadow_id = Database.shadow_id(nome_horda)
                    atributos_base = Database.atributos_iniciais(shadow_id)
                    atributos_atacante = Reparador.valores_atributos(atributos_base)
                else:
                    atacante_id = Database.personagem_id(nome_horda)
                    a_persona_id = Database.persona_equipada(personagem_id)
                    equips_atacante = Database.itens_equipados()
                    meelee_atacante = equips_atacante[0]
                    atributos = Database.atributos(atacante_id, a_persona_id)
                    atributos_base = Reparador.valores_atributos(atributos)
                    atributos_atacante = Somatorio.atributos_totais_personagem(atacante_id, atributos_base)
                valor = (self.horda_mult_acc[ok1-1], self.party_mult_evs[ok2-1])
                critico_mod =  self.horda_mult_crit[ok1-1]
                ataque = self.horda_mult_atk[ok1-1]
                usuario = "Axuáti#9639"
                defesa = self.party_mult_def[ok2-1]
                dano_mod = self.party_elem_dano[ok2-1][0]
            if ok < 3:
                next = 0
                while next == 0:
                    await ctx.send("Qual o valor critério? (0 a 100)")
                    msg = await self.bot.wait_for('message')
                    mensagem = msg.content
                    try:
                        var = int(mensagem)
                        if var > 0 and var <= 100:
                            next = 1
                    except:
                        await ctx.send("Digite um número entre 0 e 100.")
                valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10 * valor[0]) - (10 * valor[1])
                await canal.send(f'Você precisa tirar um valor menor que **{valor_criterio}** no dado')
                dado = await Dado.rolagem_pronta(self.bot, canal, nome1, usuario, 1, 100)
                critico = 10 + (critico_mod * 10)
                if dado <= valor_criterio:
                    if meelee_atacante != None:
                        valor_arma = Database.valor_item(meelee_atacante)
                    else:
                        valor_arma = 0
                    if armadura_defensor == None:
                        valor_armadura = 0
                    else:
                        valor_armadura = Database.valor_item(armadura_defensor)
                    dano = int(20 + math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2])) * ((0.3 * ataque) + 1) 
                    dano_mitigado = int(dano / math.sqrt((atributos_defensor[4]*8) + valor_armadura)) * ((0.3 * defesa) + 1)
                    dano = dano - dano_mitigado
                    interacoes = {
                        1: f'**FRACO!** **{nome1}** causou **{int(dano * 2)}** de dano e derrubou **{nome2}**!',
                        2: f'**RESISTIU!** {nome1}** causou **{int(dano / 2)}** de dano em **{nome2}**!',
                        3: f'**NULIFICOU!** **{nome2}** nulificou todo o dano causado!',
                        4: f'**DRENOU!** **{nome2}** se curou em **{int(dano)}**!',
                        5: f'**REFLETIU!** **{nome2}** refletiu **{int(dano)}** de dano em **{nome1}**!',
                        6: f'**{nome1}** causou **{int(dano)}** de dano em **{nome2}**!',
                        7: f'**CRÍTICO!** {nome1}** causou **{int(dano * 2)}** de dano e derrubou **{nome2}**!'
                    }  
                    if dano_mod > 0:
                        await canal.send(interacoes[dano_mod])
                    elif dado <= critico:
                        await canal.send(interacoes[7])
                    else:
                        await canal.send(interacoes[fraquezas[0]])
                else:
                    await canal.send(f'**{nome1}** errou o ataque físico  em **{nome2}**')
            else:
                await ctx.send("Ataque físico cancelado.")
        except:
            await ctx.send("Ataque cancelado ou Algo está incorreto.")

    @commands.command(name='tiro')
    async def tiro(self, ctx):
        try:
            titulo = "Qual personagem da Party irá atacar?"
            descricao = "Reaja com a opção desejada"
            cor = "azul"
            emojis_campo = [":one:", ":two:", ":three:", ":four:", ":five:"]
            campos = Gerador.gerador_campos(emojis_campo, self.party)
            reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            reacoes = reacoes[:len(self.party)]
            reacoes.append("❌")
            embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
            ok1 = await embed.enviar_embed_reacoes()
            nome_party = self.party[ok1-1]
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[ok1-1]))
            personagem_id = Database.personagem_id(nome_party)
            persona_id = Database.persona_equipada(personagem_id)
            usuario = Database.discord_user(personagem_id)
            equips = Database.itens_equipados(personagem_id)
            ranged = equips[1]
            atributos = Database.atributos(personagem_id, persona_id)
            atributos_base = Reparador.valores_atributos(atributos)
            atributos_atacante = Somatorio.atributos_totais_personagem(personagem_id, atributos_base)
            titulo = "Quem da horda será atacado?"
            horda_nomes = Reparador.repara_lista(self.horda, 1)
            campos = Gerador.gerador_campos(emojis_campo, horda_nomes)
            reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            reacoes = reacoes[:len(self.horda)]
            reacoes.append("❌")
            embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
            ok2 = await embed.enviar_embed_reacoes()
            nome_horda = horda_nomes[ok2-1]
            armadura_defensor = None
            if self.horda[ok2-1][0] == "s":
                shadow_id = Database.shadow_id(nome_horda)
                fraquezas = Database.fraquezas(shadow_id)
                atributos_base = Database.atributos_iniciais(shadow_id)
                atributos_defensor = Reparador.valores_atributos(atributos_base)
            else:
                defensor_id = Database.personagem_id(nome_horda)
                d_persona_id = Database.persona_equipada(defensor_id)
                equips_defensor = Database.itens_equipados(defensor_id)
                armadura_defensor = equips_defensor[2]
                fraquezas = Database.fraquezas(d_persona_id)
                atributos = Database.atributos(defensor_id, d_persona_id)
                atributos_base = Reparador.valores_atributos(atributos)
                atributos_defensor = Somatorio.atributos_totais_personagem(defensor_id, atributos_base)
            next = 0
            while next == 0:
                await ctx.send("Qual o valor critério? (0 a 100)")
                msg = await self.bot.wait_for('message')
                mensagem = msg.content
                try:
                    var = int(mensagem)
                    if var > 0 and var <= 100:
                        next = 1
                except:
                    await ctx.send("Digite um número entre 0 e 100.")
            valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.party_mult_acc[ok1-1]) - (10*self.horda_mult_evs[ok2-1])
            await canal.send(f'Você precisa tirar um valor menor que **{valor_criterio}** no dado')
            critico = 10 + (self.party_mult_crit[ok1-1] * 10)
            dado = await Dado.rolagem_pronta(self.bot, canal, self.party[ok1-1], usuario, 1, 100)
            if dado <= valor_criterio:
                if ranged == None:
                    valor_arma = 0
                else:
                    valor_arma = Database.valor_item(ranged)
                if armadura_defensor == None:
                    valor_armadura = 0
                else:
                    valor_armadura = Database.valor_item(armadura_defensor)
                dano = int(math.sqrt(valor_arma) * math.sqrt(atributos_atacante[2])) * ((0.3 * self.party_mult_atk[ok1-1]) + 1) 
                dano_mitigado = int(math.sqrt(atributos_defensor[4]*8 + valor_armadura)) * ((0.3 * self.horda_mult_def[ok2-1]) + 1)
                dano = dano - dano_mitigado
                interacoes = {
                    1: f'**FRACO!** **{nome_party}** causou **{int(dano * 2)}** de dano e derrubou **{nome_horda}**!',
                    2: f'**RESISTIU!** {nome_party}** causou **{int(dano / 2)}** de dano em **{nome_horda}**!',
                    3: f'**NULIFICOU!** **{nome_horda}** nulificou todo o dano causado!',
                    4: f'**DRENOU!** **{nome_horda}** se curou em **{int(dano)}**!',
                    5: f'**REFLETIU!** **{nome_horda}** refletiu **{int(dano)}** de dano em **{nome_party}**!',
                    6: f'**{nome_party}** causou **{int(dano)}** de dano em **{nome_horda}**!',
                    7: f'**CRÍTICO!** {nome_party}** causou **{int(dano * 2)}** de dano e derrubou **{nome_horda}**!'
                }  
                if self.horda_elem_dano[ok2-1][1] > 0:
                    await canal.send(interacoes[self.horda_elem_dano[ok2-1][1]])
                elif dado <= critico:
                    await canal.send(interacoes[7])
                else:
                    await canal.send(interacoes[fraquezas[0]])
            else:
                await canal.send(f'**{nome_party}** errou o tiro em **{nome_horda}**')
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
                intensidade = Database.intensidade(skill_id)
                elemento = Database.elemento(skill_id)
                tipo = ""
                if elemento < 3:
                    tipo = "fisico"
                else:
                    tipo = "magico"
                nome_elemento = Database.nome_elemento(elemento)
                vezes = Database.skill_vezes(skill_id)
                nome_skill = Database.nome_skill(skill_id)
                nome1 = ""
                atributos_atacante = []
                defensores_info = []
                valor1 = 0
                dano_mod = 0
                critico_mod = 0
                ataque = 0
                titulo = "Quem vai atacar?"
                descricao = "Reaja com a opção desejada"
                cor = "azul"
                campos = [(":one:", "Party"), (":two:", "Horda")]
                emojis_campo = [":one:", ":two:", ":three:", ":four:", ":five:"]
                reacoes = ["1️⃣", "2️⃣", "❌"]
                embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                ok = await embed.enviar_embed_reacoes()
                if ok == 1:
                    titulo = "Qual personagem da Party irá atacar?"
                    campos = Gerador.gerador_campos(emojis_campo, self.party)
                    reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                    reacoes = reacoes[:len(self.party)]
                    reacoes.append("❌")
                    embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                    ok1 = await embed.enviar_embed_reacoes()
                    nome_party = self.party[ok1-1]
                    nome1 = nome_party
                    canal = self.bot.get_channel(Canal.carregar_canal_jogador(nome_party))
                    personagem_id = Database.personagem_id(nome_party)
                    persona_id = Database.persona_equipada(personagem_id)
                    skills = Database.skills_id(personagem_id, persona_id)
                    valor1 = self.party_mult_acc[ok1-1]
                    if skill_id in skills:
                        intensidade = Database.intensidade(skill_id)
                        elemento = Database.elemento(skill_id)
                        nome_elemento = Database.nome_elemento(elemento)
                        usuario = Database.discord_user(personagem_id)
                        atributos = Database.atributos(personagem_id, persona_id)
                        atributos_base = Reparador.valores_atributos(atributos)
                        atributos_atacante = Somatorio.atributos_totais_personagem(personagem_id, atributos_base)
                        titulo = "Quem/Quais da horda serão atacado(s)?"
                        horda_nomes = Reparador.repara_lista(self.horda, 1)
                        campos = Gerador.gerador_campos(emojis_campo, horda_nomes)
                        reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                        reacoes = reacoes[:len(self.horda)]
                        reacoes.append("✅")
                        reacoes.append("❌")
                        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                        resultado = await embed.enviar_embed_reacoes_multiplas()
                        ok2 = resultado[0]
                        defensores = resultado[1]
                        if ok2 == len(reacoes) - 1 and defensores != []:
                            valores = []
                            for defensor in defensores:
                                nome_horda = self.horda[defensor-1][1]
                                armadura_defensor = None
                                if self.horda[defensor-1][0] == "s":
                                    shadow_id = Database.shadow_id(nome_horda)
                                    fraquezas = Database.fraquezas(shadow_id)
                                    atributos_base = Database.atributos_iniciais(shadow_id)
                                    atributos_defensor = Reparador.valores_atributos(atributos_base)
                                else:
                                    defensor_id = Database.personagem_id(self.party[defensor-1])
                                    d_persona_id = Database.persona_equipada(defensor_id)
                                    equips_defensor = Database.itens_equipados(defensor_id)
                                    armadura_defensor = equips_defensor[2]
                                    fraquezas = Database.fraquezas(d_persona_id)
                                    atributos = Database.atributos(defensor_id, d_persona_id)
                                    atributos_base = Reparador.valores_atributos(atributos)
                                    atributos_defensor = Somatorio.atributos_totais_personagem(defensor_id, atributos_base)
                                defesa = self.horda_mult_def[defensor-1]
                                dano_mod = self.horda_elem_dano[defensor-1][elemento]
                                valor = self.horda_mult_evs[defensor-1]
                                defensor_info = (defensor, atributos_defensor, armadura_defensor, valor, defesa, dano_mod, fraquezas, nome_horda)
                                defensores_info.append(defensor_info)
                            ataque = self.party_mult_atk[ok1-1]
                elif ok == 2:
                    titulo = "Qual personagem da Horda irá atacar?"
                    horda_nomes = Reparador.repara_lista(self.horda, 1)
                    campos = Gerador.gerador_campos(emojis_campo, horda_nomes)
                    reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                    reacoes = reacoes[:len(self.horda)]
                    reacoes.append("❌")
                    embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                    ok1 = await embed.enviar_embed_reacoes()
                    canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
                    nome_horda = self.horda[ok1-1][1]
                    nome1 = nome_horda
                    usuario = "Axuáti#9639"
                    valor1 = self.horda_mult_acc[ok1-1]
                    if self.horda[ok1-1][0] == "s":
                        shadow_id = Database.shadow_id(nome_horda)
                        nivel = Database.nivel_persona(shadow_id)
                        skills = Database.skills_shadow(shadow_id, nivel)
                        atributos_base = Database.atributos_iniciais(shadow_id)
                        atributos_atacante = Reparador.valores_atributos(atributos_base)
                    else:
                        personagem_id = Database.personagem_id(nome_horda)
                        persona_id = Database.persona_equipada(personagem_id)
                        atributos_atacante = Database.atributos_iniciais(shadow_id)
                        skills = Database.skills_id(personagem_id, persona_id)
                        atributos = Database.atributos(personagem_id, persona_id)
                        atributos_base = Reparador.valores_atributos(atributos)
                        atributos_atacante = Somatorio.atributos_totais_personagem(personagem_id, atributos_base)
                    if skill_id in skills:
                        titulo = "Quem/Quais da party serão atacado(s)?"
                        campos = Gerador.gerador_campos(emojis_campo, self.party)
                        reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                        reacoes = reacoes[:len(self.party)]
                        reacoes.append("✅")
                        reacoes.append("❌")
                        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                        resultado = await embed.enviar_embed_reacoes_multiplas()
                        ok2 = resultado[0]
                        defensores = resultado[1]
                        if ok2 == len(reacoes) - 1 and defensores != []:
                            for defensor in defensores:
                                defensor_id = Database.personagem_id(self.party[defensor-1])
                                nome_party = self.party[defensor-1]
                                d_persona_id = Database.persona_equipada(defensor)
                                equips_defensor = Database.itens_equipados(defensor_id)
                                armadura_defensor = equips_defensor[2]
                                fraquezas = Database.fraquezas(d_persona_id)
                                atributos = Database.atributos(defensor_id, d_persona_id)
                                atributos_base = Reparador.valores_atributos(atributos)
                                atributos_defensor = Somatorio.atributos_totais_personagem(defensor_id, atributos_base)
                                defesa = self.party_mult_def[defensor-1]
                                dano_mod = self.party_elem_dano[defensor-1][elemento]
                                valor = self.party_mult_evs[defensor-1]
                                defensor_info = (defensor, atributos_defensor, armadura_defensor, valor, defesa, dano_mod, fraquezas, nome_party)
                                defensores_info.append(defensor_info)
                            ataque = self.horda_mult_atk[ok1-1]
                if defensores_info != []:
                    next = 0
                    while next == 0:
                        await ctx.send("Qual o valor critério? (0 a 100)")
                        msg = await self.bot.wait_for('message')
                        mensagem = msg.content
                        try:
                            var = int(mensagem)
                            if var > 0 and var <= 100:
                                next = 1
                        except:
                            await ctx.send("Digite um número entre 0 e 100.")
                    valores = []
                    for defensor_info in defensores_info:
                        atributos_defensor = defensor_info[1]
                        valor2 = defensor_info[3]
                        valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10 * valor1) - (10 * valor2)
                        valores.append(valor_criterio)
                    texto = ""
                    for valor in valores:
                        texto += str(valor_criterio) + ", "
                    texto = texto[:-2]
                    await canal.send(f'Você precisa tirar valor(es) menor(es) que **{texto}** no dado')
                    dados = []
                    for i in range(vezes):   
                        dado = await Dado.rolagem_pronta(self.bot, canal, nome1, usuario, 1, 100)
                        dados.append(dado)
                    habilidade_controlador = {
                        "fisico": int((intensidade * 25) * math.sqrt(atributos_atacante[2])),
                        "magico": int((intensidade * 25) + ((intensidade * 25) * (atributos_atacante[3]/30)))
                    }
                    dano = (bonus + 1) * habilidade_controlador[tipo] * ((0.3 * ataque) + 1)
                    i = 0
                    for defensor_info in defensores_info:
                        atributos_defensor = defensor_info[1]
                        armadura_defensor = defensor_info[2]
                        defesa = defensor_info[4]
                        dano_mod = defensor_info[5]
                        fraquezas = defensor_info[6]
                        nome2 = defensor_info[7]
                        if armadura_defensor == None:
                            valor_armadura = 0
                        else:
                            valor_armadura = Database.valor_item(armadura_defensor)
                        dano_mitigado = int(math.sqrt((atributos_defensor[4]*8) + valor_armadura)) * ((0.3 * defesa) + 1)
                        dano = dano - dano_mitigado
                        interacoes = {
                            1: f'**FRACO!** **{nome1}** causou **{int(dano * 2)}** de dano de {nome_elemento} e derrubou **{nome2}**!',
                            2: f'**RESISTIU!** {nome1}** causou **{int(dano / 2)}** de dano de {nome_elemento} em **{nome2}**!',
                            3: f'**NULIFICOU!** **{nome2}** nulificou todo o dano de {nome_elemento} causado!',
                            4: f'**DRENOU!** **{nome2}** se curou em **{int(dano)} de {nome_elemento}**!',
                            5: f'**REFLETIU!** **{nome2}** refletiu **{int(dano)}** de dano de {nome_elemento} em **{nome1}**!',
                            6: f'**{nome1}** causou **{int(dano)}** de dano de {nome_elemento} em **{nome2}**!'
                        }  
                        for dado in dados:
                            if dado <= valores[i]:
                                if dano_mod > 0:
                                    await canal.send(interacoes[dano_mod])
                                else:
                                    await canal.send(interacoes[fraquezas[elemento-1]])
                            else:
                                await canal.send(f'**{nome1}** errou a habilidade **{nome_skill}** em **{nome2}**')
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
                    self.party.insert(0, self.party.pop(i))
                    await canal.send(f'**{personagem}** foi denominado o líder do grupo.')
                    break
    
    @commands.command(name='marcador')
    async def marcador(self, ctx, tipo_marcador, tipo_grupo, codigo=0, quant=0):
        try:
            canal = 0
            if tipo_grupo == "party":
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[codigo-1]))
            elif tipo_grupo == "horda":
                canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
            execucao = {
                'atk': self.modifica_ataque(tipo_grupo, codigo, canal, quant),
                'def': self.modifica_defesa(tipo_grupo, codigo, canal, quant),
                'acc': self.modifica_acuracia(tipo_grupo, codigo, canal, quant),
                'evs': self.modifica_evasao(tipo_grupo, codigo, canal, quant),
                'crit': self.modifica_critico(tipo_grupo, codigo, canal, quant)
            }
            await execucao[tipo_marcador]
        except:
            await ctx.send("Erro")
    
    async def modifica_ataque(self, tipo_grupo, codigo, canal, quant):
        if tipo_grupo == "party":
            self.party_mult_atk[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.party[codigo-1]}** teve seu ataque aumentado em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.party[codigo-1]}** teve seu ataque diminuido em {quant}.')
        else:
            self.horda_mult_atk[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve seu ataque aumentado em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve seu ataque diminuido em {quant}.')
    
    async def modifica_defesa(self, tipo_grupo, codigo, canal, quant):
        if tipo_grupo == "party":
            self.party_mult_def[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.party[codigo-1]}** teve sua defesa aumentada em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.party[codigo-1]}** teve sua defesa diminuida em {quant}.')
        else:
            self.horda_mult_atk[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve sua defesa aumentada em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve sua defesa diminuida em {quant}.')
    
    async def modifica_acuracia(self, tipo_grupo, codigo, canal, quant):
        if tipo_grupo == "party":
            self.party_mult_acc[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.party[codigo-1]}** teve sua acurácia aumentada em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.party[codigo-1]}** teve sua acurácia diminuida em {quant}.')
        else:
            self.horda_mult_acc[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve sua acurácia aumentada em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve sua acurácia diminuida em {quant}.')
    
    async def modifica_evasao(self, tipo_grupo, codigo, canal, quant):
        if tipo_grupo == "party":
            self.party_mult_evs[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.party[codigo-1]}** teve sua evasão aumentada em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.party[codigo-1]}** teve sua evasão diminuida em {quant}.')
        else:
            self.horda_mult_evs[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve sua evasão aumentada em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve sua evasão diminuida em {quant}.')
    
    async def modifica_critico(self, tipo_grupo, codigo, canal, quant):
        if tipo_grupo == "party":
            self.party_mult_evs[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.party[codigo-1]}** teve sua evasão aumentada em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.party[codigo-1]}** teve sua evasão diminuida em {quant}.')
        else:
            self.horda_mult_evs[codigo-1] += quant
            if quant > 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve sua evasão aumentada em {quant}.')
            elif quant < 0:
                await canal.send(f'**{self.horda[codigo-1][1]}** teve sua evasão diminuida em {quant}.')

    @commands.command(name='cura')
    async def cura(self, ctx, bonus=0.0):
        titulo = "Quem vai atacar?"
        descricao = "Reaja com a opção desejada"
        cor = "azul"
        campos = [(":one:", "Party"), (":two:", "Horda")]
        emojis_campo = [":one:", ":two:", ":three:", ":four:", ":five:"]
        reacoes = ["1️⃣", "2️⃣", "❌"]
        nome = ""
        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
        ok = await embed.enviar_embed_reacoes()
        conjurador = 0
        tamanho = 0
        if ok == 1:
            tamanho = len(self.party)
            titulo = "Quem vai atacar?"
            descricao = "Reaja com a opção desejada"
            cor = "azul"
            campos = Gerador.gerador_campos(emojis_campo, self.party)
            reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            reacoes = reacoes[:len(self.party)]
            reacoes.append("❌")
            embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
            conjurador = await embed.enviar_embed_reacoes()
            print(conjurador)
            if conjurador < 6:
                nome = self.party[conjurador-1]
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[conjurador-1]))
                personagem_id = Database.personagem_id(self.party[conjurador-1])
                persona_id = Database.persona_equipada(personagem_id)
                atributos = Database.atributos(personagem_id, persona_id)
                atributos_base = Reparador.valores_atributos(atributos)
                atributos_conjurador = Somatorio.atributos_totais_personagem(personagem_id, atributos_base)
        elif ok == 2:
            tamanho = len(self.horda)
            titulo = "Qual personagem da Horda irá atacar?"
            horda_nomes = Reparador.repara_lista(self.horda, 1)
            campos = Gerador.gerador_campos(emojis_campo, horda_nomes)
            reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            reacoes = reacoes[:len(self.horda)]
            reacoes.append("❌")
            embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
            conjurador = await embed.enviar_embed_reacoes()
            canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
            if conjurador < 6:
                nome = self.horda[conjurador-1][1]
                if self.horda[conjurador-1][0] == "s":
                    shadow_id = Database.shadow_id(self.horda[conjurador-1][1])
                    nivel = Database.nivel_persona(shadow_id)
                    atributos_base = Database.atributos_iniciais(shadow_id)
                    atributos_conjurador = Reparador.valores_atributos(atributos_base)
                else:
                    personagem_id = Database.personagem_id(self.horda[conjurador-1][1])
                    persona_id = Database.persona_equipada(personagem_id)
                    atributos = Database.atributos(personagem_id, persona_id)
                    atributos_base = Reparador.valores_atributos(atributos)
                    atributos_conjurador = Somatorio.atributos_totais_personagem(personagem_id, atributos_base)
        if conjurador > 0 and conjurador < tamanho + 2:
            titulo = "Qual a magia de cura?"
            reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
            campos = [(":one:", "Dia"), (":two:", "Media"), (":three:", "Diarama"), (":four:", "Mediarama")]
            embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
            skill = await embed.enviar_embed_reacoes()
            skill_controlador = {
                1: int((1+bonus) * (50 + (50 * (atributos_conjurador[3]/30)))),
                2: int((1+bonus) * (50 + (50 * (atributos_conjurador[3]/30)))),
                3: int((1+bonus) * (75 + (75 * (atributos_conjurador[3]/30)))),
                4: int((1+bonus) * (75 + (75 * (atributos_conjurador[3]/30))))
            }
            area_controlador = {
                1: "curou seu alvo",
                2: "curou em área os alvos",
                3: "curou seu alvo",
                4: "curou em área os alvos"
            }     
            await canal.send(f'**{nome}** {area_controlador[skill]} em **{skill_controlador[skill]}**')
        else:
            await ctx.send("Cura cancelada.")

    @commands.command(name='interacao')
    async def interacao(self, ctx, tipo_grupo, codigo=0, elemento=0, tipo_interacao=0):
        try:
            if tipo_grupo == "horda":
                self.horda_elem_dano[codigo-1][elemento] == tipo_interacao
            elif tipo_grupo == "party":
                self.party_elem_dano[codigo-1][elemento] == tipo_interacao
            else:
                await ctx.send("Tipo incorreto.")
        except:
            await ctx.send("Erro")

def setup(bot):
    bot.add_cog(Combate(bot))