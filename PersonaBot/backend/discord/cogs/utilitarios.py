from cogs.database import Database

class Ordenacao:

    @staticmethod
    def ordenacao_emboscada(party, horda, emboscador):
        ordem1 = []
        ordem2 = []
        quant1 = []
        quant2 = []
        for personagem in party:
            personagem_id = Database.personagem_id(personagem)
            persona_id = Database.persona_equipada(personagem_id)
            atributos = Database.atributos(personagem_id, persona_id)
            agilidade = atributos[5]
            ordem1.append(personagem)
            quant1.append(agilidade)
        Ordenacao.insertion_sort(quant1, ordem1)
        for tipo, char in horda:
            if tipo == "s":
                shadow_id = Database.shadow_id(char)
                atributos = Database.atributos_iniciais(shadow_id)
                agilidade = atributos[5]
                ordem2.append(char)
                quant2.append(agilidade)
            else:
                personagem_id = Database.personagem_id(char)
                persona_id = Database.persona_equipada(personagem_id)
                atributos = Database.atributos(personagem_id, persona_id)
                agilidade = atributos[5]
                ordem2.append(personagem_id)
                quant2.append(agilidade)
        Ordenacao.insertion_sort(quant2, ordem2)
        if emboscador == "party":
            return ordem1 + ordem2
        else:
            return ordem2 + ordem1

    @staticmethod
    def ordenacao_disputa(party, horda):
        ordem = []
        quant = []
        for personagem in party:
            personagem_id = Database.personagem_id(personagem)
            persona_id = Database.persona_equipada(personagem_id)
            atributos = Database.atributos(personagem_id, persona_id)
            agilidade = atributos[5]
            ordem.append(personagem)
            quant.append(agilidade)
        for tipo, char in horda:
            if tipo == "s":
                shadow_id = Database.shadow_id(char)
                atributos = Database.atributos_iniciais(shadow_id)
                agilidade = atributos[5]
            else:
                personagem_id = Database.personagem_id(char)
                persona_id = Database.persona_equipada(personagem_id)
                atributos = Database.atributos(personagem_id, persona_id)
                agilidade = atributos[5]
                ordem.append(personagem_id)
                quant.append(agilidade)
        Ordenacao.insertion_sort(quant, ordem)
        return ordem

    @staticmethod
    def insertion_sort(arr, ordem):
        for i in range(1, len(arr)):
            key = arr[i]
            key2 = ordem[i]
            j = i-1
            while j >=0 and key < arr[j]:
                    arr[j+1] = arr[j]
                    ordem[j+1] = ordem[j]
                    j -= 1
            arr[j+1] = key
            ordem[j+1] = key2

class Somatorio:

    @staticmethod
    def atributos_totais_personagem(personagem_id, atributos):
        atributos_soma = Database.atributos_total("soma", personagem_id)
        atributos_porcent = Database.atributos_total("porcent", personagem_id)
        for i in range(len(atributos)):
            a = atributos[i] + atributos_soma[i]
            p = (atributos_porcent[i]/100) * a
            if atributos_soma[i] > 0:
                atributos[i] += int(a+p)
            else:
                atributos[i] += int(p)
        return atributos

class Reparador:

    @staticmethod
    def valores_atributos(atributos):
        for i in range(len(atributos)):
            atributos[i] = atributos[i][1]
        return atributos

    @staticmethod
    def repara_lista(lista, indice):
        nova_lista = []
        for i in range(len(lista)):
            nova_lista.append(lista[i][indice])
        return nova_lista

    @staticmethod
    def repara_nome(texto):
        nome = ""
        for palavra in texto:
            nome += palavra + " "
        nome = nome[:-1]
        return nome

class Gerador:

    @staticmethod
    def gerador_campos(chaves, valores):
        campos = []
        for i in range(len(valores)):
            campo = (chaves[i], valores[i])
            campos.append(campo)
        return campos

    @staticmethod
    def gerador_texto(lista_item):
        texto = ""
        for elem, quant in lista_item:
            texto += f'{elem} x{quant}; '
        texto = texto[:-2]
        return texto

    @staticmethod
    def gerador_campos_fraquezas(ficha):
        campos_fraquezas = [
            ("<:phys:790320130810839101>", ficha[2][0][1]),
            ("<:gun:790320131028287488>", ficha[2][1][1]),
            ("<:fire:790320130483421245>", ficha[2][2][1]),
            ("<:ice:790320130738356224>", ficha[2][3][1]),
            ("<:elec:790320130151809047>", ficha[2][4][1]),
            ("<:wind:790320130521169922>", ficha[2][5][1]),
            ("<:psy:790320130772566046>", ficha[2][6][1]),
            ("<:nuclear:790320130584084532>", ficha[2][7][1]),
            ("<:bless:790320130746744892>", ficha[2][8][1]),
            ("<:curse:790320130387214336>", ficha[2][9][1]),
            ("<:almighty:790320130297954374>", ficha[2][10][1])
        ]
        return campos_fraquezas

    @staticmethod
    def gerador_campos_atributos(fool, atributos):
        campos = []
        if fool:
            campos = [
                ("**St**", f'+{atributos[2]}'),
                ("**Ma**", f'+{atributos[3]}'),
                ("**En**", f'+{atributos[4]}'),
                ("**Ag**", f'+{atributos[5]}'),
                ("**Lu**", f'+{atributos[6]}')
            ]
        else:
            campos = [
                ("**HP**", f'+{atributos[0]}'),
                ("**SP**", f'+{atributos[1]}'),
                ("**St**", f'+{atributos[2]}'),
                ("**Ma**", f'+{atributos[3]}'),
                ("**En**", f'+{atributos[4]}'),
                ("**Ag**", f'+{atributos[5]}'),
                ("**Lu**", f'+{atributos[6]}')
            ]
        return campos

class Mensageiro:

    @staticmethod
    def informacoes_personagem(nome):
        informacoes = {}
        personagem_id = Database.personagem_id(nome)
        persona_id = Database.persona_equipada(personagem_id)
        usuario = Database.discord_user(personagem_id)
        equips = Database.itens_equipados(personagem_id)
        meelee = equips[0]
        ranged = equips[1]
        armadura = equips[2]
        fraquezas = Database.fraquezas(persona_id)
        atributos = Database.atributos(personagem_id, persona_id)
        atributos_base = Reparador.valores_atributos(atributos)
        atributos_somados = Somatorio.atributos_totais_personagem(personagem_id, atributos_base)
        skills = Database.skills_id(personagem_id, persona_id)
        informacoes["usuario"] = usuario
        informacoes["meelee"] = meelee
        informacoes["ranged"] = ranged
        informacoes["armadura"] = armadura
        informacoes["fraquezas"] = fraquezas
        informacoes["atributos"] = atributos_somados
        informacoes["skills"] = skills
        return informacoes

    @staticmethod
    def informacoes_shadow(nome):
        informacoes = {}
        shadow_id = Database.shadow_id(nome)
        fraquezas = Database.fraquezas(shadow_id)
        atributos_base = Database.atributos_iniciais(shadow_id)
        atributos_somados = Reparador.valores_atributos(atributos_base)
        nivel = Database.nivel_persona(shadow_id)
        skills = Database.skills_shadow(shadow_id, nivel)
        informacoes["fraquezas"] = fraquezas
        informacoes["skills"] = skills
        informacoes["atributos"] = atributos_somados
        return informacoes

    @staticmethod
    def info_armadura(armadura):
        valor_armadura = 0
        if armadura != None:
            valor_armadura = Database.valor_item(armadura)
        return valor_armadura

    @staticmethod
    def info_ranged(ranged):
        valor_arma = 0
        if ranged != None:
            valor_arma = Database.valor_item(ranged)
        return valor_arma

    @staticmethod
    def info_meelee(meelee):
        valor_arma = 0
        if meelee != None:
            valor_arma = Database.valor_item(meelee)
        return valor_arma