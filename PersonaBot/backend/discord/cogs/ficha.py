import discord
import pickle
from discord.ext import commands

from cogs.database import Database
from cogs.canal import Canal
from cogs.embed import Embed, EmbedComCampos, EmbedComReacao
from cogs.utilitarios import Gerador

class Ficha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reacoes_elementos = [
            "<:phys:790320130810839101>",
            "<:gun:790320131028287488>",
            "<:fire:790320130483421245>",
            "<:ice:790320130738356224>",
            "<:elec:790320130151809047>",
            "<:wind:790320130521169922>",
            "<:psy:790320130772566046>",
            "<:nuclear:790320130584084532>",
            "<:bless:790320130746744892>",
            "<:curse:790320130387214336>",
            "<:almighty:790320130297954374>",
            "🔼",
            "❌"
        ]
        self.elementos = [
            "Física",
            "Arma de Fogo",
            "Fogo",
            "Gelo",
            "Elétrica",
            "Vento",
            "Psy",
            "Nuclear",
            "Benção",
            "Maldição",
            "Onipotência"
        ]

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
            persona_id = Database.persona_id(nome)
            nivel = Database.nivel_persona(persona_id)
            titulo = f'**{nome}**'
            cor = "vermelho"
            campos = [
                ("**Nível base**", nivel),
                ("**Arcana**", arcana),
                (f'**{ficha[1][0][0]}**', ficha[1][0][1]),
                (f'**{ficha[1][1][0]}**', ficha[1][1][1]),
                (f'**{ficha[1][2][0]}**', ficha[1][2][1]),
                (f'**{ficha[1][3][0]}**', ficha[1][3][1]),
                (f'**{ficha[1][4][0]}**', ficha[1][4][1]),
                (f'**{ficha[1][5][0]}**', ficha[1][5][1]),
                (f'**{ficha[1][6][0]}**', ficha[1][6][1])
            ]
            embed1 = EmbedComCampos(self.bot, canal, titulo, False, cor, foto, campos, False)
            titulo = "**Fraquezas**"
            campos = Gerador.gerador_campos_fraquezas(ficha)
            embed2 = EmbedComCampos(self.bot, canal, titulo, False, cor, False, campos, True)
            await embed1.enviar_embed()
            await embed2.enviar_embed()
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
                titulo = f'**{nome}**'
                cor = "vermelho"
                info_fraquezas = {
                    0: {0: "???", 1: ficha[1][0][1]},
                    1: {0: "???", 1: ficha[1][1][1]},
                    2: {0: "???", 1: ficha[1][2][1]},
                    3: {0: "???", 1: ficha[1][3][1]},
                    4: {0: "???", 1: ficha[1][4][1]},
                    5: {0: "???", 1: ficha[1][5][1]},
                    6: {0: "???", 1: ficha[1][6][1]},
                    7: {0: "???", 1: ficha[1][7][1]},
                    8: {0: "???", 1: ficha[1][8][1]},
                    9: {0: "???", 1: ficha[1][9][1]},
                    10: {0: "???", 1: ficha[1][10][1]}
                }
                campos = [
                    ("Nível base", nivel),
                    ("<:phys:790320130810839101>", info_fraquezas[0][info[shadow_id][0]]),
                    ("<:gun:790320131028287488>", info_fraquezas[1][info[shadow_id][1]]),
                    ("<:fire:790320130483421245>", info_fraquezas[2][info[shadow_id][2]]),
                    ("<:ice:790320130738356224>", info_fraquezas[3][info[shadow_id][3]]),
                    ("<:elec:790320130151809047>", info_fraquezas[4][info[shadow_id][4]]),
                    ("<:wind:790320130521169922>", info_fraquezas[5][info[shadow_id][5]]),
                    ("<:psy:790320130772566046>", info_fraquezas[6][info[shadow_id][6]]),
                    ("<:nuclear:790320130584084532>", info_fraquezas[7][info[shadow_id][7]]),
                    ("<:bless:790320130746744892>", info_fraquezas[8][info[shadow_id][8]]),
                    ("<:curse:790320130387214336>", info_fraquezas[9][info[shadow_id][9]]),
                    ("<:almighty:790320130297954374>", info_fraquezas[10][info[shadow_id][10]])
                ]
                embed = EmbedComCampos(self.bot, canal, titulo, False, cor, foto, campos, True)
                await embed.enviar_embed()
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
            titulo = f'**Revelando afinidades elementais de {nome}**'
            descricao = "Reaja com o elemento desejado (:arrow_up_small: para revelação completa)"
            cor = "azul"
            embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, False, False, self.reacoes_elementos)
            opcao = await embed.enviar_embed_reacoes()
            if opcao < 12:
                info[shadow_id][opcao-1] = 1
                mensagem = f'Afinidade **{self.elementos[opcao-1]}** de {nome} agora é conhecida pelo grupo'
            elif opcao == 12:
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
            titulo = f'**Afinidades conhecidas de {nome} atualizadas**'
            descricao = mensagem
            embed = Embed(self.bot, ctx, titulo, descricao, cor, False)
            await embed.enviar_embed()
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
            titulo = f'**Escondendo afinidades elementais de {nome}**'
            descricao = "Reaja com o elemento desejado (:arrow_up_small: para revelação completa)"
            cor = "azul"
            embed = EmbedComReacao(self.bot, ctx, titulo, descricao, cor, False, False, False, self.reacoes_elementos)
            opcao = await embed.enviar_embed_reacoes()
            if opcao < 12:
                info[shadow_id][opcao-1] = 0
                mensagem = f'Afinidade **{self.elementos[opcao-1]}** de {nome} agora não é mais conhecida pelo grupo'
            elif opcao == 12:
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
            titulo = f'**Afinidades conhecidas de {nome} atualizadas**'
            descricao = mensagem
            embed = Embed(self.bot, ctx, titulo, descricao, cor, False)
            await embed.enviar_embed()
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
            titulo_personagem = "**Ficha de personagem**"
            descricao_personagem = f'Atributos, equipamentos e Persona de **{personagem}**'
            cor = "vermelho"
            foto_personagem = Database.foto_personagem(personagem_id)
            eh_fool = Database.eh_fool(personagem_id)
            embed_personas = 0
            canal = self.bot.get_channel(Canal.carregar_canal_jogador(personagem))
            campos_personagem = []
            campos_info = []
            campos_equipamentos = []
            equips = Database.itens_equipados(personagem_id)
            persona_id = Database.persona_equipada(personagem_id)
            ficha = Database.ficha_personagem(personagem_id, persona_id)
            skills = Database.skills(personagem_id, persona_id)
            nivel_persona = Database.nivel(personagem_id, persona_id)
            if equips[0] != None:
                item = Database.nome_item(equips[0])
                campo = ("Arma corpo-a-corpo", item)
                campos_equipamentos.append(campo)
            if equips[1] != None:
                item = Database.nome_item(equips[1])
                campo = ("Arma à distância", item)
                campos_equipamentos.append(campo)
            if equips[2] != None:
                item = Database.nome_item(equips[2])
                campo = ("Armadura", item)
                campos_equipamentos.append(campo)
            if equips[3] != None:
                item = Database.nome_item(equips[3])
                campo = ("Acessório", item)
                campos_equipamentos.append(campo)
            campos_persona = []
            nome_persona = ficha[0][0]
            foto_persona = ficha[0][1]
            arcana_persona = ficha[0][2]
            titulo_persona = f'**{nome_persona}**'
            emote = ["<:phys:790320130810839101>", "<:gun:790320131028287488>", "<:fire:790320130483421245>", "<:ice:790320130738356224>", "<:elec:790320130151809047>", "<:wind:790320130521169922>", "<:psy:790320130772566046>", "<:nuclear:790320130584084532>", "<:bless:790320130746744892>", "<:curse:790320130387214336>", "<:almighty:790320130297954374>", "<:ailment:790320130286551060>", "<:healing:790320130508718100>", "<:support:790320130323775518>", "<:passive:790320130780561408>", "<:navigator:798197909761556521>"]
            texto = ""
            for skill in skills:
                skill_id = Database.skill_id(skill)
                elemento = Database.elemento(skill_id)
                texto += f'{skill} {emote[elemento-1]}' + "\n"
            texto = texto[:-1]
            campo_habilidade = [("**Habilidades**", texto)]
            titulo_fraquezas = "**Fraquezas**"
            campos_fraquezas = Gerador.gerador_campos_fraquezas(ficha)
            atributos = [ficha[1][0][1], ficha[1][1][1], ficha[1][2][1], ficha[1][3][1], ficha[1][4][1], ficha[1][5][1], ficha[1][6][1]]
            atributos_soma = Database.atributos_total("soma", personagem_id)
            atributos_porcent = Database.atributos_total("porcent", personagem_id)
            plus = []
            for i in range(len(atributos)):
                a = atributos[i] + atributos_soma[i]
                p = (atributos_porcent[i]/100) * a
                if atributos_soma[i] > 0:
                    plus.append(int(a+p))
                else:
                    plus.append(int(p))
            campos_atributos = [
                ("**Arcana**", arcana_persona),
                ("**Nível**", nivel_persona),
                (f'**{ficha[1][0][0]}**', f'{atributos[0]} +{plus[0]}'),
                (f'**{ficha[1][1][0]}**', f'{atributos[1]} +{plus[1]}'),
                (f'**{ficha[1][2][0]}**', f'{atributos[2]} +{plus[2]}'),
                (f'**{ficha[1][3][0]}**', f'{atributos[3]} +{plus[3]}'),
                (f'**{ficha[1][4][0]}**', f'{atributos[4]} +{plus[4]}'),
                (f'**{ficha[1][5][0]}**', f'{atributos[5]} +{plus[5]}'),
                (f'**{ficha[1][6][0]}**', f'{atributos[6]} +{plus[6]}')
            ]
            campos_personagem = campos_equipamentos
            if eh_fool:
                nivel_personagem = Database.nivel_fool(personagem_id)
                atributos = Database.atributos_fool_personagem(personagem_id)
                campos_info = [
                    ("Nível do personagem", nivel_personagem),
                    ("Vida (Hp)", atributos[0]),
                    ("Energia Espiritual (Sp)", atributos[1]),
                    ("Arcana", "Fool")
                ]
                campos_personagem = campos_info + campos_equipamentos
                del campos_atributos[2]
                del campos_atributos[2]
                lista_personas = Database.lista_personas(personagem_id)
                texto = ""
                for persona in lista_personas:
                    texto += persona + "\n"
                texto = texto[:-1]
                titulo_personas = f'Lista de personas de **{personagem}**'
                campo_personas = [("Personas", texto)]
                embed_personas = EmbedComCampos(self.bot, canal, titulo_personas, False, cor, False, campo_personas, False)
            campos_persona = campos_atributos + campo_habilidade
            embed_personagem = EmbedComCampos(self.bot, canal, titulo_personagem, descricao_personagem, cor, foto_personagem, campos_personagem, False)
            embed_persona = EmbedComCampos(self.bot, canal, titulo_persona, False, cor, foto_persona, campos_persona, False)
            embed_fraquezas = EmbedComCampos(self.bot, canal, titulo_fraquezas, False, cor, False, campos_fraquezas, True)
            await embed_personagem.enviar_embed()
            await embed_persona.enviar_embed()
            await embed_fraquezas.enviar_embed()
            if embed_personas != 0:
                await embed_personas.enviar_embed()
        else:
            await ctx.send("Personagem não encontrado.")

def setup(bot):
    bot.add_cog(Ficha(bot))