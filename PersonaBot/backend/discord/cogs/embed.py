import discord

class Embed:
    def __init__(self, bot, ctx, titulo, descricao, cor, imagem):
        self.bot = bot
        self.ctx = ctx
        self.titulo = titulo
        self.descricao = descricao
        self.obj_embed = 0
        self.seleciona_cor(cor)
        self.gerar_embed(imagem)

    def seleciona_cor(self, cor):
        cores = {"azul": discord.Colour.blue(), "vermelho": discord.Colour.red(), "verde": discord.Colour.green(), "laranja": discord.Colour.orange()}
        self.cor = cores[cor]

    def gerar_embed(self, imagem):
        obj_embed = discord.Embed(
            title=self.titulo,
            colour=self.cor
        )
        if self.descricao != False:
            obj_embed.description = self.descricao
        if imagem != False:
            self.obj_embed.set_image(url=imagem)
        self.obj_embed = obj_embed

    async def enviar_embed(self):
        embed_msg = await self.ctx.send(embed=self.obj_embed)
        return embed_msg

class EmbedComCampos(Embed):
    def __init__(self, bot, ctx, titulo, descricao, cor, imagem, campos, alinhamento):
        super().__init__(bot, ctx, titulo, descricao, cor, imagem)
        self.campos = campos
        self.alinhamento = alinhamento
        self.adicionar_campos()

    def adicionar_campos(self):
        for campo in self.campos:
            self.obj_embed.add_field(name=campo[0], value=campo[1], inline=self.alinhamento)

class EmbedComReacao(EmbedComCampos):
    def __init__(self,bot, ctx, titulo, descricao, cor, imagem, campos, alinhamento, reacoes):
        super().__init__(bot, ctx, titulo, descricao, cor, imagem, campos, alinhamento)
        self.reacoes = reacoes
    
    async def enviar_embed_reacoes(self):
        embed_msg = await self.enviar_embed()
        for reacao in self.reacoes:
            await embed_msg.add_reaction(emoji=reacao)
        opcao = 0
        while opcao == 0:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=None)
            if str(reaction.emoji) != None and str(user) != "Persona Bot#0708":
                for i in range(len(self.reacoes)):
                    if str(reaction.emoji) == self.reacoes[i]:
                        opcao = i + 1
                        break
        await embed_msg.delete()
        return opcao
    
    async def enviar_embed_reacoes_multiplas(self):
        embed_msg = await self.enviar_embed()
        for reacao in self.reacoes:
            await embed_msg.add_reaction(emoji=reacao)
        opcoes = []
        opcao = 0
        while opcao == 0:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=None)
            if str(reaction.emoji) != None and str(user) != "Persona Bot#0708":
                for i in range(len(self.reacoes)-2):
                    if str(reaction.emoji) == self.reacoes[i]:
                        opcoes.append(i + 1)
                if str(reaction.emoji) == self.reacoes[len(self.reacoes) - 1]:
                        opcao = len(self.reacoes)
                elif str(reaction.emoji) == self.reacoes[len(self.reacoes) - 2]:
                        opcao = len(self.reacoes) - 1
        if opcao == len(self.reacoes):
            opcoes = []
        final = (opcao, opcoes)
        await embed_msg.delete()
        return final


    
        

    