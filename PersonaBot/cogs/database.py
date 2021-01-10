import urllib.parse as up
import psycopg2
import json

f = open('./config.json')
data = json.load(f)

conn = psycopg2.connect(f"""dbname='{data['dbname']}' user='{data['user']}' host='{data['host']}' password='{data['password']}'""")
cur = conn.cursor()

class Database:
        @staticmethod
        def ficha_persona(nome):
                select_atributos = """
select atributo.nome, persona_atributo.valor 
from persona inner join persona_atributo on 
persona.persona_id = persona_atributo.fk_persona_persona_id inner join atributo on 
persona_atributo.fk_atributo_atributo_id = atributo.atributo_id 
where persona.nome=%s
order by atributo.atributo_id;
"""
                select_fraquezas = """
select elemento.nome, interacao_elemento.nome_interacao
from persona inner join reacao_elemental on
persona.persona_id = reacao_elemental.fk_persona_persona_id inner join elemento on
reacao_elemental.fk_elemento_elemento_id = elemento_id inner join interacao_elemento on
reacao_elemental.fk_interacao_elemento_interacao_id = interacao_elemento.interacao_id
where persona.nome=%s
order by elemento.elemento_id
"""
                select_persona = """
select persona.nome, persona.link_foto, arcana.nome 
from persona inner join persona_arcana on 
persona.persona_id = persona_arcana.fk_persona_persona_id inner join arcana on
persona_arcana.fk_arcana_arcana_id = arcana.arcana_id
where persona.nome = %s
"""
                cur.execute(select_atributos,[nome,])
                atributos = cur.fetchall()
                cur.execute(select_fraquezas,[nome,])
                fraquezas = cur.fetchall()
                cur.execute(select_persona,[nome,])
                persona = cur.fetchone()
                ficha = (persona, atributos, fraquezas)
                return ficha
        
        @staticmethod
        def ficha_shadow(nome):
                select_fraquezas = """
select elemento.nome, interacao_elemento.nome_interacao
from persona inner join reacao_elemental on
persona.persona_id = reacao_elemental.fk_persona_persona_id inner join elemento on
reacao_elemental.fk_elemento_elemento_id = elemento_id inner join interacao_elemento on
reacao_elemental.fk_interacao_elemento_interacao_id = interacao_elemento.interacao_id inner join shadow on
persona.persona_id = shadow.fk_persona_persona_id
where shadow.codinome = %s
order by elemento.elemento_id
"""
                select_shadow = """
select persona.persona_id, shadow.codinome, persona.link_foto, arcana.nome 
from persona inner join persona_arcana on 
persona.persona_id = persona_arcana.fk_persona_persona_id inner join arcana on
persona_arcana.fk_arcana_arcana_id = arcana.arcana_id inner join shadow on
persona.persona_id = shadow.fk_persona_persona_id
where shadow.codinome = %s
"""
                cur.execute(select_fraquezas,[nome,])
                fraquezas = cur.fetchall()
                cur.execute(select_shadow,[nome,])
                shadow = cur.fetchone()
                ficha = (shadow, fraquezas)
                return ficha

        @staticmethod
        def lista_shadows_id():
                try:
                        select_shadows = """
select persona.persona_id from persona inner join shadow on persona.persona_id = shadow.fk_persona_persona_id
"""
                        cur.execute(select_shadows)
                        lista = cur.fetchall()
                        shadows = []
                        for elem in lista:
                                shadows.append(elem[0])
                        return shadows
                except:
                        return False

        @staticmethod
        def shadow_id(shadow):
                try:
                        select_shadow = """
select persona.persona_id from persona inner join shadow on persona.persona_id = shadow.fk_persona_persona_id
where shadow.codinome = %s
"""
                        cur.execute(select_shadow,[shadow,])
                        elem = cur.fetchone()
                        shadow_id = elem[0]
                        return shadow_id
                except:
                        return False

        @staticmethod
        def item_id(item):
                try:
                        select_item = """
select item.item_id from item where item.nome = %s
"""
                        cur.execute(select_item,[item,])
                        elem = cur.fetchone()
                        item_id = elem[0]
                        return item_id
                except:
                        return False
        
        @staticmethod
        def item_no_inventario(item):
                try:
                        select_item = """
select item.item_id, inventario.quant from item inner join inventario on
item.item_id = inventario.fk_item_item_id
where item.nome = %s
"""
                        cur.execute(select_item,[item,])
                        elem = cur.fetchone()
                        if elem == None:
                                return False
                        else:
                                return elem
                except:
                        return False
        
        @staticmethod
        def item_no_inventario2(item_id):
                try:
                        select_item = """
select item.item_id, inventario.quant from item inner join inventario on
item.item_id = inventario.fk_item_item_id
where item.item_id = %s
"""
                        cur.execute(select_item,[item_id,])
                        elem = cur.fetchone()
                        if elem == None:
                                return False
                        else:
                                return elem
                except:
                        return False
        
        @staticmethod
        def add_item_database(item_id, quant):
                try:
                        insert_item = """
insert into inventario(quant, fk_item_item_id, fk_grupo_grupo_id) values (%s, %s, 1);
"""
                        cur.execute(insert_item,(quant, item_id))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def soma_item_database(item_id, quant_inicial, quant):
                nova_quant = quant_inicial + quant
                try:
                        update_item = """
update inventario set quant = %s where fk_item_item_id = %s;
"""
                        cur.execute(update_item,(nova_quant, item_id))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def subtrai_item_database(item_id, quant_inicial, quant):
                nova_quant = quant_inicial - quant
                try:
                        update_item = """
update inventario set quant = %s where fk_item_item_id = %s;
"""
                        cur.execute(update_item,(nova_quant, item_id))
                        conn.commit()
                        return True
                except:
                        return False

        @staticmethod
        def del_item_database(item_id):
                try:
                        delete_item = """
delete from inventario where fk_item_item_id = %s;
"""
                        cur.execute(delete_item,(item_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def inventario_grupo():
                select_itens = """
select item.nome, tipo_item.nome, inventario.quant from item inner join inventario on
item.item_id = inventario.fk_item_item_id inner join tipo_item on
item.fk_tipo_item_tipo_id = tipo_item.tipo_id;
"""
                cur.execute(select_itens)
                itens = cur.fetchall()
                if itens != None:
                        return itens
                else:
                        return False
        
        @staticmethod
        def dinheiro_grupo():
                select_dinheiro = """
select grupo.dinheiro from grupo where grupo.grupo_id = 1;
"""
                cur.execute(select_dinheiro)
                dinheiro = cur.fetchone()
                dinheiro = dinheiro[0]
                return dinheiro
        
        @staticmethod
        def modificar_dinheiro(quant):
                try:
                        update_dinheiro = """
update grupo set dinheiro = %s where grupo_id = 1;
"""
                        cur.execute(update_dinheiro,(quant,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def itens_drop(shadow_id):
                select_drops = """
select item.item_id, drop.chance from item inner join drop on
item.item_id = drop.fk_item_item_id
where drop.fk_shadow_fk_persona_persona_id = %s
"""
                cur.execute(select_drops,(shadow_id,))
                drops = cur.fetchall()
                if drops != None:
                        return drops
                else:
                        return False
        
        @staticmethod
        def dinheiro_exp(shadow_id):
                select = """
select shadow.dinheiro, shadow.exp from shadow
where shadow.fk_persona_persona_id = %s
"""
                cur.execute(select,(shadow_id,))
                coisas = cur.fetchall()
                coisas = coisas[0]
                if coisas != None:
                        return coisas
                else:
                        return False
        
        @staticmethod
        def nome_item(item_id):
                try:
                        select_item = """
select item.nome from item where item.item_id =%s
"""
                        cur.execute(select_item,(item_id,))
                        item = cur.fetchone()
                        item = item[0]
                        return item
                except:
                        return False

        @staticmethod
        def personagem_id(personagem):
                try:
                        select_personagem = """
select personagem.personagem_id from personagem where personagem.nome =%s
"""
                        cur.execute(select_personagem,(personagem,))
                        personagem_id = cur.fetchone()
                        personagem_id = personagem_id[0]
                        return personagem_id
                except:
                        return False
        
        @staticmethod
        def tipo_item_id(item_id):
                select_tipo_item = """
select tipo_item.tipo_id from tipo_item inner join item on
tipo_item.tipo_id = item.fk_tipo_item_tipo_id
where item.item_id = %s
"""
                cur.execute(select_tipo_item,(item_id,))
                tipo_item_id = cur.fetchone()
                tipo_item_id = tipo_item_id[0]
                if tipo_item_id != None:
                        return tipo_item_id
                else:
                        return False
        
        @staticmethod
        def equipar_item(personagem_id, item_id, tipo_item_id):
                update_personagem = ""
                if tipo_item_id == 7:
                        update_personagem = """
update personagem set meelee = %s where personagem.personagem_id = %s;
"""
                elif tipo_item_id == 8:
                        update_personagem = """
update personagem set ranged = %s where personagem.personagem_id = %s;
"""
                elif tipo_item_id == 9:
                        update_personagem = """
update personagem set armadura = %s where personagem.personagem_id = %s;
"""
                elif tipo_item_id == 10:
                        update_personagem = """
update personagem set acessorio = %s where personagem.personagem_id = %s;
"""
                else:
                        return False

                cur.execute(update_personagem,(item_id, personagem_id,))
                conn.commit()
                return True
        
        @staticmethod
        def desequipar_item(personagem_id, tipo_item_id):
                update_personagem = ""
                if tipo_item_id == 7:
                        update_personagem = """
update personagem set meelee = null where personagem.personagem_id = %s;
"""
                elif tipo_item_id == 8:
                        update_personagem = """
update personagem set ranged = null where personagem.personagem_id = %s;
"""
                elif tipo_item_id == 9:
                        update_personagem = """
update personagem set armadura = null where personagem.personagem_id = %s;
"""
                elif tipo_item_id == 10:
                        update_personagem = """
update personagem set acessorio = null where personagem.personagem_id = %s;
"""
                else:
                        return False
                cur.execute(update_personagem,(personagem_id,))
                conn.commit()
                return True
        
        @staticmethod
        def item_equipado(personagem_id, item_id, tipo_item_id):
                try:
                        select = ""
                        if tipo_item_id == 7:
                                select = """
select personagem.meelee from personagem
where personagem.personagem_id = %s
"""
                        elif tipo_item_id == 8:
                                select = """
select personagem.ranged from personagem
where personagem.personagem_id = %s
"""     
                        elif tipo_item_id == 9:
                                select = """
select personagem.armadura from personagem
where personagem.personagem_id = %s
"""     
                        else:
                                select = """
select personagem.acessorio from personagem
where personagem.personagem_id = %s
"""    
                        cur.execute(select,(personagem_id,))
                        equip_item_id = cur.fetchone()
                        equip_item_id = equip_item_id[0]
                        if equip_item_id == item_id:
                                return True
                        else:
                                return False
                except:
                        return False

        @staticmethod
        def eh_fool(personagem_id):
                select = """
select personagem.fool from personagem where personagem.personagem_id = %s
"""
                cur.execute(select,(personagem_id,))
                eh_fool = cur.fetchone()
                eh_fool = eh_fool[0]
                return eh_fool
        
        @staticmethod
        def persona_equipada(personagem_id):
                select = """
select personagem.persona_equipada from personagem where personagem.personagem_id = %s
"""
                cur.execute(select,(personagem_id,))
                persona_id = cur.fetchone()
                persona_id = persona_id[0]
                return persona_id
        
        @staticmethod
        def skills(personagem_id, persona_id):
                try:
                        select_personagem_persona = """
select personagem_persona.personagem_persona_id from personagem_persona
where personagem_persona.fk_personagem_personagem_id = %s and 
personagem_persona.fk_persona_persona_id = %s
"""
                        cur.execute(select_personagem_persona,[personagem_id, persona_id])
                        personagem_persona = cur.fetchone()
                        personagem_persona = personagem_persona[0]
                        select = """
select habilidade.nome from habilidade inner join persona_habilidade on
habilidade.habilidade_id = persona_habilidade.fk_habilidade_habilidade_id inner join personagem_persona on
persona_habilidade.fk_personagem_persona_personagem_persona_id = personagem_persona.personagem_persona_id
where persona_habilidade.fk_personagem_persona_personagem_persona_id = %s
"""
                        cur.execute(select,(personagem_persona, ))
                        skills = cur.fetchall()
                        lista_skills = []
                        for skill in skills:
                                lista_skills.append(skill[0])
                        return lista_skills
                except:
                        return False
        
        @staticmethod
        def skills_id(personagem_id, persona_id):
                try:
                        select_personagem_persona = """
select personagem_persona.personagem_persona_id from personagem_persona
where personagem_persona.fk_personagem_personagem_id = %s and 
personagem_persona.fk_persona_persona_id = %s
"""
                        cur.execute(select_personagem_persona,[personagem_id, persona_id])
                        personagem_persona = cur.fetchone()
                        personagem_persona = personagem_persona[0]
                        select = """
select habilidade.habilidade_id from habilidade inner join persona_habilidade on
habilidade.habilidade_id = persona_habilidade.fk_habilidade_habilidade_id inner join personagem_persona on
persona_habilidade.fk_personagem_persona_personagem_persona_id = personagem_persona.personagem_persona_id
where persona_habilidade.fk_personagem_persona_personagem_persona_id = %s
"""
                        cur.execute(select,(personagem_persona,))
                        skills = cur.fetchall()
                        lista_skills = []
                        for skill in skills:
                                lista_skills.append(skill[0])
                        return lista_skills
                except:
                        return False
        
        @staticmethod
        def ficha_personagem(personagem_id, persona_id):
                select_level  = """
select personagem_persona.nivel from personagem_persona
where personagem_persona.fk_personagem_personagem_id = %s order by nivel desc limit 1
"""
                select_atributos_level1 = """
select atributo.nome, persona_atributo.valor 
from persona inner join persona_atributo on 
persona.persona_id = persona_atributo.fk_persona_persona_id inner join atributo on 
persona_atributo.fk_atributo_atributo_id = atributo.atributo_id 
where persona.persona_id=%s
order by atributo.atributo_id;
"""
                select_atributos_crescimento = """
select crescimento_atributo.nivel, atributo.atributo_id, crescimento_atributo.quantidade 
from personagem_persona inner join crescimento_atributo on 
personagem_persona.personagem_persona_id = crescimento_atributo.fk_personagem_persona_personagem_persona_id inner join atributo on 
crescimento_atributo.fk_atributo_atributo_id = atributo.atributo_id
where personagem_persona.fk_persona_persona_id = %s and personagem_persona.fk_personagem_personagem_id = %s
order by crescimento_atributo.nivel, atributo.atributo_id;
"""
                select_fraquezas = """
select elemento.nome, interacao_elemento.nome_interacao
from persona inner join reacao_elemental on
persona.persona_id = reacao_elemental.fk_persona_persona_id inner join elemento on
reacao_elemental.fk_elemento_elemento_id = elemento_id inner join interacao_elemento on
reacao_elemental.fk_interacao_elemento_interacao_id = interacao_elemento.interacao_id
where persona.persona_id=%s
order by elemento.elemento_id
"""
                select_persona = """
select persona.nome, persona.link_foto, arcana.nome 
from persona inner join persona_arcana on 
persona.persona_id = persona_arcana.fk_persona_persona_id inner join arcana on
persona_arcana.fk_arcana_arcana_id = arcana.arcana_id
where persona.persona_id = %s
"""
                cur.execute(select_level,[personagem_id,])
                level = cur.fetchone()
                level = level[0]
                cur.execute(select_atributos_level1,[persona_id,])
                atributos = cur.fetchall()
                lista_atributos = []
                for nome, quant in atributos:
                        lista_atributos.append([nome, quant])
                if level > 1:
                        cur.execute(select_atributos_crescimento,[persona_id, personagem_id,])
                        crescimento = cur.fetchall()
                        for nivel, atributo_id, quant in crescimento:
                                if atributo_id == 1:
                                        lista_atributos[0][1] += quant
                                elif atributo_id == 2:
                                        lista_atributos[1][1] += quant
                                elif atributo_id == 3:
                                        lista_atributos[2][1] += quant
                                elif atributo_id == 4:
                                        lista_atributos[3][1] += quant
                                elif atributo_id == 5:
                                        lista_atributos[4][1] += quant
                                elif atributo_id == 6:
                                        lista_atributos[5][1] += quant
                                else:
                                        lista_atributos[6][1] += quant
                cur.execute(select_fraquezas,[persona_id,])
                fraquezas = cur.fetchall()
                cur.execute(select_persona,[persona_id,])
                persona = cur.fetchone()
                ficha = (persona, lista_atributos, fraquezas)
                return ficha
        
        @staticmethod
        def itens_equipados(personagem_id):
                select = """
select personagem.meelee, personagem.ranged, personagem.armadura, personagem.acessorio from personagem where personagem.personagem_id = %s
"""
                cur.execute(select,(personagem_id,))
                equips = cur.fetchone()
                return equips
        
        @staticmethod
        def nivel(personagem_id, persona_id):
                select = """
select personagem_persona.nivel from personagem_persona
where personagem_persona.fk_personagem_personagem_id = %s and
personagem_persona.fk_persona_persona_id = %s
"""
                cur.execute(select,(personagem_id, persona_id,))
                nivel = cur.fetchone()
                nivel = nivel[0]
                return nivel
        
        @staticmethod
        def foto_personagem(personagem_id):
                select = """
select personagem.foto from personagem
where personagem.personagem_id = %s
"""
                cur.execute(select,(personagem_id,))
                foto = cur.fetchone()
                foto = foto[0]
                return foto
        
        @staticmethod
        def aumentar_nivel(personagem_id):
                try:
                        update = """
update personagem_persona set nivel = nivel + 1 where fk_personagem_personagem_id = %s;
"""
                        cur.execute(update,(personagem_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def diminuir_nivel(personagem_id):
                try:
                        update = """
update personagem_persona set nivel = nivel - 1 where fk_personagem_personagem_id = %s;
"""
                        cur.execute(update,(personagem_id,))
                        conn.commit()
                        return True
                except:
                        return False
                
        @staticmethod
        def aumentar_status(personagem_persona_id, nivel, atributos):
                try:
                        aumento_status = """
insert into crescimento_atributo(nivel, quantidade, fk_atributo_atributo_id, fk_personagem_persona_personagem_persona_id)
values (%s, %s, %s, %s)
"""
                        cur.execute(aumento_status,(nivel, atributos[0], 1 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[1], 2 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[2], 3 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[3], 4 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[4], 5 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[5], 6 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[6], 7 , personagem_persona_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def atributos_iniciais(persona_id):
                select_atributos = """
select atributo.atributo_id, persona_atributo.valor 
from persona inner join persona_atributo on 
persona.persona_id = persona_atributo.fk_persona_persona_id inner join atributo on 
persona_atributo.fk_atributo_atributo_id = atributo.atributo_id 
where persona.persona_id=%s
order by atributo.atributo_id;
"""
                cur.execute(select_atributos,[persona_id,])
                atributos = cur.fetchall()
                return atributos
        
        @staticmethod
        def personagem_persona_id(personagem_id, persona_id):
                try:
                        select_personagem_persona = """
select personagem_persona.personagem_persona_id from personagem_persona
where personagem_persona.fk_personagem_personagem_id = %s and 
personagem_persona.fk_persona_persona_id = %s
"""
                        cur.execute(select_personagem_persona,[personagem_id, persona_id])
                        personagem_persona = cur.fetchone()
                        personagem_persona = personagem_persona[0]
                        return personagem_persona
                except:
                        return False
        
        @staticmethod
        def atributos(personagem_id, persona_id):
                select_level  = """
select personagem_persona.nivel from personagem_persona
where personagem_persona.fk_personagem_personagem_id = %s order by nivel desc limit 1
"""
                select_atributos_level1 = """
select atributo.nome, persona_atributo.valor 
from persona inner join persona_atributo on 
persona.persona_id = persona_atributo.fk_persona_persona_id inner join atributo on 
persona_atributo.fk_atributo_atributo_id = atributo.atributo_id 
where persona.persona_id=%s
order by atributo.atributo_id;
"""
                select_atributos_crescimento = """
select crescimento_atributo.nivel, atributo.atributo_id, crescimento_atributo.quantidade 
from personagem_persona inner join crescimento_atributo on 
personagem_persona.personagem_persona_id = crescimento_atributo.fk_personagem_persona_personagem_persona_id inner join atributo on 
crescimento_atributo.fk_atributo_atributo_id = atributo.atributo_id
where personagem_persona.fk_persona_persona_id = %s and personagem_persona.fk_personagem_personagem_id = %s
order by crescimento_atributo.nivel, atributo.atributo_id;
"""
                cur.execute(select_level,[personagem_id,])
                level = cur.fetchone()
                level = level[0]
                cur.execute(select_atributos_level1,[persona_id,])
                atributos = cur.fetchall()
                lista_atributos = []
                for nome, quant in atributos:
                        lista_atributos.append([nome, quant])
                if level > 1:
                        cur.execute(select_atributos_crescimento,[persona_id, personagem_id,])
                        crescimento = cur.fetchall()
                        for nivel, atributo_id, quant in crescimento:
                                if atributo_id == 1:
                                        lista_atributos[0][1] += quant
                                elif atributo_id == 2:
                                        lista_atributos[1][1] += quant
                                elif atributo_id == 3:
                                        lista_atributos[2][1] += quant
                                elif atributo_id == 4:
                                        lista_atributos[3][1] += quant
                                elif atributo_id == 5:
                                        lista_atributos[4][1] += quant
                                elif atributo_id == 6:
                                        lista_atributos[5][1] += quant
                                else:
                                        lista_atributos[6][1] += quant
                return lista_atributos
        
        @staticmethod
        def apagar_crecimento(personagem_persona_id, nivel):
                try:
                        delete = """
delete from crescimento_atributo
where crescimento_atributo.fk_personagem_persona_personagem_persona_id = %s and crescimento_atributo.nivel = %s
"""
                        cur.execute(delete,(personagem_persona_id, nivel,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def nivel_persona(persona_id):
                try:
                        select = """
select persona.nivel from persona where persona.persona_id = %s
"""
                        cur.execute(select,(persona_id,))
                        nivel = cur.fetchone()
                        nivel = nivel[0]
                        return nivel
                except:
                        return False
        
        @staticmethod
        def persona_id(persona):
                try:
                        select = """
select persona.persona_id from persona where persona.nome = %s
"""
                        cur.execute(select,(persona,))
                        persona_id = cur.fetchone()
                        persona_id = persona_id[0]
                        return persona_id
                except:
                        return False

        @staticmethod
        def persona_id_shadow(shadow):
                try:
                        select = """
select persona.persona_id 
from persona inner join persona_arcana on 
persona.persona_id = persona_arcana.fk_persona_persona_id inner join arcana on
persona_arcana.fk_arcana_arcana_id = arcana.arcana_id inner join shadow on
persona.persona_id = shadow.fk_persona_persona_id
where shadow.codinome = %s
"""
                        cur.execute(select,(shadow,))
                        persona_id = cur.fetchone()
                        persona_id = persona_id[0]
                        return persona_id
                except:
                        return False
        
        @staticmethod
        def atributos_fool_personagem(personagem_id):
                try:
                        select_level  = """
select personagem.nivel from personagem where personagem.personagem_id = %s
"""
                        select1 = """
select personagem.hp, personagem.sp from personagem
where personagem.personagem_id = %s
"""
                        select2 = """
select crescimento_fool.fk_atributo_atributo_id, crescimento_fool.quant from crescimento_fool
where crescimento_fool.fk_personagem_personagem_id = %s
"""
                        cur.execute(select_level,(personagem_id,))
                        level = cur.fetchone()
                        level = level[0]
                        cur.execute(select1,(personagem_id,))
                        atributos = cur.fetchone()
                        lista_atributos = [atributos[0], atributos[1]]
                        if level > 1:
                                cur.execute(select2,(personagem_id,))
                                crescimento_atributos = cur.fetchall()
                                for atributo_id, quant in crescimento_atributos:
                                        if atributo_id == 1:
                                                lista_atributos[0] += quant
                                        else:
                                                lista_atributos[1] += quant
                        return lista_atributos
                except:
                        return False
        
        @staticmethod
        def nivel_fool(personagem_id):
                try:
                        select_level  = """
select personagem.nivel from personagem where personagem.personagem_id = %s
"""
                        cur.execute(select_level,(personagem_id,))
                        level = cur.fetchone()
                        level = level[0]
                        return level
                except:
                        return False
        
        @staticmethod
        def lista_personas(personagem_id):
                try:
                        select = """
select persona.nome from persona inner join personagem_persona on
personagem_persona.fk_persona_persona_id = persona.persona_id
where personagem_persona.fk_personagem_personagem_id = %s and personagem_persona.compendium = false
""" 
                        cur.execute(select,(personagem_id,))
                        personas = cur.fetchall()
                        lista_personas = []
                        for persona in personas:
                                lista_personas.append(persona[0])
                        return lista_personas
                except:
                        return False
        
        @staticmethod
        def aumentar_nivel_fool(personagem_id):
                try:
                        update = """
update personagem set nivel = nivel + 1 where personagem.personagem_id = %s
""" 
                        cur.execute(update,(personagem_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def diminuir_nivel_fool(personagem_id):
                try:
                        update = """
update personagem set nivel = nivel - 1 where personagem.personagem_id = %s
""" 
                        cur.execute(update,(personagem_id,))
                        conn.commit()
                        return True
                except:
                        return False
                
        @staticmethod
        def atributos_iniciais_fool(personagem_id):
                try:
                        select = """
select personagem.hp, personagem.sp from personagem
where personagem.personagem_id = %s
"""
                        cur.execute(select,(personagem_id,))
                        atributos = cur.fetchall()
                        return atributos
                except:
                        return False
        
        @staticmethod
        def aumentar_status_fool(personagem_id, nivel, atributos):
                try:
                        select = """
insert into crescimento_fool(nivel, quant, fk_personagem_personagem_id, fk_atributo_atributo_id)
values (%s, %s, %s, %s)
"""
                        cur.execute(select,(nivel, atributos[0], personagem_id, 1,))
                        cur.execute(select,(nivel, atributos[1], personagem_id, 2,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def apagar_crecimento_fool(personagem_id, nivel):
                try:
                        delete = """
delete from crescimento_fool
where crescimento_fool.fk_personagem_personagem_id = %s and crescimento_fool.nivel = %s
"""
                        cur.execute(delete,(personagem_id, nivel,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def aumentar_status_fool_persona(personagem_persona_id, nivel, atributos):
                try:
                        aumento_status = """
insert into crescimento_atributo(nivel, quantidade, fk_atributo_atributo_id, fk_personagem_persona_personagem_persona_id)
values (%s, %s, %s, %s)
"""
                        cur.execute(aumento_status,(nivel, atributos[2], 3 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[3], 4 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[4], 5 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[5], 6 , personagem_persona_id,))
                        cur.execute(aumento_status,(nivel, atributos[6], 7 , personagem_persona_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def nome_persona(persona_id):
                try:
                        select = """
select persona.nome from persona
where persona.persona_id = %s
"""
                        cur.execute(select,(persona_id,))
                        persona_nome = cur.fetchone()
                        return persona_nome[0]
                except:
                        return False
        
        @staticmethod
        def equipar_persona(personagem_id, persona_id):
                try:
                        update = """
update personagem set persona_equipada = %s where personagem.personagem_id = %s
"""
                        cur.execute(update,(persona_id, personagem_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def personagem_add_persona(personagem_id, persona_id):
                nivel = Database.nivel_persona(persona_id)
                try:
                        insert = """
insert into personagem_persona(nivel, fk_personagem_personagem_id, fk_persona_persona_id, compendium)
values (%s, %s, %s, false)
"""
                        select_skills = """
select habilidade_persona.fk_habilidade_habilidade_id from habilidade_persona
where nivel = %s and fk_persona_persona_id = %s
"""
                        insert_skills = """
insert into persona_habilidade(fk_habilidade_habilidade_id, fk_personagem_persona_personagem_persona_id)
values (%s, %s)
"""
                        cur.execute(insert,(nivel, personagem_id, persona_id,))
                        cur.execute(select_skills,(nivel, persona_id,))
                        skills = cur.fetchall()
                        personagem_persona_id = Database.personagem_persona_id(personagem_id, persona_id)
                        for skill in skills:
                                cur.execute(insert_skills,(skill, personagem_persona_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def personagem_del_persona(personagem_id, persona_id):
                personagem_persona_id = Database.personagem_persona_id(personagem_id, persona_id)
                try:
                        update = """
update personagem_persona set compendium = true where personagem_persona_id = %s
"""
                        cur.execute(update,(personagem_persona_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def compendium(personagem_persona_id):
                try:
                        select = """
select compendium from personagem_persona where personagem_persona_id = %s
"""
                        cur.execute(select,(personagem_persona_id,))
                        compendium = cur.fetchone()
                        return compendium[0]
                except:
                        return 0
        
        @staticmethod
        def personagem_reativar_persona(personagem_id, persona_id):
                personagem_persona_id = Database.personagem_persona_id(personagem_id, persona_id)
                try:
                        update = """
update personagem_persona set compendium = false where personagem_persona_id = %s
"""
                        cur.execute(update,(personagem_persona_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def nivel_skills(nivel, persona_id):
                select = """
select fk_habilidade_habilidade_id from habilidade_persona
where nivel = %s and fk_persona_persona_id = %s
"""
                cur.execute(select,(nivel, persona_id,))
                skills = cur.fetchall()
                if skills != None:
                        return skills
                else:
                        return False
        
        @staticmethod
        def add_skill(skill_id, personagem_persona_id):
                try:
                        insert = """
insert into persona_habilidade(fk_habilidade_habilidade_id, fk_personagem_persona_personagem_persona_id)
values (%s, %s)
"""
                        cur.execute(insert,(skill_id, personagem_persona_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def del_skill(skill_id, personagem_persona_id):
                try:
                        delete = """
delete from persona_habilidade where fk_habilidade_habilidade_id = %s and fk_personagem_persona_personagem_persona_id = %s
"""
                        cur.execute(delete,(skill_id, personagem_persona_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def mod_skill(skill_antiga_id, skill_nova_id, personagem_persona_id):
                try:
                        update = """
update persona_habilidade set fk_habilidade_habilidade_id = %s
where fk_habilidade_habilidade_id = %s and fk_personagem_persona_personagem_persona_id = %s
"""
                        cur.execute(update,(skill_antiga_id, skill_nova_id, personagem_persona_id,))
                        conn.commit()
                        return True
                except:
                        return False
        

        @staticmethod
        def nome_skill(skill_id):
                try:
                        select = """
select nome from habilidade
where habilidade_id = %s
"""
                        cur.execute(select,(skill_id,))
                        skill_nome = cur.fetchone()
                        return skill_nome[0]
                except:
                        return False
        
        @staticmethod
        def skills_conhecidas(nivel,persona_id):
                try:
                        select = """
select fk_habilidade_habilidade_id from habilidade_persona
where nivel <= %s and fk_persona_persona_id = %s
"""
                        cur.execute(select,(nivel, persona_id,))
                        skills = cur.fetchall()
                        return skills
                except:
                        return False
        
        @staticmethod
        def skill_id(skill):
                try:
                        select = """
select habilidade.habilidade_id from habilidade
where habilidade.nome = %s
"""
                        cur.execute(select,(skill,))
                        skill = cur.fetchone()
                        return skill[0]
                except:
                        return False
        
        @staticmethod
        def discord_user(personagem_id):
                try:
                        select = """
select usuario from personagem
where personagem_id = %s
"""
                        cur.execute(select,(personagem_id,))
                        user = cur.fetchone()
                        return user[0]
                except:
                        return False
        
        @staticmethod
        def valor_item(item_id):
                try:
                        select = """
select valor from item
where item_id = %s
"""
                        cur.execute(select,(item_id,))
                        valor = cur.fetchone()
                        return valor[0]
                except:
                        return False

        @staticmethod
        def fraquezas(persona_id):
                select = """
select interacao_elemento.interacao_id
from persona inner join reacao_elemental on
persona.persona_id = reacao_elemental.fk_persona_persona_id inner join elemento on
reacao_elemental.fk_elemento_elemento_id = elemento_id inner join interacao_elemento on
reacao_elemental.fk_interacao_elemento_interacao_id = interacao_elemento.interacao_id
where persona.persona_id = %s
order by elemento.elemento_id
"""
                cur.execute(select,[persona_id])
                fraquezas = cur.fetchall()
                for i in range(len(fraquezas)):
                        fraquezas[i] = fraquezas[i][0]
                return fraquezas
        
        @staticmethod
        def add_atributo(personagem_id, atributo_id, quant):
                try:
                        update = """
update crescimento_personagem set quant = quant + %s
where fk_personagem_personagem_id = %s and fk_atributo_atributo_id = %s and fk_tipo_crescimento_tipo_crescimento_id = 1
"""
                        cur.execute(update,(quant, personagem_id, atributo_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def del_atributo(personagem_id, atributo_id, quant):
                try:
                        update = """
update crescimento_personagem set quant = quant - %s
where fk_personagem_personagem_id = %s and fk_atributo_atributo_id = %s and fk_tipo_crescimento_tipo_crescimento_id = 1
"""
                        cur.execute(update,(quant, personagem_id, atributo_id,))
                        conn.commit()
                        return True
                except:
                        return False
        
        @staticmethod
        def mod_atributo(personagem_id, atributo_id, quant):
                try:
                        update = """
update crescimento_personagem set quant = %s
where fk_personagem_personagem_id = %s and fk_atributo_atributo_id = %s and fk_tipo_crescimento_tipo_crescimento_id = 2
"""
                        cur.execute(update,(quant, personagem_id, atributo_id,))
                        conn.commit()
                        return True
                except:
                        return False

        @staticmethod
        def atributo_id(nome):
                try:
                        select = """
select atributo_id from atributo
where nome = %s
"""
                        cur.execute(select,(atributo_id,))
                        atributo_id = cur.fetchone()
                        return atributo_id[0]
                except:
                        return False
        
        @staticmethod
        def atributos_soma(personagem_id):
                try:
                        select = """
select quant from crescimento_personagem
where fk_personagem_personagem_id = %s and fk_tipo_crescimento_tipo_crescimento_id = 1
order by fk_atributo_atributo_id
"""
                        cur.execute(select,(personagem_id,))
                        atributos = cur.fetchall()
                        for i in range(len(atributos)):
                                atributos[i] = atributos[i][0]
                        return atributos
                except:
                        return False
        
        @staticmethod
        def atributos_porcent(personagem_id):
                try:
                        select = """
select quant from crescimento_personagem
where fk_personagem_personagem_id = %s and fk_tipo_crescimento_tipo_crescimento_id = 2
order by fk_atributo_atributo_id
"""
                        cur.execute(select,(personagem_id,))
                        atributos = cur.fetchall()
                        for i in range(len(atributos)):
                                atributos[i] = atributos[i][0]
                        return atributos
                except:
                        return False
        
        @staticmethod
        def intensidade(habilidade_id):
                try:
                        select = """
select fk_intensidade_intensidade_id from habilidade
where habilidade_id = %s
"""
                        cur.execute(select,(habilidade_id,))
                        intensidade = cur.fetchone()
                        return intensidade[0]
                except:
                        return False
        
        @staticmethod
        def elemento(habilidade_id):
                try:
                        select = """
select fk_elemento_elemento_id from habilidade
where habilidade_id = %s
"""
                        cur.execute(select,(habilidade_id,))
                        elemento = cur.fetchone()
                        return elemento[0]
                except:
                        return False
        
        @staticmethod
        def nome_elemento(elemento_id):
                try:
                        select = """
select nome from elemento
where elemento_id = %s
"""
                        cur.execute(select,(elemento_id,))
                        elemento = cur.fetchone()
                        return elemento[0]
                except:
                        return False

        @staticmethod
        def skills_shadow(shadow_id, nivel):
                try:
                        select = """
select fk_habilidade_habilidade_id from habilidade_persona
where fk_persona_persona_id = %s and nivel = %s
"""
                        cur.execute(select,(shadow_id, nivel,))
                        skills = cur.fetchall()
                        for i in range(len(skills)):
                                skills[i] = skills[i][0]
                        return skills
                except:
                        return False