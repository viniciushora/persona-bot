from cogs.database import Database

class Ordenacao:

    @staticmethod
    def ordenacao_emboscada(party, horda):
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
        return ordem1 + ordem2
    
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
    def ordenacao_emboscado(party, horda):
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
        return ordem2 + ordem1

    @staticmethod
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

class Somatorio:

    @staticmethod
    def atributos_totais_personagem(personagem_id, atributos):
        atributos_soma = Database.atributos_soma(personagem_id)
        atributos_porcent = Database.atributos_porcent(personagem_id)
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

class Gerador:

    @staticmethod
    def gerador_campos(chaves, valores):
        campos = []
        for i in range(len(valores)):
            campo = (chaves[i], valores[i])
            campos.append(campo)
        return campos