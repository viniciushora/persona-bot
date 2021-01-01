import urllib.parse as up
import psycopg2

conn = psycopg2.connect("dbname='mkigjvup' user='mkigjvup' host='motty.db.elephantsql.com' password='s4d_bAHqGiWhyuZ8OaIMyDWPVc8lXBUE'")
cur = conn.cursor()

class Database:
        @staticmethod
        def ficha_persona(nome):
                print(nome)
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
                print(nome)
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
                select_item = """
select item.nome from item where item.item_id =%s
"""
                cur.execute(select_item,(item_id,))
                item = cur.fetchone()
                item = item[0]
                if item != None:
                        return item
                else:
                        return False