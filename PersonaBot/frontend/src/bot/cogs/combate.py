import math
import discord
from discord.ext import commands

from cogs.database import Database
from cogs.dado import Dado
from cogs.canal import Canal
from cogs.embed import EmbedComCampos, EmbedComReacao
from cogs.utilitarios import Ordenacao, Somatorio, Reparador, Gerador, Mensageiro

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
        self.mestre = 0
    
    @commands.command(name='add_horda')
    async def adicionar_horda(self, ctx, tipo, *personagem):
        nome = ""
        nome = Reparador.repara_nome(personagem)
        id_controlador = {
            "s": Database.shadow_id,
            "shadow": Database.shadow_id,
            "p": Database.personagem_id,
            "personagem": Database.personagem_id
        }
        if tipo == "p" or tipo == "s":
            elemento_id = id_controlador[tipo](nome)
            if elemento_id != False:
                self.horda.append((tipo,nome))
                self.horda_mult_atk.append(0)
                self.horda_mult_def.append(0)
                self.horda_mult_acc.append(0)
                self.horda_mult_evs.append(0)
                self.horda_mult_crit.append(0)
                self. horda_elem_dano.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                await ctx.send(f'**{nome}** foi adicionado à horda.')
            else:
                await ctx.send("Elemento não existente.")
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
        nome = Reparador.repara_nome(personagem)
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
    
    @commands.command(name='resetar_marcadores')
    async def resetar_marcadores(self, ctx):
        for i in range(len(self.party)):
            self.party_mult_atk[i] = 0
            self.party_mult_def[i] = 0
            self.party_mult_acc[i] = 0
            self.party_mult_evs[i] = 0
            self.party_mult_crit[i] = 0
        for i in range(len(self.horda)):
            self.horda_mult_atk[i] = 0
            self.horda_mult_def[i] = 0
            self.horda_mult_acc[i] = 0
            self.horda_mult_evs[i] = 0
            self.horda_mult_crit[i] = 0
        await ctx.send("Marcadores resetados!")
    
    @commands.command(name='resetar_interacoes')
    async def resetar_interacoes(self, ctx):
        for i in range(len(self.party)):
            self.party_elem_dano[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(self.horda)):
            self.horda_elem_dano[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        await ctx.send("Interações resetadas!")

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
                titulo = "Qual a forma de interação pré combate?"
                descricao ="Reaja com a opção desejada"
                cor = "azul"
                campos = [(":one:", "Emboscada"), (":two:","Disputa")]
                reacoes = ["1️⃣", "2️⃣"]
                embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
                ok = await embed.enviar_embed_reacoes()
                titulo = "**Ordem de turnos**"
                if ok == 1:
                    valor_criterio = await self.definir_valor_criterio(ctx, "**EMBOSCADA**: Qual o valor critério? (0 a 100)")
                    dado = await self.encaminhar_dado(canal)
                    if dado <= valor_criterio:
                        await canal.send(f'O grupo tirou um dado de {dado} e conseguiu emboscar a Shadow, vocês atacarão primeiro.')
                        ordem = Ordenacao.ordenacao_emboscada(self.party, self.horda, "party")
                    else:
                        await canal.send(f'O grupo tirou um dado de {dado} e falhou em emboscar a shadow, vocês atacarão de acordo com a sua agilidade.')
                        ordem = Ordenacao.ordenacao_disputa(self.party, self.horda)
                elif ok == 2:
                    valor_criterio = await self.definir_valor_criterio(ctx, "**DISPUTA**: Qual o valor critério? (0 a 100)")
                    dado = await self.encaminhar_dado(canal)
                    if dado <= valor_criterio:
                        await canal.send(f'O grupo tirou um dado de {dado} e conseguiu evitar ser emboscado, vocês atacarão de acordo com a sua agilidade.')
                        ordem = Ordenacao.ordenacao_disputa(self.party, self.horda)
                    else:
                        await canal.send(f'O grupo tirou um dado de {dado} e falhou em evitar ser emboscado, vocês atacarão por último.')
                        ordem = Ordenacao.ordenacao_emboscada(self.party, self.horda, "horda")
                if ordem != []:
                    texto = ""
                    i = 1
                    for elem in ordem:
                        texto += f'{i}. {elem}' + "\n"
                        i += 1
                    texto = texto[:-1]
                    campos = [("ORDEM:", texto)]
                    embed = EmbedComCampos(self.bot, canal, titulo, False, cor, False, campos, False)
                    await embed.enviar_embed()
                else:
                    await ctx.send("Cálculo cancelado.")
            else:
                await ctx.send("Sem requisitos mínimos para iniciar um combate.")
        except AttributeError:
            await ctx.send("Canal do grupo não está registrado.")

    @commands.command(name='ataque_fisico')
    async def ataque_fisico(self, ctx):
        try:
            horda_nomes = Reparador.repara_lista(self.horda, 1)
            atributos_atacante = []
            atributos_defensor = []
            ok1 = -1
            ok2 = -1
            valor = 0
            dano_mod = 0
            ataque = 0
            defesa = 0
            critico_mod = 0
            nome1 = ""
            nome2 = ""
            usuario = ""
            meelee_atacante = None
            armadura_defensor = None
            ok = await self.embed_selecionar_grupo(ctx)
            if ok == 1:
                ok1 = await self.embed_selecionar_unico(ctx, "party", "ataque")
                nome_party = self.party[ok1-1]
                nome1 = nome_party
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(nome_party))
                informacoes_party = Mensageiro.informacoes_personagem(nome_party)
                meelee_atacante = informacoes_party["meelee"]
                atributos_atacante = informacoes_party["atributos"]
                usuario = informacoes_party["usuario"]
                ok2 = await self.embed_selecionar_unico(ctx, "horda", "defesa")
                nome_horda = horda_nomes[ok2-1]
                nome2 = nome_horda
                informacoes_horda = await self.info_horda_defensor(ok2, nome_horda)
                atributos_defensor = informacoes_horda["atributos"]
                fraquezas = informacoes_horda["fraquezas"]
                if informacoes_horda["armadura"] != -1:
                    armadura_defensor = informacoes_horda["armadura"]
                valor = (self.party_mult_acc[ok1-1], self.horda_mult_evs[ok2-1])
                critico_mod =  self.party_mult_crit[ok1-1]
                ataque = self.party_mult_atk[ok1-1]
                defesa = self.horda_mult_def[ok2-1]
                dano_mod = self.horda_elem_dano[ok2-1][0]
            elif ok == 2:
                canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
                ok1 = await self.embed_selecionar_unico(ctx, "horda", "ataque")
                nome_horda = self.horda[ok1-1][1]
                nome1 = nome_horda
                ok2 = await self.embed_selecionar_unico(ctx, "party", "defesa")
                nome_party = self.party[ok2-1]
                nome2 = nome_party
                informacoes_party = Mensageiro.informacoes_personagem(nome_party)
                armadura_defensor = informacoes_party["armadura"]
                fraquezas = informacoes_party["fraquezas"]
                atributos_defensor = informacoes_party["atributos"]
                meelee_atacante = None
                if self.horda[ok1-1][0] == "s":
                    informacoes_horda = Mensageiro.informacoes_shadow(nome_horda)
                    fraquezas = informacoes_horda["fraquezas"]
                    atributos_atacante = informacoes_horda["atributos"]
                    usuario = f'{self.mestre.name}#{self.mestre.discriminator}'
                else:
                    informacoes_horda = Mensageiro.informacoes_personagem(nome_horda)
                    meelee_atacante = informacoes_horda["meelee"]
                    atributos_atacante = informacoes_horda["atributos"]
                    usuario = informacoes_horda["usuario"]
                valor = (self.horda_mult_acc[ok1-1], self.party_mult_evs[ok2-1])
                critico_mod =  self.horda_mult_crit[ok1-1]
                ataque = self.horda_mult_atk[ok1-1]
                defesa = self.party_mult_def[ok2-1]
                dano_mod = self.party_elem_dano[ok2-1][0]
            if ok < 3:
                var = await self.definir_valor_criterio(ctx, "Qual o valor critério? (0 a 100)")
                valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10 * valor[0]) - (10 * valor[1])
                await canal.send(f'Você precisa tirar um valor menor que **{valor_criterio}** no dado')
                dado = await Dado.rolagem_pronta(self.bot, canal, nome1, usuario, 1, 100)
                critico = 10 + (critico_mod * 10)
                if dado <= valor_criterio:
                    valor_arma = Mensageiro.info_meelee(meelee_atacante)
                    valor_armadura = Mensageiro.info_armadura(armadura_defensor)
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
                        7: f'**CRÍTICO!** **{nome1}** causou **{int(dano * 2)}** de dano e derrubou **{nome2}**!'
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
            await ctx.send(f'*Não foi possível executar o comando. Alguns dos motivos podem ser:*\n\n**Canal do jogador ou dos inimigos não encontrados**.\n*Dica: Cadastre o canal com o comando:* `{self.bot.command_prefix}canal_jogador <nome do personagem> <#canal>` ou `{self.bot.command_prefix}canal_inimigos <#canal>`\n\n**O mestre não foi definido**.\n*Dica: Defina o mestre com o comando:* `{self.bot.command_prefix}mestre <@usuário do mestre>`')

    @commands.command(name='tiro')
    async def tiro(self, ctx):
        try:
            horda_nomes = Reparador.repara_lista(self.horda, 1)
            ok1 = await self.embed_selecionar_unico(ctx, "party", "ataque")
            nome_party = self.party[ok1-1]
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(nome_party))
            informacoes_party = Mensageiro.informacoes_personagem(nome_party)
            ranged = informacoes_party["ranged"]
            atributos_atacante = informacoes_party["atributos"]
            usuario = informacoes_party["usuario"]
            ok2 = await self.embed_selecionar_unico(ctx, "horda", "defesa")
            nome_horda = horda_nomes[ok2-1]
            armadura_defensor = None
            informacoes_horda = await self.info_horda_defensor(ok2, nome_horda)
            atributos_defensor = informacoes_horda["atributos"]
            fraquezas = informacoes_horda["fraquezas"]
            if informacoes_horda["armadura"] != -1:
                armadura_defensor = informacoes_horda["armadura"]
            var = await self.definir_valor_criterio(ctx, "Qual o valor critério? (0 a 100)")
            valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10*self.party_mult_acc[ok1-1]) - (10*self.horda_mult_evs[ok2-1])
            await canal.send(f'Você precisa tirar um valor menor que **{valor_criterio}** no dado')
            critico = 10 + (self.party_mult_crit[ok1-1] * 10)
            dado = await Dado.rolagem_pronta(self.bot, canal, nome_party, usuario, 1, 100)
            if dado <= valor_criterio:
                valor_arma = Mensageiro.info_ranged(ranged)
                valor_armadura = Mensageiro.info_armadura(armadura_defensor)
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
                    7: f'**CRÍTICO!** **{nome_party}** causou **{int(dano * 2)}** de dano e derrubou **{nome_horda}**!'
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
            await ctx.send(f'*Não foi possível executar o comando. Alguns dos motivos podem ser:*\n\n**Canal do jogador ou dos inimigos não encontrados**.\n*Dica: Cadastre o canal com o comando:* `{self.bot.command_prefix}canal_jogador <nome do personagem> <#canal>` ou `{self.bot.command_prefix}canal_inimigos <#canal>`\n\n**O mestre não foi definido**.\n*Dica: Defina o mestre com o comando:* `{self.bot.command_prefix}mestre <@usuário do mestre>`')

    @commands.command(name='habilidade')
    async def habilidade(self, ctx, bonus=0.0, *habilidade):
        try:
            nome = Reparador.repara_nome(habilidade)
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
                atributos_atacante = []
                defensores_info = []
                valor1 = 0
                dano_mod = 0
                ataque = 0
                ok = await self.embed_selecionar_grupo(ctx)
                if ok == 1:
                    ok1 = await self.embed_selecionar_unico(ctx, "party", "ataque")
                    nome_party = self.party[ok1-1]
                    canal = self.bot.get_channel(Canal.carregar_canal_jogador(nome_party))
                    informacoes_party = Mensageiro.informacoes_personagem(nome_party)
                    skills = informacoes_party["skills"]
                    valor1 = self.party_mult_acc[ok1-1]
                    nome1 = nome_party
                    if skill_id in skills:
                        intensidade = Database.intensidade(skill_id)
                        elemento = Database.elemento(skill_id)
                        nome_elemento = Database.nome_elemento(elemento)
                        usuario = informacoes_party["usuario"]
                        atributos_atacante = informacoes_party["atributos"]
                        resultado = await self.embed_selecionar_multiplo(ctx, "horda")
                        defensores = resultado[1]
                        if defensores != []:
                            ataque = self.party_mult_atk[ok1-1]
                            valores = []
                            for defensor in defensores:
                                nome_horda = self.horda[defensor-1][1]
                                armadura_defensor = None
                                informacoes_horda = await self.info_horda_defensor(defensor, nome_horda)
                                atributos_defensor = informacoes_horda["atributos"]
                                fraquezas = informacoes_horda["fraquezas"]
                                if informacoes_horda["armadura"] != -1:
                                    armadura_defensor = informacoes_horda["armadura"]
                                defesa = self.horda_mult_def[defensor-1]
                                dano_mod = self.horda_elem_dano[defensor-1][elemento-1]
                                valor = self.horda_mult_evs[defensor-1]
                                defensor_info = (defensor, atributos_defensor, armadura_defensor, valor, defesa, dano_mod, fraquezas, nome_horda)
                                defensores_info.append(defensor_info)
                elif ok == 2:
                    ok1 = await self.embed_selecionar_unico(ctx, "horda", "ataque")
                    canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
                    nome_horda = self.horda[ok1-1][1]
                    nome1 = nome_horda
                    valor1 = self.horda_mult_acc[ok1-1]
                    if self.horda[ok1-1][0] == "s":
                        informacoes_horda = Mensageiro.informacoes_shadow(nome_horda)
                        fraquezas = informacoes_horda["fraquezas"]
                        atributos_atacante = informacoes_horda["atributos"]
                        skills = informacoes_horda["skills"]
                        usuario = f'{self.mestre.name}#{self.mestre.discriminator}'
                    else:
                        informacoes_horda = Mensageiro.informacoes_personagem(nome_horda)
                        skills = informacoes_horda["skills"]
                        atributos_atacante = informacoes_horda["atributos"]
                        usuario = informacoes_horda["usuario"]
                    if skill_id in skills:
                        resultado = await self.embed_selecionar_multiplo(ctx, "party")
                        defensores = resultado[1]
                        if defensores != []:
                            for defensor in defensores:
                                nome_party = self.party[defensor-1]
                                informacoes_party = Mensageiro.informacoes_personagem(self.party[defensor-1])
                                armadura_defensor = informacoes_party["armadura"]
                                fraquezas = informacoes_party["fraquezas"]
                                atributos_defensor = informacoes_party["atributos"]
                                defesa = self.party_mult_def[defensor-1]
                                dano_mod = self.party_elem_dano[defensor-1][elemento-1]
                                valor = self.party_mult_evs[defensor-1]
                                defensor_info = (defensor, atributos_defensor, armadura_defensor, valor, defesa, dano_mod, fraquezas, nome_party)
                                defensores_info.append(defensor_info)
                            ataque = self.horda_mult_atk[ok1-1]
                if defensores_info != []:
                    var = await self.definir_valor_criterio(ctx, "Qual o valor critério? (0 a 100)")
                    valores = []
                    for defensor_info in defensores_info:
                        atributos_defensor = defensor_info[1]
                        valor2 = defensor_info[3]
                        valor_criterio = var + (5*(atributos_atacante[5]//5)) - (5*(atributos_defensor[6]//5)) + (10 * valor1) - (10 * valor2)
                        valores.append(valor_criterio)
                    texto = ""
                    for valor in valores:
                        texto += str(valor) + ", "
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
                        valor_armadura = Mensageiro.info_armadura(armadura_defensor)
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
            await ctx.send(f'*Não foi possível executar o comando. Alguns dos motivos podem ser:*\n\n**Canal do jogador ou dos inimigos não encontrados**.\n*Dica: Cadastre o canal com o comando:* `{self.bot.command_prefix}canal_jogador <nome do personagem> <#canal>` ou `{self.bot.command_prefix}canal_inimigos <#canal>`\n\n**O mestre não foi definido**.\n*Dica: Defina o mestre com o comando:* `{self.bot.command_prefix}mestre <@usuário do mestre>`')

    @commands.command(name='doenca')
    async def doenca(self, ctx, bonus=0, *nome_doenca):
        try:
            nome_doenca = Reparador.repara_nome(nome_doenca)
            chance = await self.embed_selecionar_chance(ctx)
            if chance < 4:
                afetados_info = []
                canal = 0
                nome = ""
                grupo = await self.embed_selecionar_grupo(ctx)
                if grupo == 1:
                    conjurador = await self.embed_selecionar_unico(ctx, "party", "cura") - 1
                    nome = self.party[conjurador]
                    canal = self.bot.get_channel(Canal.carregar_canal_jogador(nome))
                    informacoes_party = Mensageiro.informacoes_personagem(nome)
                    usuario = informacoes_party["usuario"]
                    resultado = await self.embed_selecionar_multiplo(ctx, "horda")
                    afetados = resultado[1]
                    for afetado in afetados:
                        nome_horda = self.horda[afetado-1][1]
                        informacoes_horda = await self.info_horda_defensor(afetado, nome_horda)
                        sorte_afetado = informacoes_horda["atributos"][6]
                        valor = self.party_mult_evs[afetado-1]
                        afetado_info = (afetado, nome_horda, sorte_afetado, valor)
                        afetados_info.append(afetado_info)
                elif grupo == 2:
                    conjurador = await self.embed_selecionar_unico(ctx, "horda", "conjura") - 1
                    nome = self.horda[conjurador][1]
                    usuario = f'{self.mestre.name}#{self.mestre.discriminator}'
                    canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
                    resultado = await self.embed_selecionar_multiplo(ctx, "party")
                    afetados = resultado[1]
                    for afetado in afetados:
                        nome_party = self.party[afetado-1]
                        informacoes_party = Mensageiro.informacoes_personagem(self.party[afetado-1])
                        sorte_afetado = informacoes_party["atributos"][6]
                        valor = self.party_mult_evs[afetado-1]
                        afetado_info = (afetado, nome_party, sorte_afetado, valor)
                        afetados_info.append(afetado_info)
                if grupo < 3:
                    valores = []
                    for afetado_info in afetados_info:
                        sorte = afetado_info[2]
                        evasao = afetado_info[3]
                        valor_criterio = (chance * 5) - ((sorte//10) * 1) - (evasao * 1)
                        valores.append(valor_criterio)
                    texto = ""
                    for valor in valores:
                        texto += str(valor) + ", "
                    texto = texto[:-2]
                    await canal.send(f'Você precisa tirar valor(es) menor(es) que **{texto}** no dado')
                    dado = await Dado.rolagem_pronta(self.bot, canal, nome, usuario, 1, 100)
                    i = 0
                    for valor in valores:
                        nome_afetado = afetados_info[i][1]
                        if dado <= valor:
                            await canal.send(f'**{nome_afetado}** foi contaminado com **{nome_doenca}**')
                        else:
                            await canal.send(f'**{nome_afetado}** evitou a contaminação por **{nome_doenca}**')
                        i += 1
                else:
                    await ctx.send("Doença cancelada.")
            else:
                await ctx.send("Doença cancelada.")
        except:
            await ctx.send(f'*Não foi possível executar o comando. Alguns dos motivos podem ser:*\n\n**Canal do jogador ou dos inimigos não encontrados**.\n*Dica: Cadastre o canal com o comando:* `{self.bot.command_prefix}canal_jogador <nome do personagem> <#canal>` ou `{self.bot.command_prefix}canal_inimigos <#canal>`\n\n**O mestre não foi definido**.\n*Dica: Defina o mestre com o comando:* `{self.bot.command_prefix}mestre <@usuário do mestre>`')


    @commands.command(name='lider')
    async def lider(self, ctx, personagem):
        canal = self.bot.get_channel(Canal.carregar_canal_grupo())
        if self.party != []:
            for i in range(len(self.party)):
                if self.party[i] == personagem:
                    self.party.insert(0, self.party.pop(i))
                    await canal.send(f'**{personagem}** foi denominado o líder do grupo.')
                    break
    
    @commands.command(name='mestre')
    async def mestre(self, ctx, mestre: discord.User):
        self.mestre = mestre
        await ctx.send(f'O mestre agora é {self.mestre.name}#{self.mestre.discriminator}')
    
    @commands.command(name='marcador')
    async def marcador(self, ctx, quant=0):
        try:
            canal = 0
            marc = await self.embed_selecionar_marcador(ctx)
            ok = await self.embed_selecionar_grupo(ctx)
            grupos = {
                1: "party",
                2: "horda",
                3: 0
            }
            marcadores = {
                1: "atk",
                2: "def",
                3: "acc",
                4: "evs",
                5: "crit",
                6: 0
            }
            tipo_grupo = grupos[ok]
            marcador = marcadores[marc]
            char = 0
            if tipo_grupo == "party":
                char = await self.embed_selecionar_unico(ctx, "party", "marcador")
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[char-1]))
            elif tipo_grupo == "horda":
                canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
                char = await self.embed_selecionar_unico(ctx, "horda", "marcador")
            codigo = char - 1
            if (tipo_grupo != 0 and marcador != 0 and char > 0):
                await self.modifica_marcador(ctx, canal, tipo_grupo, marcador, codigo, quant)
            else:
                await ctx.send("Modificação do marcador cancelada.")
        except:
            await ctx.send("*Não foi possível ser executado o comando, digite um número inteiro.")

    async def embed_selecionar_grupo(self, ctx):
        titulo = "Qual grupo será o protagonista?"
        descricao = "Reaja com a opção desejada"
        cor = "azul"
        campos = [(":one:", "Party"), (":two:", "Horda")]
        reacoes = ["1️⃣", "2️⃣", "❌"]
        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
        opcao = await embed.enviar_embed_reacoes()
        return opcao
    
    async def embed_selecionar_unico(self, ctx, grupo, modo):
        grupo_controlador = {
            "party": {
                "ataque": "Qual personagem da Party irá atacar?",
                "defesa": "Qual personagem da Party será atacado?",
                "cura": "Quem vai conjurar?",
                "interacao": "Quem terá a interação elemental modificada?",
                "marcador": "Quem terá seu marcador modificado?"
            },
            "horda": {
                "ataque": "Qual elemento da Horda irá atacar?",
                "defesa": "Queal da horda será atacado?",
                "interacao": "Quem terá a interação elemental modificada?",
                "marcador": "Quem terá seu marcador modificado?",
                "conjura": "Quem vai conjurar?"
            }
        }
        opcao = -1
        titulo = grupo_controlador[grupo][modo]
        cor = "azul"
        descricao = "Reaja com a opção desejada"
        campos = []
        info = await self.gerar_campos_reacoes(grupo)
        campos = info[0]
        reacoes = info[1]
        reacoes.append("❌")
        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
        opcao = await embed.enviar_embed_reacoes()
        return opcao
    
    async def embed_selecionar_elemento(self, ctx):
        opcao = -1
        titulo = "Selecione o elemento"
        cor = "azul"
        descricao = "Reaja com a opção desejada"
        campos = []
        reacoes = ["<:phys:790320130810839101>", "<:gun:790320131028287488>", "<:fire:790320130483421245>", "<:ice:790320130738356224>", "<:elec:790320130151809047>", "<:wind:790320130521169922>", "<:psy:790320130772566046>", "<:nuclear:790320130584084532>", "<:bless:790320130746744892>", "<:curse:790320130387214336>", "<:almighty:790320130297954374>", "❌"]
        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
        opcao = await embed.enviar_embed_reacoes()
        return opcao
    
    async def embed_selecionar_interacao(self, ctx):
        opcao = -1
        titulo = "Selecione a interação elemental"
        cor = "azul"
        descricao = "Reaja com a opção desejada"
        reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "❌"]
        campos = [
            (":one:", "Fraco"),
            (":two:", "Forte"),
            (":three:", "Nulo"),
            (":four:", "Drena"),
            (":five:", "Reflete"),
            (":six:", "Normal")
        ]
        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
        opcao = await embed.enviar_embed_reacoes()
        return opcao
    
    async def embed_selecionar_chance(self, ctx):
        opcao = -1
        titulo = "Selecione a chance de afetamento"
        cor = "azul"
        descricao = "Reaja com a opção desejada"
        reacoes = ["1️⃣", "2️⃣", "3️⃣","❌"]
        campos = [
            (":one:", "Chances baixas"),
            (":two:", "Chances médias"),
            (":three:", "Chances altas")
        ]
        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
        opcao = await embed.enviar_embed_reacoes()
        return opcao
    
    async def embed_selecionar_marcador(self, ctx):
        opcao = -1
        titulo = "Selecione o marcador desejado"
        cor = "azul"
        descricao = "Reaja com a opção desejada"
        reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "❌"]
        campos = [
            (":one:", "Ataque"),
            (":two:", "Defesa"),
            (":three:", "Acurácia"),
            (":four:", "Evasão"),
            (":five:", "Crítico")
        ]
        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
        opcao = await embed.enviar_embed_reacoes()
        return opcao
    
    async def embed_selecionar_multiplo(self, ctx, grupo):
        grupo_controlador = {
            "party": "Quem/Quais da party serão atacado(s)?",
            "horda": "Quem/Quais da horda serão atacado(s)?"
        }
        cor = "azul"
        titulo = grupo_controlador[grupo]
        descricao = "Reaja com a opções desejadas e confirme"
        info = await self.gerar_campos_reacoes(grupo)
        campos = info[0]
        reacoes = info[1]
        reacoes.append("✅")
        reacoes.append("❌")
        embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, campos, False, reacoes)
        resultado = await embed.enviar_embed_reacoes_multiplas()
        return resultado
    
    async def gerar_campos_reacoes(self, grupo):
        emojis_campo = [":one:", ":two:", ":three:", ":four:", ":five:"]
        reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        if grupo == "party":
            campos = Gerador.gerador_campos(emojis_campo, self.party)
            reacoes = reacoes[:len(self.party)]
        else:
            horda_nomes = Reparador.repara_lista(self.horda, 1)
            campos = Gerador.gerador_campos(emojis_campo, horda_nomes)
            reacoes = reacoes[:len(self.horda)]
        info = (campos, reacoes)
        return info
    
    async def modifica_marcador(self, ctx, canal, tipo_grupo, marcador, codigo, quant):
        try:
            operador = ""
            if quant > 0:
                operador = "aumentado(a)"
            else:
                operador = "diminuído(a)"
            texto_controlador = {}
            if tipo_grupo == "party":
                texto_controlador = {
                    "atk": f'**{self.party[codigo-1]}** teve seu ataque {operador} em {quant}.',
                    "def": f'**{self.party[codigo-1]}** teve sua defesa {operador} em {quant}.',
                    "acc": f'**{self.party[codigo-1]}** teve sua acurácia {operador} em {quant}.',
                    "evs": f'**{self.party[codigo-1]}** teve sua evasão {operador} em {quant}.',
                    "crit": f'**{self.party[codigo-1]}** teve seu crítico {operador} em {quant}.'
                }
            else:
                texto_controlador = {
                    "atk": f'**{self.horda[codigo-1][1]}** teve seu ataque {operador} em {quant}.',
                    "def": f'**{self.horda[codigo-1][1]}** teve sua defesa {operador} em {quant}.',
                    "acc": f'**{self.horda[codigo-1][1]}** teve sua acurácia {operador} em {quant}.',
                    "evs": f'**{self.horda[codigo-1][1]}** teve sua evasão {operador} em {quant}.',
                    "crit": f'**{self.horda[codigo-1][1]}** teve seu crítico {operador} em {quant}.'
                }
            if marcador == "atk":
                self.party_mult_atk[codigo-1] += quant
            elif marcador == "def":
                self.party_mult_def[codigo-1] += quant
            elif marcador == "acc":
                self.party_mult_acc[codigo-1] += quant
            elif marcador == "evs":
                self.party_mult_evs[codigo-1] += quant
            else:
                self.party_mult_crit[codigo-1] += quant
            await canal.send(texto_controlador[marcador])
        except ValueError:
            await ctx.send("Erro em algum valor, tente novamente")

    @commands.command(name='cura')
    async def cura(self, ctx, bonus=0.0):
        ok = await self.embed_selecionar_grupo(ctx)
        conjurador = 0
        tamanho = 0
        if ok == 1:
            tamanho = len(self.party)
            conjurador = await self.embed_selecionar_party_unico(ctx, "cura")
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
            conjurador = await self.embed_selecionar_horda_unico(ctx, "cura")
            canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
            if conjurador < 6:
                nome = self.horda[conjurador-1][1]
                if self.horda[conjurador-1][0] == "s":
                    shadow_id = Database.shadow_id(self.horda[conjurador-1][1])
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
            descricao = "Reaja com a opção desejada"
            reacoes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
            cor = "azul"
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
    async def interacao(self, ctx):
        elementos = {
            1: "Físico",
            2: "Arma de Fogo",
            3: "Fogo",
            4: "Gelo",
            5: "Elétrico",
            6: "Vento",
            7: "Psy",
            8: "Nuclear",
            9: "Benção",
            10: "Maldição",
            11: "Onipotência"
        }
        interacoes = {
            1: "Fraco",
            2: "Forte",
            3: "Nulo",
            4: "Drena",
            5: "Reflete",
            6: "Normal"
        }
        try:
            ok = await self.embed_selecionar_grupo(ctx)
            canal = 0
            if ok == 1:
                char = await self.embed_selecionar_unico(ctx, "party", "interacao")
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(self.party[char-1]))
            elif ok == 2:
                char = await self.embed_selecionar_unico(ctx, "horda", "interacao")
                canal = self.bot.get_channel(Canal.carregar_canal_inimigos())
            if ok < 3:
                elemento = await self.embed_selecionar_elemento(ctx)
                if elemento < 12:
                    intera = await self.embed_selecionar_interacao(ctx)
                    if intera < 7 and ok == 1:
                        self.party_elem_dano[char-1][elemento-1] = intera
                        await canal.send(f'A interação elemental de **{elementos[elemento]}** de **{self.party[char-1]}** foi alterada para **{interacoes[intera]}**')
                    elif intera < 7 and ok == 2:
                        self.horda_elem_dano[char-1][elemento-1] = intera
                        await canal.send(f'A interação elemental de **{elementos[elemento]}** de **{self.horda[char-1][1]}** foi alterada para **{interacoes[intera]}**')
                    else:
                        await ctx.send("Mudança de interação cancelada.")
                else:
                    await ctx.send("Mudança de interação cancelada.")
            else:
                await ctx.send("Mudança de interação cancelada.")
        except ValueError:
            await ctx.send("Erro")
        except IndexError:
            await ctx.send("Mudança de interação cancelada.")
    
    async def definir_valor_criterio(self, ctx, titulo):
        next = 0
        valor_criterio = -1
        while next == 0:
            await ctx.send(titulo)
            msg = await self.bot.wait_for('message')
            mensagem = msg.content
            try:
                valor_criterio = int(mensagem)
                if valor_criterio > 0 and valor_criterio <= 100:
                    next = 1
            except ValueError:
                await ctx.send("Digite um número entre 0 e 100.")
        return valor_criterio
    
    async def info_horda_defensor(self, opcao, nome_horda):
        info = {}
        fraquezas = 0
        atributos_defensor = 0
        armadura_defensor = -1
        if self.horda[opcao-1][0] == "s":
            informacoes_horda = Mensageiro.informacoes_shadow(nome_horda)
            fraquezas = informacoes_horda["fraquezas"]
            atributos_defensor = informacoes_horda["atributos"]
        else:
            informacoes_horda = Mensageiro.informacoes_personagem(nome_horda)
            fraquezas = informacoes_horda["fraquezas"]
            armadura_defensor = informacoes_horda["armadura"]
            info["fraquezas"] = armadura_defensor
            atributos_defensor = informacoes_horda["atributos"]
        info["fraquezas"] = fraquezas
        info["atributos"] = atributos_defensor
        info["armadura"] = armadura_defensor
        return info
    
    async def encaminhar_dado(self, canal):
        lider_id = Database.personagem_id(self.party[0])
        usuario = Database.discord_user(lider_id)
        dado = await Dado.rolagem_pronta(self.bot, canal, self.party[0], usuario, 1, 100)
        return dado

def setup(bot):
    bot.add_cog(Combate(bot))