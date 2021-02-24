import random
from discord.ext import commands

from cogs.database import Database
from cogs.canal import Canal
from cogs.embed import EmbedComCampos
from cogs.utilitarios import Gerador, Reparador

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
            nome = Reparador.repara_nome(item)
            item_id = Database.item_id(nome)
            if item_id != False:
                contem_item = Database.item_no_inventario(nome)
                if contem_item != False:
                    soma_item = Database.soma_item_database(item_id, contem_item[1], quant)
                    if soma_item:
                        await canal.send(f'**{quant} {nome}** adicionado(s) no inventário do grupo. Quantidade atual: ({contem_item[1]+quant})')
                else:
                    add_item = Database.add_item_database(item_id, quant)
                    if add_item:
                        await canal.send(f'**{quant} {nome}** adicionado(s) no inventário do grupo.')
                    else:
                        await ctx.send("**Erro interno**")
            else:
                await ctx.send(f'**{nome} não existe.**"')
        except:
            await ctx.send("Canal do grupo não registrado.")
    
    @commands.command(name='del_item')
    async def deletar_item(self, ctx, quant, *item):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            quant = int(quant)
            nome = Reparador.repara_nome(item)
            item_id = Database.item_id(nome)
            if item_id != False:
                contem_item = Database.item_no_inventario(nome)
                if contem_item != False:
                    if contem_item[1] > quant:
                        subtrai_item = Database.subtrai_item_database(item_id, contem_item[1], quant)
                        print(subtrai_item)
                        await canal.send(f'**{quant} {nome}** removido(s) no inventário do grupo. Quantidade atual: ({contem_item[1]-quant})')
                    else:
                        delete_item = Database.del_item_database(item_id)
                        await canal.send(f'**{nome}** removido completamente do inventário do grupo.')
                else:
                    await ctx.send(f'**{nome}** não encontrado no inventário do grupo.')
            else:
                await ctx.send(f'**{nome} não existe.**')
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
                    await canal.send(f'Adicionado **R$ {quant}**; (Valor anterior: **R$ {dinheiro_inicial}**). O dinheiro do grupo agora é **R$ {dinheiro_final}**')
                else:
                    await ctx.send("Erro interno")
            except:
                await ctx.send("Valor incorreto")
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
                    await canal.send(f'O dinheiro do grupo agora é **R$ {quant}**')
                else:
                    await ctx.send("Erro interno")
            except:
                await ctx.send("Valor incorreto")
        except:
            await ctx.send("Canal do grupo não registrado.")
    
    @commands.command(name='drop')
    async def drop(self, ctx, *shadow):
        try:
            canal = self.bot.get_channel(Canal.carregar_canal_grupo())
            nome = Reparador.repara_nome(shadow)
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
            titulo = f'**Drops de {nome}**'
            descricao = f'Dinheiro: R$ {dinheiro1} ; Experiência : {exp}'
            cor = "verde"
            texto = ""
            if lista_drops != []:
                for drop in lista_drops:
                    texto += drop + "; "
                texto = texto[:-2]
            else:
                texto = "Sem itens dropados"
            campos = ["Itens dropados", texto]
            embed = EmbedComCampos(self.bot, canal, titulo, descricao, cor, False, campos, False)
            await embed.enviar_embed()
        except:
            await ctx.send("Canal do grupo não registrado ou informações do dado erradas.")
    
    @commands.command(name='equipar')
    async def equipar(self, ctx, personagem, *item):
        try:
            nome = Reparador.repara_nome(item)
            personagem_id = Database.personagem_id(personagem)
            if personagem_id != False:
                canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
                item_id = Database.item_id(nome)
                if item_id != False:
                    contem_item = Database.item_no_inventario(nome)
                    if contem_item != False:
                        tipo_item_id = Database.tipo_item_id(item_id)
                        equip = Database.equipar_item(personagem_id, item_id, tipo_item_id)
                        texto_controlador = {
                            7: f'**{nome}** agora é a arma corpo-a-corpo equipada de **{personagem}**',
                            8: f'**{nome}** agora é a arma à distância equipada de **{personagem}**',
                            9: f'**{nome}** agora é a armadura equipado de **{personagem}**',
                            10: f'**{nome}** agora é o acessório equipado de **{personagem}**'
                        }
                        if equip == False:
                            await canal.send("Este item não é equipável")
                        else:
                            await canal.send(texto_controlador[tipo_item_id])
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
            nome = Reparador.repara_nome(item)
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
                            texto_controlador = {
                                7: f'**{nome}** não está mais equipado(a) como arma corpo-a-corpo de **{personagem}**',
                                8: f'**{nome}** não está mais equipado(a) como arma à distância equipada de **{personagem}**',
                                9: f'**{nome}** não está mais equipado(a) como armadura equipada de **{personagem}**',
                                10: f'**{nome}** não está mais equipado(a) como acessório equipado de **{personagem}**'
                            }
                            if desequip == False:
                                await canal.send("Este item não é equipável")
                            else:
                                await canal.send(texto_controlador[tipo_item_id])
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
            lista_controlador = {
                "Consumíveis": consumiveis.append,
                "Cartas de Habilidade": cartas.append,
                "Materiais": materiais.append,
                "Tesouros": tesouros.append,
                "Essenciais": essenciais.append,
                "Itens-chave": itens_chave.append,
                "Armas Corpo-a-corpo": armas_meelee.append,
                "Armas à distância": armas_ranged.append,
                "Armadura": armaduras.append,
                "Acessórios": acessorios.append,
                "Roupas": acessorios.append
            }
            for item, tipo_item, quant in itens:
                lista_controlador[tipo_item]((item,quant))
            dinheiro = Database.dinheiro_grupo()
            titulo = "**Inventário do grupo**"
            descricao = f'Dinheiro: R$ {dinheiro}'
            cor = "azul"
            campos = []
            if consumiveis != []:
                texto = Gerador.gerador_texto(consumiveis)
                campo = ("Consumíveis", texto)
                campos.append(campo)
            if cartas != []:
                texto = Gerador.gerador_texto(cartas)
                campo = ("Cartas", texto)
                campos.append(campo)
            if materiais != []:
                texto = Gerador.gerador_texto(materiais)
                campo = ("Materiais", texto)
                campos.append(campo)
            if tesouros != []:
                texto = Gerador.gerador_texto(tesouros)
                campo = ("Tesouros", texto)
                campos.append(campo)
            if essenciais != []:
                texto = Gerador.gerador_texto(essenciais)
                campo = ("Essenciais", texto)
                campos.append(campo)
            if itens_chave != []:
                texto = Gerador.gerador_texto(itens_chave)
                campo = ("Itens-Chave", texto)
                campos.append(campo)
            if armas_meelee != []:
                texto = Gerador.gerador_texto(armas_meelee)
                campo = ("Armas corpo à corpo", texto)
                campos.append(campo)
            if armas_ranged != []:
                texto = Gerador.gerador_texto(armas_ranged)
                campo = ("Armas à distância", texto)
                campos.append(campo)
            if armaduras != []:
                texto = Gerador.gerador_texto(armaduras)
                campo = ("Armaduras", texto)
                campos.append(campo)
            if acessorios != []:
                texto = Gerador.gerador_texto(acessorios)
                campo = ("Acessórios", texto)
                campos.append(campo)
            if roupas != []:
                texto = Gerador.gerador_texto(roupas)
                campo = ("Roupas", texto)
                campos.append(campo)
            embed = EmbedComCampos(self.bot, canal, titulo, descricao, cor, False, campos, False)
            await embed.enviar_embed()
        except:
            await ctx.send("Canal do grupo não registrado.")

def setup(bot):
    bot.add_cog(Item(bot))